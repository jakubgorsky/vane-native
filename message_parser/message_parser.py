def message_parser(message, code="INFO"):
    colour_codes = [
        {"FATAL": '\033[4;1;37;41m'},
        {"CRITICAL": '\033[1;31m'},
        {"ERROR": '\033[0;31m'},
        {"WARNING": '\033[0;33m'},
        {"INFO": '\033[0;37m'},
        {"DEBUG": '\033[0;34m'},
        {"ENDC": '\033[0m'}
    ]
    cc = None
    ec = list(colour_codes[6].values())[0]
    if code == "":
        return(str(message))
    if isinstance(code, str):
        match(code):
            case "FATAL":
                code = 0
            case "CRITICAL":
                code = 1
            case "ERROR":
                code = 2
            case "WARNING":
                code = 3
            case "INFO":
                code = 4
            case "DEBUG":
                code = 5
    if isinstance(code, int):
        if code > 5 or code < 0:
            return(str(message))
        cc = list(colour_codes[code].values())[0]
        prefix = "[" + list(colour_codes[code].keys())[0] + "]"
    return(cc + prefix + " " + str(message) + ec)