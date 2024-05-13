from fastapi import FastAPI
from fastapi.responses import JSONResponse
from user.routes import router as guest_router, user_router
from auth.routes import router as auth_router
from pallet_detection.routes import router as pd_router
from core.security import JWTAuth
from starlette.middleware.authentication import AuthenticationMiddleware

app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(pd_router)

# Add Middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())


@app.get('/')
def health_check():
    return JSONResponse(content={"status": "Running!"})
