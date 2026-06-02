from pydantic import BaseModel

class SaleStatisticsResponse(BaseModel):
    faturamento_total: float
    ticket_medio: float
    total_vendas: float

    class Config:
        from_attributes = True