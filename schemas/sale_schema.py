from pydantic import BaseModel
from datetime import datetime

class SaleResponse(BaseModel):
    id_venda: int
    data: datetime
    cliente: str
    produto: str
    categoria: str
    quantidade: int
    valor_unitario: float
    valor_total: float
    cidade: str
    estado: str
    forma_pagamento: str

    class Config:
        from_attributes = True