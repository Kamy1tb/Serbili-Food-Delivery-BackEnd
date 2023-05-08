from fastapi import APIRouter
from prisma import Prisma

router = APIRouter()

prisma = Prisma()


@router.on_event("startup")
async def startup():
    await prisma.connect()
@router.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()

    
@router.get("/restaurants")
async def read_restaurants():
    restaurants = await prisma.restaurant.find_many(include={
    "type_resto": True
    })
    return restaurants