from logger.message_parser.message_parser import message_parser

def test_regular():
    assert message_parser("regular") == "regular"

def test_fatal():
    assert message_parser("fatal", 0) == "\x1b[4;1;37;41m[FATAL] fatal\x1b[0m"

def test_critical():
    assert message_parser("critical", 1) == "\x1b[1;31m[CRITICAL] critical\x1b[0m"

def test_error():
    assert message_parser("error", 2) == "\x1b[0;31m[ERROR] error\x1b[0m"

def test_warning():
    assert message_parser("warning", 3) == "\x1b[0;33m[WARNING] warning\x1b[0m"

def test_info():
    assert message_parser("info", 4) == "\x1b[0;37m[INFO] info\x1b[0m"

def test_debug():
    assert message_parser("debug", 5) == "\x1b[0;34m[DEBUG] debug\x1b[0m"