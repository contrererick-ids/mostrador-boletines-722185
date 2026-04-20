# Práctica 4 - Comunicación entre contenedores
# Alumno: Erick Alejandro Contreras Salas
# Expediente: 722185
# Desarrollo en la Nube - Primavera 2026 ITESO

from fastapi import FastAPI, HTTPException, Query
from services.database.db import get_boletin, mark_as_read

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "¡Hola desde el contenedor de FastAPI!"}


@app.get("/boletines/{boletin_id}")
async def get_boletin_endpoint(boletin_id: str, correoElectronico: str = Query(...)):
    try:
        boletin_data = get_boletin(boletin_id, correoElectronico)
        if boletin_data:
            mark_as_read(boletin_id)
            return boletin_data
        else:
            raise HTTPException(status_code=404, detail="Boletín no encontrado")
    except Exception as e:
        return {"error": str(e)}
