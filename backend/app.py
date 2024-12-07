from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.controllers import auth_controller, movie_controller


origins = ["*"]
methods = ["*"]
headers = ["*"]

app = FastAPI()

app.include_router(movie_controller.router)
app.include_router(auth_controller.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=methods,
    allow_headers=headers,
    allow_credentials=True,
)
