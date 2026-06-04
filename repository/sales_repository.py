import pandas as pd
from model.sale import Sale
from utils.sales_utils import save_file_base_csv
from utils.sales_utils import get_file_name_csv
from utils.sales_utils import get_full_path_csv

class SalesRepository:
    def __init__(self) -> None:
        self._file_path = get_full_path_csv()
    
        self._load_file()

        print(self._file_path)

    def _load_file(self) -> bool:
        try:

            df_geral = pd.read_csv(self._file_path, sep=";", decimal=",")

            df_geral["data"] = pd.to_datetime(df_geral["data"], dayfirst=True, errors="coerce")
            df_geral["data"] = df_geral["data"].fillna(pd.Timestamp("2026-01-01 00:00:00"))
            df_geral["data"] = df_geral["data"].dt.strftime('%Y-%m-%dT%H:%M:%S')

            df_geral["valor_unitario"] = df_geral["valor_unitario"].astype(str).str.replace("R$", "", regex=False).str.strip()

            df_geral["quantidade"] = pd.to_numeric(df_geral["quantidade"], errors="coerce").fillna(0).astype(int)

            df_geral["valor_unitario"] = pd.to_numeric(df_geral["valor_unitario"], errors="coerce").fillna(0.0).astype(float)
            
            df_geral["valor_total"] = (df_geral["quantidade"] * df_geral["valor_unitario"]).round(2)

            self.__df = df_geral

            self._file_exists = True

            return True

        except FileNotFoundError:
            self._file_exists = False
            self.__df = pd.DataFrame()
            return False
        
        except Exception:
            self._file_exists = False
            self.__df = pd.DataFrame()
            return False            


    def check_base(self) -> bool:
        return self._file_exists


    def is_empty(self) -> bool:
        return self.__df.empty

    
    def get_dataframe(self):
        return self.__df
    
    def get_dataframe_null(self):
        return self.__df.isnull().sum().to_dict()


    def convert_objects(self, df: pd.DataFrame):
        list_sales = []
        
        for _, row in df.iterrows():
            sale = Sale(
                id_venda        =int(row["id_venda"]),
                data            =row["data"],
                cliente         =str(row["cliente"]),
                produto         =str(row["produto"]),
                categoria       =str(row["categoria"]),
                quantidade      =int(row["quantidade"]),
                valor_unitario  =float(row["valor_unitario"]),
                cidade          =str(row["cidade"]),
                estado          =str(row["estado"]),
                forma_pagamento =str(row["forma_pagamento"])
            )
            list_sales.append(sale.to_dict())

        return list_sales            


    def get_category(self,category) -> bool:
        exists = self.__df["categoria"].str.lower()

        return category.lower() in exists.values


    def get_city(self,city) -> bool:
        exists = self.__df["cidade"].str.lower()

        return city.lower() in exists.values
    

    def get_sales(self) -> list[Sale]:
        return self.convert_objects(self.__df)


    def sales_by_category(self, category: str) -> list[Sale]:
        df_filter = self.__df[self.__df["categoria"].str.lower() == category.lower()]
        return self.convert_objects(df_filter)


    def sales_by_city(self, city: str) -> list[Sale]:
        df_filter = self.__df[self.__df["cidade"].str.lower() == city.lower()]
        return self.convert_objects(df_filter)


    def total_records(self) -> int:
        if self.is_empty():
            return 0
       
        return len(self.__df)


    def calculate_total_invoicing(self) -> float:
        return round(float(self.__df["valor_total"].sum()),2)


    def average_ticket(self) -> float:
        return round(float(self.__df["valor_total"].mean()),2)


    def best_selling_product(self) -> dict:     
        df_prod = self.__df.groupby("produto", as_index=False).sum()
    
        df_top = df_prod.sort_values(by="quantidade", ascending=False).head(1)
        best_selling = df_top.to_dict(orient="records")[0]
    
        return {
            "product": best_selling["produto"], 
            "total_quatity": int(best_selling["quantidade"])
            }


    def category_more_profitable(self) -> dict:    
        df_cat = self.__df.groupby("categoria", as_index=False).sum()

        more_profitable = df_cat.sort_values(by="valor_total", ascending=False).head(1)

        return {
            "categoria": more_profitable["categoria"].values[0], 
            "faturamento_total": round(float(more_profitable["valor_total"].values[0]), 2)
            }
    

    def top_ten_products(self) -> list[dict]:
        ranking = self.__df.groupby("produto", as_index=False)[["quantidade"]].sum()
        
        ranking = ranking.sort_values(by="quantidade", ascending=False).head(10)
        
        return ranking.to_dict(orient="records")
    

    def ranking_city_invoicing(self) -> list[dict]:
        ranking = self.__df.groupby("cidade", as_index=False)[["valor_total"]].sum()
        
        ranking = ranking.sort_values(by="valor_total", ascending=False)
        
        return ranking.to_dict(orient="records")


    def average_category_invoicing(self) -> list[dict]:
        summary = self.__df.groupby("categoria", as_index=False).agg(faturamento_medio=("valor_total", "mean"))
        
        summary["faturamento_medio"] = round(summary["faturamento_medio"],2)
        
        return summary.to_dict(orient="records")


    def sales_payment(self) -> list[dict]:
        df_pagamento = self.__df["forma_pagamento"].value_counts().reset_index()

        df_pagamento.columns = ["forma_pagamento", "total_vendas"]

        return df_pagamento.to_dict(orient="records")
    
    def export_for_csv_string(self) -> str:
        if self.is_empty():
            return "id_venda;data;cliente;produto;categoria;quantidade;valor_unitario;cidade;estado;forma_pagamento;valor_total\n"
            
        return self.__df.to_csv(index=False, sep=";", encoding="utf-8-sig")    
    
    
    def update_base_data(self, file_bytes: bytes) -> bool:
        file_update_path = get_full_path_csv()
        
        if not save_file_base_csv(file_update_path, file_bytes):
            return False
            
        return self._load_file()
    

    def valid_dataframe(self,df_valid: pd.DataFrame) -> pd.DataFrame:

        if self.is_empty():
            raise ValueError("The uploaded file is empty.")

        required_columns = [
            "id_venda", "data", "cliente", "produto", "categoria", 
            "quantidade", "valor_unitario", "cidade", "estado", "forma_pagamento"
        ]
        
        missing_columns = [col for col in required_columns if col not in df_valid.columns]
        if missing_columns:
            raise ValueError(f"Invalid structure. Missing columns in CSV: {missing_columns}")

        df_clean = df_valid.copy()

        # Tratamento para cada coluna...
        df_clean["id_venda"] = df_clean["id_venda"].fillna("0").astype(str)

        df_clean["data"] = pd.to_datetime(df_clean["data"], dayfirst=True, errors="coerce")
        df_clean["data"] = df_clean["data"].fillna(pd.Timestamp("2026-01-01 00:00:00"))
        df_clean["data"] = df_clean["data"].dt.strftime('%Y-%m-%dT%H:%M:%S')

        df_clean["valor_unitario"] = (
            df_clean["valor_unitario"]
            .astype(str)
            .str.replace("R$", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.strip()
        )

        df_clean["quantidade"]      = pd.to_numeric(df_clean["quantidade"], errors="coerce").fillna(0).astype(int)
        df_clean["valor_unitario"]  = pd.to_numeric(df_clean["valor_unitario"], errors="coerce").fillna(0.0).astype(float)
        
        df_clean["cliente"]         = df_clean["cliente"].fillna("anonymous").astype(str).str.strip()
        df_clean["produto"]         = df_clean["produto"].fillna("product not specified").astype(str).str.strip()
        df_clean["categoria"]       = df_clean["categoria"].fillna("general").astype(str).str.strip()
        df_clean["cidade"]          = df_clean["cidade"].fillna("not specified").astype(str).str.strip()
        df_clean["estado"]          = df_clean["estado"].fillna("PR").astype(str).str.strip()
        df_clean["forma_pagamento"] = df_clean["forma_pagamento"].fillna("others").astype(str).str.strip()

        df_clean["valor_total"]     = (df_clean["quantidade"] * df_clean["valor_unitario"]).round(2)

        return df_clean