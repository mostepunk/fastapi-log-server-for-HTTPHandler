import logging
import urllib.parse
from logging.handlers import TimedRotatingFileHandler

from app.core.settings import app_settings, log_settings as ls

LOGGING_LEVEL = logging.NOTSET


def get_logger(log_name: str, log_path: str) -> logging.Logger:
    """ Возвращает объект логгер названный точно так же как и принимаемый путь
        dev/app1 -> dev_app1
    """
    logger = logging.getLogger(log_name)
    logger.setLevel(LOGGING_LEVEL)
    log_file_format = app_settings.LOG_FORMAT

    if not logger.hasHandlers():
        # Каждый раз, когда приходит сообщение на логгер навешивается новый экземпляр хэндлера,
        # И каждый хэндлер делает запись в журнале и появляются дубли
        # Чтобы этого не происходило, вставил эту проверку
        fh = TimedRotatingFileHandler(
            log_path,
            when=ls.WHEN,
            interval=ls.INTERVAL,
            backupCount=ls.BACKUP_COUNT,
            atTime=ls.AT_TIME
        )
        fh.setFormatter(logging.Formatter(log_file_format))

        logger.addHandler(fh)

    return logger


def logrecord(request_body: bytes) -> logging.LogRecord:
    """ Принимает тело запроса в байтах
        И преобразует его в LogRecord
        Приходит он в url кодировке
        Это будет работать только если установлен стандартный logging.handlers.HTTPHandler

        Пример входящего сообщения:
            {
                'name': 'main',
                'msg': 'Answer code: 401 request url: GET "http://127.0.0.1:8000/api/v1/user" duration: 74 ms Request body: b\'\' Response body: b\'{"message":"Token expired"}\' ',
                'args': '()',
                'levelname': 'INFO',
                'levelno': '20',
                'pathname': '/app/./app/core/middlewares/logging_middleware.py',
                'filename': 'logging_middleware.py',
                'module': 'logging_middleware',
                'exc_info': 'None',
                'exc_text': 'None',
                'stack_info': 'None',
                'lineno': '155',
                'funcName': '__call__',
                'created': '1647248729.8843582',
                'msecs': '884.3581676483154',
                'relativeCreated': '3603232.8238487244',
                'thread': '140245387786048',
                'threadName': 'MainThread',
                'processName': 'SpawnProcess-2',
                'process': '28'
            }
    """
    assert isinstance(request_body, bytes), 'Request body should be in bytes'
    logrec = urllib.parse.unquote(request_body.decode())

    # name=main&process=28...
    log_dict = dict(
        (x.split('=')[0], (x.split('=')[1]))
        for x in logrec.split('&')
    )
    # Заменить + на пробел
    log_dict['msg'] = urllib.parse.unquote_plus(log_dict['msg'])
    log_dict['level'] = log_dict['levelno']

    # Если приходят '()' в параметре args, падает в ошибку
    if log_dict.get('args') == '()':
        log_dict['args'] = ''

    rec = record_factory(**log_dict)
    return rec


def record_factory(*args, **kwargs) -> logging.Logger:
    factory = logging.getLogRecordFactory()
    record = factory(*args, **kwargs)
    return record
