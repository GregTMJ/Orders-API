import datetime
import logging
import os

# Формат название файлов логирования.
file_name_format = "{year:04d}{month:02d}{day:02d}.log"

# Формат логирования.
file_msg_format = "%(asctime)s %(levelname)-8s: %(message)s"
console_msg_format = "%(levelname)s: %(message)s"

# Максимальное кол-во байтов для каждого файла.
max_bytes = 1024**2  # ~ 1MB
backup_count = 100


class ColoredFormatter(logging.Formatter):
    COLOR_CODES = {
        "DEBUG": "\033[94m",  # синий
        "INFO": "\033[92m",  # зелёный
        "WARNING": "\033[93m",  # жёлтый
        "ERROR": "\033[91m",  # красный
        "CRITICAL": "\033[41m\033[97m",  # красный фон с белым текстом
    }
    RESET_CODE = "\033[0m"

    def format(self, record):
        color = self.COLOR_CODES.get(record.levelname, "")
        formatted_message = f"{color}{super().format(record)}{self.RESET_CODE}"
        return formatted_message


def init_logger(init_dir="log", file_level=logging.DEBUG, stream_level=logging.INFO):
    """Функция инициализации логгера."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    init_dir = os.path.normpath(init_dir)

    if not os.path.exists(init_dir):
        os.makedirs(init_dir)

    t = datetime.datetime.now()
    file_name = file_name_format.format(
        year=t.year,
        month=t.month,
        day=t.day,
    )
    file_name = os.path.join(init_dir, file_name)

    file_handler = logging.handlers.RotatingFileHandler(
        filename=file_name, maxBytes=max_bytes, backupCount=backup_count
    )
    file_handler.setLevel(file_level)
    file_formatter = logging.Formatter(file_msg_format)
    file_handler.setFormatter(file_formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(stream_level)
    stream_formatter = ColoredFormatter(console_msg_format)
    stream_handler.setFormatter(stream_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return


logger = logging.getLogger()
