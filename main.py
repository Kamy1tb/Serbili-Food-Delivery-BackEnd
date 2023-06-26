from fastapi import FastAPI
from prisma import Prisma
import uvicorn

from routes.authentification import router as router_authentification
from routes.restaurants import router as router_restaurants
from routes.menus import router as router_menus
from routes.command import router as router_command


app = FastAPI()

prisma = Prisma()

app.include_router(router_authentification)
app.include_router(router_restaurants)
app.include_router(router_menus)
app.include_router(router_command)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


