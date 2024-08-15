from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# Conectar ao banco de dados PostgreSQL
def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname="test_db_cua7",
            user="guilherme",
            password="JUkHqaT8aWPzhLXLqZ1eKy3kYjqZm1LZ",
            host="dpg-cqtaqslds78s739io6ig-a.oregon-postgres.render.com",
            port="5432"
        )
        print("Conectado ao banco de dados.")
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados")

# Modelo de dados usando Pydantic
class SensorData(BaseModel):
    esp_id: str
    rfid: str
    peso: float
    preco: float
    nome: str

@app.post("/sensor_data/")
def insert_sensor_data(sensor_data: SensorData):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO sensor_data (esp_id, rfid, peso, preco, nome)
            VALUES (%(esp_id)s, %(rfid)s, %(peso)s, %(preco)s, %(nome)s)
        """, sensor_data.dict())
        connection.commit()
        return {"message": "Dados inseridos com sucesso"}
    except Exception as e:
        connection.rollback()
        print(f"Erro ao inserir dados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao inserir dados no banco de dados")
    finally:
        cursor.close()
        connection.close()

@app.get("/sensor_data/{sensor_id}")
def get_sensor_data(sensor_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM sensor_data WHERE id = %s", (sensor_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "esp_id": row[1],
                "rfid": row[2],
                "peso": row[3],
                "preco": row[4],
                "nome": row[5]
            }
        else:
            raise HTTPException(status_code=404, detail="Dados não encontrados")
    except Exception as e:
        print(f"Erro ao consultar dados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao consultar dados no banco de dados")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
