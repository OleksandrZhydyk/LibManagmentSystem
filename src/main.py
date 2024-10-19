from api import api_router
from fastapi import FastAPI
from fastapi_pagination import add_pagination


def get_application():
    application = FastAPI(title="DBB Software Task")
    application.include_router(api_router)
    add_pagination(application)
    return application


app = get_application()
