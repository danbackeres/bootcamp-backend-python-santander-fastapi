from workout_api.contrib.schemas import BaseSchema

from pydantic import UUID4, Field
from typing import Annotated

class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(title="Nome do centro de treinamento", example="CT King", max_length=10)]
    endereco: Annotated[str, Field(title="Endereço do centro de treinamento", example="Av. Paulista, 1000", max_length=100)]
    proprietario: Annotated[str, Field(title="Proprietário do centro de treinamento", example="João", max_length=50)]
    
class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(title="Nome do centro de treinamento", example="CT King", max_length=10)]
    
class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description="Identificador do centro de treinamento")]