import pytest
from vane.message_formatter.message_formatter import Message_Formatter
from colorama import Fore, Back, Style
import datetime
from unittest.mock import patch

# Helper to strip ANSI codes for comparison if needed (though formatter should include them)
def strip_ansi(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', text)


def test_formatter_basic_info():
    formatter = Message_Formatter("Hello World")
    expected = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | [{Fore.GREEN}INFO{Style.RESET_ALL}] {Fore.GREEN}Hello World{Style.RESET_ALL}"
    with patch('datetime.datetime') as mock_dt:
        fixed_time = datetime.datetime(2025, 6, 18, 10, 0, 0)
        mock_dt.now.return_value = fixed_time
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
        
        formatter_instance = Message_Formatter("Hello World")
        expected_time_str = fixed_time.strftime("%Y-%m-%d %H:%M:%S")
        expected = f"{expected_time_str} | [{Fore.GREEN}INFO{Style.RESET_ALL}] {Fore.GREEN}Hello World{Style.RESET_ALL}"
        assert formatter_instance.format_message("INFO") == expected


def test_formatter_custom_timestamp_and_decorators():
    formatter = Message_Formatter(
        "Custom message",
        timestamp_type='short',
        timestamp_left_decorator='<',
        timestamp_right_decorator='>'
    )
    with patch('datetime.datetime') as mock_dt:
        fixed_time = datetime.datetime(2025, 6, 18, 10, 30, 45)
        mock_dt.now.return_value = fixed_time
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
        
        expected_timestamp = fixed_time.strftime("%H:%M:%S")
        expected_output = f"<{expected_timestamp}> [{Fore.CYAN}DEBUG{Style.RESET_ALL}] {Fore.CYAN}Custom message{Style.RESET_ALL}"
        assert formatter.format_message("DEBUG") == expected_output


def test_formatter_text_styles():
    formatter_upper = Message_Formatter("test message", text_style_type='uppercase')
    with patch('datetime.datetime') as mock_dt:
        fixed_time = datetime.datetime(2025, 6, 18, 10, 0, 0)
        mock_dt.now.return_value = fixed_time
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
        expected_time_str = fixed_time.strftime("%Y-%m-%d %H:%M:%S")
        expected = f"{expected_time_str} | [{Fore.RED}ERROR{Style.RESET_ALL}] {Fore.RED}TEST MESSAGE{Style.RESET_ALL}"
        assert formatter_upper.format_message("ERROR") == expected

    formatter_cap = Message_Formatter("another test", text_style_type='capitalized')
    with patch('datetime.datetime') as mock_dt: 
        fixed_time = datetime.datetime(2025, 6, 18, 10, 0, 0)
        mock_dt.now.return_value = fixed_time
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
        expected_time_str = fixed_time.strftime("%Y-%m-%d %H:%M:%S")
        expected = f"{expected_time_str} | [{Fore.YELLOW}WARN{Style.RESET_ALL}] {Fore.YELLOW}Another test{Style.RESET_ALL}"
        assert formatter_cap.format_message("WARN") == expected

def test_formatter_log_number_timestamp():
    formatter = Message_Formatter("Counted message", timestamp_type='log_number')
    # Note: current_log_count must be passed from Logger for accuracy.
    # Here, we simulate it directly.
    expected = f"1 | [{Fore.GREEN}INFO{Style.RESET_ALL}] {Fore.GREEN}Counted message{Style.RESET_ALL}"
    assert formatter.format_message("INFO", current_log_count=1) == expected

    expected2 = f"5 | [{Fore.CYAN}DEBUG{Style.RESET_ALL}] {Fore.CYAN}Another counted message{Style.RESET_ALL}"
    formatter2 = Message_Formatter("Another counted message", timestamp_type='log_number')
    assert formatter2.format_message("DEBUG", current_log_count=5) == expected2


def test_formatter_plain_message():
    # Test the 'log' equivalent where level name and colors are suppressed
    formatter = Message_Formatter("Plain content here", timestamp_type='short')
    with patch('datetime.datetime') as mock_dt:
        fixed_time = datetime.datetime(2025, 6, 18, 10, 30, 45)
        mock_dt.now.return_value = fixed_time
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
        
        expected_timestamp = fixed_time.strftime("%H:%M:%S") # Default right decorator used
        # No level name, no level colors applied to the message itself
        expected_output = f"{expected_timestamp} | Plain content here"
        
        assert formatter.format_message(
            "ANY_LEVEL", # Level string still needed for _get_level_colors, but not displayed
            include_level_name=False,
            apply_level_colors=False # Explicitly disable
        ) == expected_output

# Add more tests covering all timestamp types, level colors, combinations, etc.