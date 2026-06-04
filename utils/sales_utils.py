import os
from dotenv import load_dotenv

load_dotenv(override=True)

def save_file_base_csv(full_path: str, bytes_content: bytes) -> bool:
    try:

        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, "wb") as f:
            f.write(bytes_content)
            
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False
    

def get_full_path_csv() -> str:
    path = os.getenv("DATABASE_PATH", "./data")
    file_name = os.getenv("DATABASE_FILE_NAME", "sales_base.csv")

    return os.path.join(path,file_name)


def get_file_name_csv() -> str:

    return os.getenv("DATABASE_FILE_NAME", "sales_base.csv")