import io
from fastapi import APIRouter 
from fastapi import Depends 
from fastapi.responses import StreamingResponse
from fastapi import UploadFile, File
from service.sales_service import SalesService

from schemas.sale_schema import(
    SaleResponse
)

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)

def get_sales_service():
    try:
        return SalesService()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ...    


@router.get(
    path="/null_values",
    tags=["General"],
    description="Return null values for columns."
)
def get_list_null_values(service:SalesService = Depends(get_sales_service)):
    return service.list_null_values()

@router.get(
    path="/",
    response_model=list[SaleResponse], 
    tags=["Sales Filters"],
    description="Returns the complete list of all recorded sales."
)
def list_sales(service:SalesService = Depends(get_sales_service)): 
    return service.list_sales_json()


@router.get(
    path="/category/{category}",
    response_model=list[SaleResponse], 
    tags=["Sales Filters"],
    description="Return sales filter by category."
)
def list_sales_by_category(category:str, service:SalesService = Depends(get_sales_service)): 
    return service.get_sales_by_category(category)


@router.get(
    path="/city/{city}",
    response_model=list[SaleResponse], 
    tags=["Sales Filters"],
    description="Return sales filter by city."
)
def list_sales_by_city(city:str, service:SalesService = Depends(get_sales_service)): 
    return service.get_sales_by_city(city)


@router.get(
    path="/total_records", 
    tags=["General"],
    description="Return total records."
)
def get_total_records(service:SalesService = Depends(get_sales_service)): 
    return service.get_total_records()


@router.get(
    path="/statistics/total_invoicing", 
    tags=["Sales statistics"],
    description="Return total invoicing."
)
def get_total_invoicing(service: SalesService = Depends(get_sales_service)):
    return {"total_invoicing": service.get_total_invoicing()}


@router.get(
    path="/statistics/average_ticket", 
    tags=["Sales statistics"],
    description="Calculate the average value per customer in each commercial transaction."
)
def get_average_ticket(service: SalesService = Depends(get_sales_service)):
    return {"average_ticket": service.get_average_ticket()}


@router.get(
    path="/statistics/best_selling_product", 
    tags=["Sales statistics"],
    description="Return the best-selling product."
)
def get_best_selling_product(service: SalesService = Depends(get_sales_service)):
    return service.get_best_selling_product()


@router.get(
    path="/statistics/top_ten_products", 
    tags=["Sales statistics"],
    description="Returns the top 10 ranked products by quantity sold."
)
def get_top_ten_products(service: SalesService = Depends(get_sales_service)):
    return service.get_top_ten_products()


@router.get(
    path="/statistics/ranking_by_cities", 
    tags=["Sales statistics"],
    description="Returns the ranking of cities with the highest sales value."
)
def get_ranking_by_cities(service: SalesService = Depends(get_sales_service)):
    return service.get_ranking_city()


@router.get(
    path="/statistics/average_by_category", 
    tags=["Sales statistics"],
    description="Realiza um agrupamento estatístico para exibir a média financeira gerada por cada categoria de produto."
)
def get_average_by_category(service: SalesService = Depends(get_sales_service)):
    return service.get_average_category_invoicing()


@router.get(
    path="/statistics/sales_payment", 
    tags=["Sales statistics"],
    description="Returns the grouping of sales by payment method."
)
def get_sales_by_payment(service: SalesService = Depends(get_sales_service)):
    return service.get_sales_payment()

@router.get(
    path="/csv/export",
    tags=["General"],
    description="Gera dinamicamente e baixa o arquivo CSV contendo todos os dados e os cálculos consolidados (valor_total). "
)
def export_sales_csv(service: SalesService = Depends(get_sales_service)):
    data = service.get_export_csv()

    csv_bytes = data.encode("utf-8-sig")

    memory_file = io.BytesIO(csv_bytes)

    return StreamingResponse(
        content=memory_file,
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename={}"}
    )


@router.post(
    path="/csv/import",
    tags=["General"],
    description=""
)
def upload_sales_csv(file: UploadFile = File(..., description="Select the file .csv."),
                     service: SalesService = Depends(get_sales_service)):
    return service.upload_csv(file)