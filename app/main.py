import uvicorn
from fastapi import FastAPI

from app.core.settings import app_settings
from app.api.router import dev, prod


def get_application() -> FastAPI:
    application = FastAPI(
        title=app_settings.PROJECT_NAME,
        debug=app_settings.DEBUG,
        version=app_settings.VERSION,
        docs_url=app_settings.DOCS,
        redoc_url=app_settings.REDOC,
    )

    application.include_router(router=prod, prefix=app_settings.PREFIX_PROD)
    application.include_router(router=dev, prefix=app_settings.PREFIX_DEV)

    return application


app = get_application()


@app.get('/')
async def root():
    """ Main Root route
    """
    return {'message': 'I am Root'}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=app_settings.HOST,
        port=app_settings.PORT,
    )
