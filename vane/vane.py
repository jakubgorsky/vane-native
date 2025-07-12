import functools
import sys
import re

from vane.message_formatter.message_formatter import Message_Formatter

class Vane:
    instance = None

    @classmethod
    def init(cls, config):
        """
        Initializes the *single* Vane instance with configuration.
        This must be called once at application startup.
        """
        if cls.instance is not None:
            cls.instance.close()
            cls.instance._reconfigure(config)
        else:
            cls.instance = cls._create_instance(config)

        if not hasattr(cls, '_atexit_registered'):
            import atexit
            atexit.register(cls.instance.close)
            cls._atexit_registered = True

    @classmethod
    def _create_instance(cls, config):
        """Internal method to create a new Vane instance."""
        return cls(
            log_file = config.get('outfile', None),
            log_level = config.get('level', 'INFO'),
            text_style = config.get('style', None),
            theme = config.get('theme', None),
            timestamp_type = config.get('timestamp_type', 'datetime'),
            timestamp_left_decorator = config.get('timestamp_left_decorator', ''),
            timestamp_right_decorator = config.get('timestamp_right_decorator', ' | ')
        )
    
    def _reconfigure(self, config):
        """Reconfigures an existing Vane instance."""
        self.log_file = config.get('outfile', self.log_file)
        self.log_level = config.get('level', self.log_level)
        self.text_style = config.get('style', self.text_style)
        self.theme = config.get('theme', self.theme)
        self.timestamp_type = config.get('timestamp_type', self.timestamp_type)
        self.timestamp_left_decorator = config.get('timestamp_left_decorator', self.timestamp_left_decorator)
        self.timestamp_right_decorator = config.get('timestamp_right_decorator', self.timestamp_right_decorator)

        if self.log_file and (self._log_file_handle is None or self._log_file_handle.name != self.log_file):
            if self._log_file_handle:
                self._log_file_handle.close()
            try:
                self._log_file_handle = open(self.log_file, 'a', encoding='utf-8')
            except IOError as e:
                sys.stderr.write(f"ERROR: Could not open log file {self.log_file}: {e}\n")
                self._log_file_handle = None
        elif not self.log_file and self._log_file_handle:
            self._log_file_handle.close()
            self._log_file_handle = None

    def __init__(self, log_file=None, log_level="INFO", text_style=None, theme=None,
                 timestamp_type="datetime", timestamp_left_decorator="",
                 timestamp_right_decorator=" | "):
        """
        Private constructor. Use Vane.init() to configure or get the singleton instance.
        """
        if Vane.instance is not None and Vane.instance is not self:
            raise RuntimeError("Vane is a singleton. Use Vane.init() to configure or get the instance.")

        self.log_file = log_file
        self.log_level = log_level
        self.text_style = text_style
        self.theme = theme # Placeholder
        self.timestamp_type = timestamp_type
        self.timestamp_left_decorator = timestamp_left_decorator
        self.timestamp_right_decorator = timestamp_right_decorator
        
        self.log_count = 0

        self._log_file_handle = None
        if self.log_file:
            try:
                self._log_file_handle = open(self.log_file, 'a', encoding='utf-8')
            except IOError as e:
                sys.stderr.write(f"ERROR: Could not open log file {self.log_file}: {e}\n")
                self._log_file_handle = None


    def _should_log(self, level_str):
        """Check if current logging level is above or equal current log level."""
        levels = ["DEBUG", "INFO", "NOTE", "WARN", "ERROR", "CRITICAL", "ALERT", "EMERGENCY"]
        try:
            return levels.index(level_str.upper()) >= levels.index(self.log_level.upper())
        except ValueError:
            sys.stderr.write(f"WARNING: Unknown log level '{level_str}' or configured level '{self.log_level}'. Logging anyway.\n")
            return True


    def _log_message(self, message, level_str, include_level_formatting=True):
        """
        Internal method to handle message processing, formatting, and output.
        `include_level_formatting=False` for the plain `log()` method.
        """
        if include_level_formatting and not self._should_log(level_str):
            return ""
        
        if self.timestamp_type in ["log_number", "ln", 3, "verbose", "v", 4]:
            self.log_count += 1
        
        formatter_for_console = Message_Formatter(
            message=message,
            timestamp_type=self.timestamp_type,
            timestamp_left_decorator=self.timestamp_left_decorator,
            timestamp_right_decorator=self.timestamp_right_decorator,
            text_style_type=self.text_style,
            theme=self.theme
        )

        console_output_str = formatter_for_console.format_message(
            level_str=level_str,
            include_timestamp=True,
            include_level_name=include_level_formatting,
            apply_level_colors=include_level_formatting,
            apply_text_case_style=True,
            current_log_count=self.log_count
        )

        formatter_for_file = Message_Formatter(
            message=message,
            timestamp_type=self.timestamp_type,
            timestamp_left_decorator=self.timestamp_left_decorator,
            timestamp_right_decorator=self.timestamp_right_decorator,
            text_style_type=self.text_style,
            theme=None
        )

        file_output_str_raw = formatter_for_file.format_message(
            level_str=level_str,
            include_timestamp=True,
            include_level_name=include_level_formatting,
            apply_level_colors=False,
            apply_text_case_style=True,
            current_log_count=self.log_count
        )

        file_output_str_clean = re.sub(r'\x1b\[[0-9;]*m', '', file_output_str_raw)

        print(console_output_str)

        if self._log_file_handle:
            try:
                self._log_file_handle.write(f"{file_output_str_clean}\n")
                self._log_file_handle.flush()
            except Exception as e:
                sys.stderr.write(f"ERROR: Could not write to log file: {e}\n")
        
        return console_output_str
    
    # --- Public API for log levels ---
    def debug(self, message): return self._log_message(message, "DEBUG")
    def info(self, message): return self._log_message(message, "INFO")
    def warn(self, message): return self._log_message(message, "WARN")
    def note(self, message): return self._log_message(message, "NOTE")
    def error(self, message): return self._log_message(message, "ERROR")
    def critical(self, message): return self._log_message(message, "CRITICAL")
    def alert(self, message): return self._log_message(message, "ALERT")
    def emergency(self, message): return self._log_message(message, "EMERGENCY")

    def log(self, message):
        """
        Outputs the message without any level-specific formatting (no level name, no level colors).
        It still applies timestamp and the general text case style if configured for the Vane.
        """
        return self._log_message(message, "PLAIN", include_level_formatting=False)


    def close(self):
        """Closes the log file handle if open."""
        if self._log_file_handle:
            self._log_file_handle.close()
            self._log_file_handle = None


_initial_Vane_config = {
    'level': 'INFO',
    'timestamp_type': 'datetime',
    'timestamp_left_decorator': '[',
    'timestamp_right_decorator': ']: ',
    'style': None, # No text case style by default
    'outfile': None # No default file logging
}
Vane.init(_initial_Vane_config)

debug = functools.partial(Vane.instance.debug)
info = functools.partial(Vane.instance.info)
note = functools.partial(Vane.instance.note)
warn = functools.partial(Vane.instance.warn)
error = functools.partial(Vane.instance.error)
critical = functools.partial(Vane.instance.critical)
alert = functools.partial(Vane.instance.alert)
emergency = functools.partial(Vane.instance.emergency)
log = functools.partial(Vane.instance.log)

configure = Vane.init