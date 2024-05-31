from fastapi import FastAPI
from fastapi.responses import JSONResponse
from user.routes import router as guest_router, user_router
from auth.routes import router as auth_router
from pallet_detection.routes import router as pd_router
from core.security import JWTAuth
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/images", StaticFiles(directory="static"), name="images")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Routers
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(pd_router)

# Authentication middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

# Health check endpoint
@app.get('/')
def health_check():
    return JSONResponse(content={"status": "Running!"})
