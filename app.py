from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates



app = FastAPI()

templates = Jinja2Templates(directory="templates")

"""Роуты для обычных представлений"""
@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about/")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})



router = APIRouter(prefix="/api")

"""Модель данных для автомобиля"""
class Car(BaseModel):
    id: int
    make: str
    model: str
    year: int
    price: float

"""Переменная для хранения данных"""
garage_db = [
    Car(id=1, make="Toyota", model="Camry", year=2020, price=25000),
    Car(id=2, make="BMW", model="X5", year=2019, price=45000),
]

"""Получение списка автомобилей"""
@router.get("/cars/", response_model=List[dict])
def get_cars():
    return [car.dict() for car in garage_db]

"""Получение данных конкретного автомобиля"""
@router.get("/cars/{car_id}", response_model=dict)
def get_car(car_id: int):
    car = next((c for c in garage_db if c.id == car_id), None)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car.dict()

"""Создание нового автомобиля"""
@router.post("/cars/", response_model=dict)
def create_car(car: Car):
    # Проверка на уникальность id
    if any(c.id == car.id for c in garage_db):
        raise HTTPException(status_code=400, detail="Car with this id already exists")
    garage_db.append(car)
    return car.dict()

"""Обновление существующего автомобиля"""
@router.put("/cars/{car_id}", response_model=dict)
def update_car(car_id: int, updated_car: Car):
    for i, car in enumerate(garage_db):
        if car.id == car_id:
            garage_db[i] = updated_car
            return updated_car.dict()
    raise HTTPException(status_code=404, detail="Car not found")

"""Удаление автомобиля"""
@router.delete("/cars/{car_id}")
def delete_car(car_id: int):
    for i, car in enumerate(garage_db):
        if car.id == car_id:
            del garage_db[i]
            return {"detail": "Car deleted"}
    raise HTTPException(status_code=404, detail="Car not found")

app.include_router(router )

