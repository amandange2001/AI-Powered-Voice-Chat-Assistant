from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from route import router as visitor_router

# from telegram_webhook import router as telegram_router

app = FastAPI()

# ==========================================
# CORS CONFIGURATION
# ==========================================

origins = [

    "*",
    "http://192.168.1.25:5170"
    # Example:
    # "http://localhost:3000",
    # "http://127.0.0.1:3000",
]

app.add_middleware(

    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# ==========================================
# ROUTERS
# ==========================================

app.include_router(visitor_router)

# app.include_router(telegram_router)

# ==========================================
# ROOT API
# ==========================================

@app.get("/")

async def root():

    return {

        "message": "Visitor Management API Running"
    }