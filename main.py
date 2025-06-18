#!/home/kubag/projects/.venv/bin/python3
from logger import debug, info, warn, note, error, critical, alert, emergency, log, configure

configure({
    'outfile': 'application.log',       # Log messages to this file
    'level': 'DEBUG',                   # Log all messages (DEBUG and higher)
    'timestamp_type': 'short',       # Use full datetime stamps
    'timestamp_left_decorator': '<',    # Add a '[' before the timestamp
    'timestamp_right_decorator': '>',   # Add a ']' after the timestamp
    'style': 'capitalized'              # Capitalize the first letter of each message
})

log("This is a plain, unformatted message. It will still get the timestamp and text case style.")

debug("Detailed information for developers. This only shows if level is DEBUG or lower.")
info("Application started successfully. We're good to go!")
note("Note. Nothing Fancy")
warn("Something might be off, but it's not critical yet.").upper
error("Uh oh! A significant error occurred, investigate immediately.")
critical("System failure imminent! Abort, abort!")
alert("just alerting.")
emergency("The system has crashed beyond recovery. This is the end.")