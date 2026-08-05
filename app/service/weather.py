from app.config import redis
from fastapi import HTTPException
import os
import httpx
import json

WEATHER_API_URL = os.getenv("WEATHER_API_URL")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

redisClient = redis.redis_client

httpClient = httpx.AsyncClient()

async def getWeather(city: str = 'Dewas, MP, India'):
    try:
        cacheKey = f"weather:{city.strip().lower()}"
        raw_data = redisClient.get(cacheKey)
        if raw_data:
          return {"result": json.loads(raw_data)}
        
        request_url = f"{WEATHER_API_URL}/{city}?key={WEATHER_API_KEY}&contentType=json&unitGroup=us&include=day"
        response = await httpClient.get(request_url)
        response.raise_for_status()
        data = response.json()
        redisClient.set(cacheKey, json.dumps(data), ex=60) 
        return {"result": data}
    except httpx.RequestError as e:
        print(f"An error occurred while requesting weather data: {e}")
        raise HTTPException(
            status_code=e.response.status_code or 500,
            detail='Failed to fetch weather data.'
        )
    except Exception as e:
        raise HTTPException(
             status_code= e.response.status_code if hasattr(e, "response") and e.response else 500,
            detail=str(e) or 'Exception occurred while processing weather data.'
        )
    