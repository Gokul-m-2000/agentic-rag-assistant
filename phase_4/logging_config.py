from pathlib import Path
import logging
from request_context import request_id


class RequestIDFilter(logging.Filter):

    def filter(self, record):
        current_request_id = request_id.get()
        record.request_id = (
        current_request_id
        if current_request_id is not None
        else "-"
        )
        return True




def configure_logging():
    log_dir=Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file=log_dir/"app.log"

    formatter=logging.Formatter("%(asctime)s | %(levelname)s | request_id=%(request_id)s | %(name)s | %(message)s")


    root_logger=logging.getLogger()
    root_logger.setLevel(logging.INFO)

    has_console_handler=False
    has_file_handler=False

    #_app_handler_type_ has been dynamically added as an attribute so that we can identify the type of handler when checking existing handlers. This is useful to avoid adding duplicate handlers if configure_logging is called multiple times.

    for handler in root_logger.handlers:
        handler_type=getattr(handler,"_app_handler_type_",None)
        if handler_type=="console":
            has_console_handler=True
        elif handler_type=="file":
            has_file_handler=True

    request_id_filter=RequestIDFilter()

    if not has_console_handler:
        console_handler=logging.StreamHandler()
        console_handler._app_handler_type_="console"
        console_handler.setFormatter(formatter)
        console_handler.addFilter(request_id_filter)
        root_logger.addHandler(console_handler)

    if not has_file_handler:
        file_handler=logging.FileHandler(
            log_file,
            encoding="utf-8"
        )
        file_handler._app_handler_type_="file"
        file_handler.setFormatter(formatter)
        file_handler.addFilter(request_id_filter)
        root_logger.addHandler(file_handler)








    third_party_loggers = {
    "httpx": logging.WARNING,
    "httpcore": logging.WARNING,
    "faiss.loader": logging.WARNING,
    "google_genai.models": logging.WARNING,
    }

    for logger_name, level in third_party_loggers.items():
        logging.getLogger(logger_name).setLevel(level)


