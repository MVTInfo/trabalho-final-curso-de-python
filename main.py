from fastapi import FastAPI

from controller.sales_controller import router as sales_router

app = FastAPI()

app.include_router(sales_router)