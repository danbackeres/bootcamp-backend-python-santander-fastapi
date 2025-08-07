from fastapi import APIRouter, status, Body

from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.atleta.schemas import AtletaIn

api_router = APIRouter()

@api_router.post('/', summary="Cadastrar atleta", status_code=status.HTTP_201_CREATED)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):
    pass