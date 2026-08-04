from fastapi import APIRouter
import os

api_key = os.getenv("WEATHER_API_KEY")
print("🚀 ~ api_key:", api_key)

router = APIRouter(prefix='/weather', tags=[
    'Weather'
])


@router.get('/')
def getWeather():
    return {
        'message': 'Welcome to the weather api!'
    }   