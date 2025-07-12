from enum import StrEnum
import datetime
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)


class Message_Formatter:
    __VERSION__ = "0.2.0"
    def __init__(self, message,
                 timestamp_type="datetime", timestamp_left_decorator="",
                 timestamp_right_decorator=" |",
                 text_style_type=None,
                 theme=None,
                ):
        self.message = message
        self.timestamp_type = timestamp_type
        self.timestamp_left_decorator = timestamp_left_decorator
        self.timestamp_right_decorator = timestamp_right_decorator
        self.text_style_type = text_style_type
        self.theme = theme


    def _get_timestamp(self, current_log_count=None):
        """
        Generates a timestamp string based on the configured type.
        `current_log_count` is passed from the Vane instance if 'log_number' or 'verbose' is used.
        """
        now = datetime.datetime.now()
        timestamp_str = ""

        if self.timestamp_type in ["datetime", "dt", 1]:
            timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
        elif self.timestamp_type in ["runtime", "rt", 2]:
            timestamp_str = str(now.timestamp())
        elif self.timestamp_type in ["log_number", "ln", 3]:
            # Use the count provided by Vane, or fall back to internal if not provided
            timestamp_str = f"{current_log_count if current_log_count is not None else self._log_count_for_formatter + 1}"
            if current_log_count is None: # Only increment if using internal counter
                self._log_count_for_formatter += 1
        elif self.timestamp_type in ["verbose", "v", 4]:
            log_num_part = f"{current_log_count if current_log_count is not None else self._log_count_for_formatter + 1}"
            timestamp_str = f"{now.strftime('%Y-%m-%d %H:%M:%S')} | {now.timestamp()} | {log_num_part}"
            if current_log_count is None:
                self._log_count_for_formatter += 1
        elif self.timestamp_type in ["short", 5]:
            timestamp_str = now.strftime("%H:%M:%S")
        else:
            timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")

        if timestamp_str:
            return f"{self.timestamp_left_decorator}{timestamp_str}{self.timestamp_right_decorator}"
        return ""
    

    def _apply_text_case_style(self, text):
        """Applies text case formatting (uppercase, lowercase, capitalized)."""
        if self.text_style_type == "uppercase":
            return text.upper()
        elif self.text_style_type == "lowercase":
            return text.lower()
        elif self.text_style_type == "capitalized":
            return text.capitalize()
        else:
            return text # Return unchanged if no known style or style is None

    def _get_level_colours(self, level_code):
        level_map = {
            "EMERGENCY": f"{Style.BRIGHT}{Fore.WHITE}{Back.RED}",
            "ALERT": f"{Style.BRIGHT}{Fore.RED}",
            "CRITICAL": f"{Style.BRIGHT}{Fore.RED}",
            "ERROR": f"{Fore.RED}",
            "WARN": f"{Fore.YELLOW}",
            "NOTE": f"{Fore.BLUE}",
            "INFO": f"{Fore.GREEN}",
            "DEBUG": f"{Fore.CYAN}",
        }
        return level_map.get(level_code)

    
    def format_message(self, level_str, include_timestamp=True, include_level_name=True,
                       apply_level_colors=True, apply_text_case_style=True, current_log_count=None):
        """
        Constructs the final formatted log string.
        `current_log_count` is passed from the Vane instance for 'log_number' and 'verbose' timestamps.
        """
        final_parts = []
        if include_timestamp:
            final_parts.append(self._get_timestamp(current_log_count=current_log_count))

        if include_level_name:
            level_color = self._get_level_colours(level_str) if apply_level_colors else ""
            final_parts.append(f"[{level_color}{level_str.upper()}{Style.RESET_ALL}]")

        processed_message = self._apply_text_case_style(self.message) if apply_text_case_style else self.message
        if apply_level_colors:
            final_parts.append(f"{self._get_level_colours(level_str)}{processed_message}{Style.RESET_ALL}")
        else:
            final_parts.append(processed_message)
        
        return " ".join(part for part in final_parts if part).strip()
    
