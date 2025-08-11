from datetime import datetime
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, status, Body, Query, HTTPException
from fastapi_pagination import Page, paginate, add_pagination

from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.atleta.schemas import AtletaIn, AtletaListOut, AtletaOut, AtletaUpdate
from workout_api.atleta.models import AtletaModel

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

api_router = APIRouter()

@api_router.post('/', summary="Cadastrar atleta", status_code=status.HTTP_201_CREATED, response_model=AtletaOut)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)): # type: ignore
    
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))).scalars().first()
    
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria não encontrada")
    
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Centro de treinamento não encontrado")
    
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_in.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError as e:
        await db_session.rollback()
        if "cpf" in str(e.orig).lower():
            raise HTTPException(
                status_code=303,
                detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}"
            )
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return atleta_out

@api_router.get(
    '/',
    summary="Consultar todos os atletas",
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaListOut]
)
async def query(
    db_session: DatabaseDependency,
    nome: Optional[str] = Query(None, description="Filtrar por nome"),
    cpf: Optional[str] = Query(None, description="Filtrar por CPF")
) -> list[AtletaListOut]: # type: ignore
    
    query = select(AtletaModel)
    if nome:
        query = query.where(AtletaModel.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.where(AtletaModel.cpf == cpf)
    result = await db_session.execute(query)
    atletas = result.scalars().all()

    lista_saida = [
        AtletaListOut(
            nome=a.nome,
            centro_treinamento=a.centro_treinamento.nome if a.centro_treinamento else "",
            categoria=a.categoria.nome if a.categoria else ""
        )
        for a in atletas
    ]
    return paginate(lista_saida)


@api_router.get('/{id}', summary="Consultar atleta pelo id", status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def query(id: UUID4, db_session: DatabaseDependency) -> AtletaOut: # type: ignore
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")
    
    return atleta   

@api_router.patch('/{id}', summary="Atualizar atleta pelo id", status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def patch(id: UUID4, atleta_up: AtletaUpdate = Body(...), db_session: DatabaseDependency) -> AtletaOut: # type: ignore
    atleta = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    
    try:
    
        for key,value in atleta_update.items():
            setattr(atleta, key, value)
        
        await db_session.commit()
        await db_session.refresh(atleta)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return atleta_update

@api_router.delete('/{id}', summary="Deletar atleta pelo id", status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None: # type: ignore
    atleta = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")
    
    try:
        await db_session.delete(atleta)
        await db_session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    