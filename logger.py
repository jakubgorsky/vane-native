from message_parser.message_parser import message_parser
from datetime import datetime

class Logger:
    instance = None

    @classmethod
    def init(cls, config):
        cls.instance = cls(
            log_file = config.get('outfile', None),
            log_level = config.get('level', 'INFO'),
            style = config.get('style', None),
            theme = config.get('theme', None),
            timestamp_type = config.get('timestamp_type', 'datetime')
        )

    # Functionality to be implemented: logging to files, different themes.
    def __init__(self, log_file=None, log_level="INFO", style=None,theme=None, timestamp_type="datetime"):
        """Initialize the logger.
        By default, log level is set to info."""
        self.log_file = log_file
        self.log_level = log_level
        self.theme = theme
        self.style = style
        self.log_count = 0
        self.timestamp_type = timestamp_type


    def _should_log(self, level):
        """Check if current logging level is above or equal current log level.\n
        For example, if current level is set to INFO, by default do not log DEBUG events."""
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "FATAL"]
        return levels.index(level) >= levels.index(self.log_level)


    def _get_timestamp(self, timestamp_type):
        """Get current timestamp. Supportted types are:\n
        datetime - datetime, dt or 1,\n
        runtime - runtime, rt or 2,\n
        log number - log_number, ln or 3,\n
        verbose - verbose, v or 4\n
        By default prints out in datetime setting."""
        now = datetime.now()
        if timestamp_type == "datetime" or timestamp_type == "dt" or timestamp_type == 1:
            return now.strftime("%Y-%m-%d %H:%M:%S") + " | "

        elif timestamp_type == "runtime" or timestamp_type == "rt" or timestamp_type == 2:
            return str(now.timestamp()) + " | "

        elif timestamp_type == "log_number" or timestamp_type == "ln" or timestamp_type == 3:
            self.log_count += 1
            return f"{self.log_count}" + " | "

        elif timestamp_type == "verbose" or timestamp_type == "v" or timestamp_type == 4:
            self.log_count += 1
            return now.strftime("%Y-%m-%d %H:%M:%S") + " | " + str(now.timestamp()) + " | " + f"{self.log_count}" + " | "

        else:
            return now.strftime("%Y-%m-%d %H:%M:%S") + " | "


    def _apply_style(self, message, style):
        """Returns message in certain style. Supports three styles:\n
        uppercase, lowercase, capitalized\n
        If no style specified, passes on message unchanged."""
        if style == "uppercase":
            return message.upper()
        elif style == "lowercase":
            return message.lower()
        elif style == "capitalized":
            return message.capitalize()
        else:
            return message

    def log(self, message, code="", timestamp_type=None, style=None):
        if not self._should_log(code or self.log_level):
            return

        timestamp = self._get_timestamp(timestamp_type or self.timestamp_type)
        message = self._apply_style(message, style or self.style)
        log_level = code or self.log_level
        formatted_message = message_parser(f"{timestamp} {message}", code=log_level)
        print(formatted_message)