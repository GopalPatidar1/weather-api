from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
load_dotenv()
from app.api.routes import weather

app = FastAPI()

@app.middleware("http")
async def auth_and_cors(request, call_next):
    public_routes = [
        '/docs',
        '/openapi.json',
        '/redoc',
        '/health'
    ]

    if request.url.path not in public_routes:
        auth_header = request.headers.get("Authorization")
        if auth_header == None:
            return JSONResponse(
                status_code=401,
                content={
                    'detail': 'Invalid or missing token'
                },
            )
            # raise HTTPException(status_code=401, detail="Unauthorized") #commented this line because it was causing an error when the Authorization header was missing. The JSONResponse above handles the response instead.

    response = await call_next(request)
    return response

app.include_router(weather.router)

@app.get('/health')
def read_root():
    return {
        'message': 'Welcome to the weather api!'
    }