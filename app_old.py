from fastapi import FastAPI, Request, APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional

# Создание базового FastAPI приложения
app = FastAPI()

# Инициализация шаблонов Jinja2
templates = Jinja2Templates(directory="templates")

# Модель Pydantic для сущности "Автомобиль"
class Car(BaseModel):
    id: int
    name: str
    year: Optional[int] = None
    color: Optional[str] = None

# Пример базы данных (временное хранилище)
cars_db = [
    Car(id=1, name="Toyota Camry", year=2020, color="Black"),
    Car(id=2, name="Honda Accord", year=2019, color="White"),
    Car(id=3, name="Ford Mustang", year=2021, color="Red"),
]

# Обычные представления (views)
@app.get("/")
def index(request: Request):
    """
    Главная страница.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about/")
def about(request: Request):
    """
    Страница "О сайте".
    """
    return templates.TemplateResponse("about.html", {"request": request})

# Создание API роутера
api_router = APIRouter(prefix="/api")

# Вложенный роутер для сущности "автомобиль"
@api_router.get("/cars/", response_model=List[Car])
def get_cars():
    """
    Получение списка всех автомобилей.
    """
    return cars_db

@api_router.get("/cars/{car_id}", response_model=Car)
def get_car(car_id: int):
    """
    Получение информации о конкретном автомобиле по его ID.
    """
    car = next((car for car in cars_db if car.id == car_id), None)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@api_router.post("/cars/", response_model=Car)
def create_car(car: Car):
    """
    Создание нового автомобиля.
    """
    cars_db.append(car)
    return car

@api_router.put("/cars/{car_id}", response_model=Car)
def update_car(car_id: int, updated_car: Car):
    """
    Обновление информации об автомобиле по его ID.
    """
    car_index = next((index for index, car in enumerate(cars_db) if car.id == car_id), None)
    if car_index is None:
        raise HTTPException(status_code=404, detail="Car not found")
    cars_db[car_index] = updated_car
    return updated_car

@api_router.delete("/cars/{car_id}", response_model=Car)
def delete_car(car_id: int):
    """
    Удаление автомобиля по его ID.
    """
    car_index = next((index for index, car in enumerate(cars_db) if car.id == car_id), None)
    if car_index is None:
        raise HTTPException(status_code=404, detail="Car not found")
    deleted_car = cars_db.pop(car_index)
    return deleted_car

# Подключение API роутера к приложению
app.include_router(api_router)