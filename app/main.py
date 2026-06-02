from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import customer , orders
 
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://h9jwsdktqe.ap-south-1.awsapprunner.com/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customer.router)
app.include_router(orders.router)