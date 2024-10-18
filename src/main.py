from api import api_router
from fastapi import FastAPI
from fastapi_pagination import add_pagination

app = FastAPI(title="DBB Software Task")
app.include_router(api_router)
add_pagination(app)
