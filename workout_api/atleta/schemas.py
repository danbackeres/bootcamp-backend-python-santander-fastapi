from typing import Annotated
from pydantic import Field, PositiveFloat

from workout_api.contrib.schemas import BaseSchema


class Atleta(BaseModel):
    nome: Annotated[str, Field(title="Nome do atleta", example="João", max_length=50)]
    cpf: Annotated[str, Field(title="CPF do atleta", example="123.456.789-10", max_length=14)]  
    idade: Annotated[int, Field(title="Idade do atleta", example="20", ge=0, le=120)]
    peso: Annotated[PositiveFloat, Field(title="Peso do atleta", example="75.5", ge=0)]
    altura: Annotated[PositiveFloat, Field(title="Altura do atleta", example="1.75", ge=0)]
    sexo: Annotated[str, Field(title="Sexo do atleta", example="M", max_length=1)]
    
    