from datetime import datetime

class Sale:
    def __init__(
        self,
        id_venda: int,
        data: datetime,
        cliente: str,
        produto: str,
        categoria: str,
        quantidade: int,
        valor_unitario: float,
        cidade: str,
        estado: str,
        forma_pagamento: str
    ):
        self.__id_venda = id_venda
        self.__data = data
        self.__cliente = cliente
        self.__produto = produto
        self.__categoria = categoria
        self.__quantidade = quantidade
        self.__valor_unitario = valor_unitario
        self.__cidade = cidade
        self.__estado = estado
        self.__forma_pagamento = forma_pagamento

    @property
    def id_venda(self):
        return self.__id_venda

    @property
    def data(self): 
        return self.__data

    @property
    def cliente(self): 
        return self.__cliente

    @property
    def produto(self): 
        return self.__produto

    @property
    def categoria(self): 
        return self.__categoria

    @property
    def quantidade(self): 
        return self.__quantidade

    @property
    def valor_unitario(self): 
        return self.__valor_unitario

    @property
    def cidade(self): 
        return self.__cidade

    @property
    def estado(self): 
        return self.__estado

    @property
    def forma_pagamento(self): 
        return self.__forma_pagamento

    @property
    def valor_total(self):
        calc = self.__quantidade * self.__valor_unitario
        return round(calc, 2)
    
    def to_dict(self) -> dict:
        return {
            "id_venda": self.id_venda,
            "data": self.data,
            "cliente": self.cliente,
            "produto": self.produto,
            "categoria": self.categoria,
            "quantidade": self.quantidade,
            "valor_unitario": self.valor_unitario,
            "cidade": self.cidade,
            "estado": self.estado,
            "forma_pagamento": self.forma_pagamento,
            "valor_total": self.valor_total
        }    