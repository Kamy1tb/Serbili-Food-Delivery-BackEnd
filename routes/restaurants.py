from fastapi import APIRouter
from prisma import Prisma

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

    
@router.get("/restaurants")
async def read_restaurants():
    restaurants = await prisma.restaurant.find_many(       
        include={
    "type_resto": True,
    })

    return restaurants

@router.get("/restaurantByID")
async def restaurantByID(id_resto:int):
    restaurants = await prisma.restaurant.find_first(    
        where={
            "id_resto": id_resto
        },    
        include={
    "type_resto": True,
    "rating_restaurant": True
    })
    return restaurants

@router.get("/ratingRestaurants")
async def rating_restaurants():
    ratings = await prisma.rating_restaurant.group_by(
        by= ["id_restaurant"],
        avg={
            "rating":True
        },
    )
    return ratings