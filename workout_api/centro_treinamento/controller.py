from http.client import HTTPException
from uuid import uuid4

from pydantic import UUID4
from fastapi import APIRouter, status, Body

from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel

from sqlalchemy import select

api_router = APIRouter()

@api_router.post('/', summary="Cadastrar um novo Centro de Treinamento", status_code=status.HTTP_201_CREATED, response_model=CentroTreinamentoOut)
async def post(db_session: DatabaseDependency, centro_treinamento_in: CentroTreinamentoIn = Body(...)) -> CentroTreinamentoOut:
    
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_in.model_dump())
    db_session.add(centro_treinamento_model)
    await db_session.commit()
    
    return centro_treinamento_out

@api_router.get('/', summary="Consultar todas os Centro de Treinamento", status_code=status.HTTP_200_OK, response_model=list[CentroTreinamentoOut])
async def query(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centros_treinamento: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    
    return centros_treinamento

@api_router.get('/{id}', summary="Consultar centro de treinamento pelo id", status_code=status.HTTP_200_OK, response_model=CentroTreinamentoOut)
async def query(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_trreinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
    
    if not centro_trreinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Centro de treinamento não encontrado")
    
    return centro_trreinamento