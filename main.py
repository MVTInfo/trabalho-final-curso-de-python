from fastapi import FastAPI

from controller.sales_controller import router as sales_router

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(sales_router)