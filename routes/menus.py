from fastapi import APIRouter
from prisma import Prisma
from pydantic import BaseModel
router = APIRouter()

prisma = Prisma()

def addRating(restaurants,ratings):
    new_restaurant = []
    for restaurant in restaurants:
        new_restaurant["restaurant"] = restaurant
        new_restaurant["rating"] = 0
        for rating in ratings:
            if restaurant["id_resto"] == rating["id_restaurant"]:
                restaurant["rating"] = rating["_avg"]["rating"]
                break

    return new_restaurant


@router.on_event("startup")
async def startup():
    await prisma.connect()
@router.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


class Id_resto(BaseModel):
    id_resto:int
@router.get("/menuByID")
async def restaurantByID(id_resto:int):
    menu = await prisma.menu.find_many(    
        where={
            "id_restaurant": id_resto
        },    
        include={
    "type_menu": True,
    
    })
    return menu
