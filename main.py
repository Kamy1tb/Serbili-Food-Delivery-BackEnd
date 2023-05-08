from fastapi import FastAPI
from prisma import Prisma


from routes.authentification import router as router_authentification
from routes.restaurants import router as router_restaurants


app = FastAPI()

prisma = Prisma()

app.include_router(router_authentification)
app.include_router(router_restaurants)



@app.get("/")
async def read_root():
    return {"Hello": "World"}



