from fastapi import APIRouter
from app.service import weather
import os
api_key = os.getenv("WEATHER_API_KEY")

router = APIRouter(prefix='/weather', tags=[
    'Weather'
])


@router.get('/{city}')
async def getWeather(city: str):
    return await weather.getWeather(city)