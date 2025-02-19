from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import matplotlib.pyplot as plt
import io
import base64
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()
# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CircleInput(BaseModel):
    radii: list[float]

from caja_anchomin import grafc 

@app.post("/api/calculate-circles")
async def calculate_circles(input: CircleInput):
    try:    
        image = grafc(input.radii)
        return image
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/healthz/")
def health_check_endpoint():
    return {"status": "ok"}
