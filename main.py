from logger import Logger

Logger.init({
    "level": "DEBUG",
    "timestamp_type": "verbose"
})

Logger.instance.log("debug", "DEBUG", timestamp_type="dt")
Logger.instance.log("info", code="INFO", timestamp_type="rt")
Logger.instance.log("warning", code="WARNING", timestamp_type="ln")
Logger.instance.log("error", code="ERROR")
Logger.instance.log("critical", code="CRITICAL")
Logger.instance.log("fatal", code="FATAL")