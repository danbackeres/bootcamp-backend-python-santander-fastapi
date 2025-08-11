from typing import Annotated, Optional
from pydantic import Field, PositiveFloat

from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin


class Atleta(BaseSchema):
    nome: Annotated[str, Field(title="Nome do atleta", example="João", max_length=50)]
    cpf: Annotated[str, Field(title="CPF do atleta", example="123.456.789-10", max_length=14)]  
    idade: Annotated[int, Field(title="Idade do atleta", example="20", ge=0, le=120)]
    peso: Annotated[PositiveFloat, Field(title="Peso do atleta", example="75.5", ge=0)]
    altura: Annotated[PositiveFloat, Field(title="Altura do atleta", example="1.75", ge=0)]
    sexo: Annotated[str, Field(title="Sexo do atleta", example="M", max_length=1)]
    categoria: Annotated[CategoriaIn, Field(title="Categoria do atleta")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(title="Centro de treinamento do atleta")]
    
class AtletaIn(Atleta):
    pass
    
class AtletaOut(AtletaIn, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, title="Nome do atleta", example="João", max_length=50)]
    idade: Annotated[Optional[int], Field(None, title="Idade do atleta", example="20", ge=0, le=120)]