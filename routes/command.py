from fastapi import APIRouter
from prisma import Prisma
import json
from pydantic import BaseModel
from datetime import datetime
router = APIRouter()

prisma = Prisma()

@router.on_event("startup")
async def startup():
    await prisma.connect()
@router.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


class Commands(BaseModel):
        id_command: int
        nom : str
        prix : float
        typeResto: str
        date:str
        heure:str
        status:int
        image:str


@router.get("/commandsByID")
async def commands(id_user:int):
    commands = await prisma.commande.find_many(       
        where={
            "id_user": id_user
        },
        include={
            "restaurant":{
                 "include" : {
                      "type_resto": True
                 }
            }
        }
    )

    

    comms = []
    for command in commands:
        totalw = await prisma.commandeitem.find_many(
        where={"id_commande": command.id_commande
               },
        include={
            "menu":True
        }
        )
        
        total = sum(total.menu.prix* total.quantite  for total in totalw)
        # Conversion de la chaîne en objet datetime
        datetime_obj = datetime.fromisoformat(str(command.date))
        date = datetime_obj.date()
        heure = datetime_obj.time()
        heure = heure.strftime("%H:%M")
        comms.append(Commands(id_command=command.id_commande, nom=command.restaurant.name, prix=total, typeResto=command.restaurant.type_resto.nom, date=str(date), heure=str(heure), status=command.valider, image=command.restaurant.image))

    # Tri des éléments en fonction de la date et de l'heure
    sorted_comms = sorted(comms, key=lambda x: (x.date, x.heure),reverse=True)

    return sorted_comms


class Command(BaseModel):
    id_resto:str
    id_user:str
    date: str
    total:str

@router.post("/newCommand")
async def newcommand(command: Command):
    dt = datetime.strptime(command.date, '%a %b %d %H:%M:%S GMT%z %Y')
    dt.strftime("%Y-%m-%d %H:%M:%S")
    dt = dt.isoformat()
    created = await prisma.commande.create(
        {
            "id_user": int(command.id_user),
            "id_resto": int(command.id_resto),
            "date": dt,
            "total": float(command.total),
            "valider": 0
        }
    )

    id_commande = await prisma.commande.find_first(
        where={
            "id_resto" : int(command.id_resto),
            "id_user": int(command.id_user),
            "date": dt
        }
    )
    return id_commande.id_commande


class CommandItems(BaseModel):
    id_command:str
    id_item:str
    quantite:str
@router.post("/newCommandItems")
async def newcommandItems(commandItem: CommandItems):
    created = await prisma.commandeitem.create(
        {
            "id_commande": int(commandItem.id_command),
            "id_item": int(commandItem.id_item),
            "quantite": float(commandItem.quantite),
        }
    )
    return {"creation" : "created successfully"}