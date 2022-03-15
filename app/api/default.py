import os
from fastapi import Request, APIRouter

from app.core.logging import get_logger, logrecord
from app.core.settings import log_settings


router = APIRouter()


@router.post('/')
async def get_logs(request: Request):
    """ LogWriter
        Преобразует endpoint в путь к папке с логами
            server.py/dev/app1
        Окончание endpoint-а будет преобразовано в имя файла
        В результате получится:
            /root_dir/dev/app1/app1.log
    """
    root = log_settings.ROOT
    path = request.url.path.strip('/')
    filename = path.split('/')[-1]

    log_path = f"{root}/{path}/{filename}.log"
    log_name = path.replace('/', '_')

    if not os.path.isfile(log_path):
        os.makedirs(f"{root}/{path}", exists_ok=True)

    file_logger = get_logger(log_name, log_path)
    request_body = await request.body()

    try:
        record = logrecord(request_body)
        file_logger.log(
            int(record.levelno),
            record.getMessage()
        )
        return {"status": "ok", "error": None, "data": request_body}

    except Exception as err:
        return {"status": "err", "error": err, "data": None}


@router.get('/healthcheck')
async def health():
    return {"status": "ok"}
