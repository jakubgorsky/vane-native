# Vane
Tiny, customisable, modular and easy-to-use python logger.

## Getting started
To use Vane in your project simply import `log` method. This is as barebones as it gets. If you wish to add more log levels, configuration (like different timestamp types, logging to files, decorators, default logging level) import the necessary method.

### Logging methods

- debug
- info
- note
- warn
- error
- critical
- alert
- emergency

### Customisation options

`configure` method takes in a dictionary with a few options to define.

- outfile - specify a file to which Vane should log. By default it does not log anything into files.
- level - default level of logging. Vane will skip anything above certain level. For example, you may want to only log `notes` but discard `info` and `debug` if a parameter is not set in your application.
- timestamp_type - takes in predefined timestap types. Can be full name, short name or number. Defaults to datetime. Available timestamps are:
    - datetime (dt, 1) - YYYY-MM-DD HH:mm:SS format.
    - runtime (rt, 2) - runtime tampstamp.
    - log_number (ln, 3) - log number in current application run.
    - verbose (v, 4) - combines all above with `|` between each type
    - short (5) - simple HH:mm:SS format.
- timestamp_left_decorator - character to be put before timestamp. Can be any valid character. Defaults to `[`
- timestamp_right_decorator - character to be put after timestamp. Can be any valid character. Defaults to `]`
- style - changes the style of log message. Defaults sto none. Not yet implemented.
- theme - Not implemented yet. Ability to customise colours of messages.



