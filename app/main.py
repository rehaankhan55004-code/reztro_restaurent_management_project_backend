from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import customer , orders ,menu ,menu_category
 
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://h9jwsdktqe.ap-south-1.awsapprunner.com/"
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customer.router)
app.include_router(orders.router)
app.include_router(menu.router)
app.include_router(menu_category.router)