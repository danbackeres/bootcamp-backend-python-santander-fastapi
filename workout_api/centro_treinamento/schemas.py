from workout_api.contrib.schemas import BaseSchema

from pydantic import Field
from typing import Annotated

class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(title="Nome do centro de treinamento", example="CT King", max_length=10)]
    endereco: Annotated[str, Field(title="Endereço do centro de treinamento", example="Av. Paulista, 1000", max_length=100)]
    proprietario: Annotated[str, Field(title="Proprietário do centro de treinamento", example="João", max_length=50)]