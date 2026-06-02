from repository.sales_repository import SalesRepository
from fastapi import HTTPException
from fastapi import UploadFile
from model.sale_model import Sale

class SalesService:
    def __init__(self):
        self._repo = SalesRepository()

    def _valid_base(self) -> SalesRepository:
        if not self._repo.check_base():
            raise HTTPException(
                status_code=500,
                detail="Internal Error: The data file was not found."
            )
        
        if self._repo.is_empty():
            raise HTTPException(
                status_code=404,
                detail="The sales database is empty."
            )
            
        return self._repo


    def list_sales_json(self) -> list[Sale]:
        return self._valid_base().get_sales()
    
    def list_null_values(self):
        return self._valid_base().get_dataframe_null()


    def get_sales_by_category(self, category) -> list[Sale]:
        valid_field = category.strip()
        if not valid_field:
            raise HTTPException(
                status_code=400, 
                detail="The field cannot be empty."
            )

        if not self._valid_base().get_category(valid_field):
            raise HTTPException(
                status_code=404,
                detail=f"Category >> {valid_field} << not found."
            )
        
        return self._valid_base().sales_by_category(valid_field)


    def get_sales_by_city(self, city) -> list[Sale]:
        valid_field = city.strip()
        if not valid_field:
            raise HTTPException(
                status_code=400, 
                detail="The field cannot be empty."
            )

        if not self._valid_base().get_city(valid_field):
            raise HTTPException(
                status_code=404,
                detail=f"City >> {valid_field} << not found."
            )
        
        return self._valid_base().sales_by_city(valid_field)
    

    def get_total_records(self):
        records = self._valid_base().total_records()
        
        return {"Total records": {records}}


    def get_total_invoicing(self) -> float:
        
        return self._valid_base().calculate_total_invoicing()
    
    def get_average_ticket(self) -> float:
        value = self._valid_base().average_ticket()

        return round(value,2)


    def get_best_selling_product(self) -> dict:

        return self._valid_base().best_selling_product()
    

    def get_category_more_profitable(self) -> dict:

        return self._valid_base().category_more_profitable()


    def get_top_ten_products(self) -> list[dict]:
        
        return self._valid_base().top_ten_products()
    

    def get_ranking_city(self) -> list[dict]:
        
        return self._valid_base().ranking_city_invoicing()


    def get_average_category_invoicing(self) -> list[dict]:
        
        return self._valid_base().average_category_invoicing()


    def get_sales_payment(self) -> list[dict]:
        
        return self._valid_base().sales_payment()
    
    def get_export_csv(self) -> str:
        if not self._valid_base():
            raise HTTPException(
                status_code=500,
                detail="Internal Error: Data cannot be exported because the original database has disappeared."
            )
        
        return self._repo.export_for_csv_string()
    
    
    def upload_csv(self, filedata: UploadFile) -> dict:
        if not filedata.filename or not filedata.filename.endswith('.csv'):
            raise HTTPException(
                status_code=400, 
                detail="Invalid format. I only accept files with the extension (*.csv)."
            )
            
        try:
            content_bytes = filedata.file.read()
            
            success_data = self._repo.update_base_data(content_bytes)
            
            if not success_data:
                raise HTTPException(
                    status_code=422,
                    detail="Error processing data. Please check the correct CSV structure."
                )
                
            return {
                "message": f"File '{filedata.filename}' save success!",
                "total records updated": self._repo.total_records()
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Critical error, unprocessed file: {e}")
        finally:
            filedata.file.close()