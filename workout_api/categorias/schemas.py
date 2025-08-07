from workout_api.contrib.schemas import BaseSchema

from pydantic import UUID4, Field
from typing import Annotated

class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(title="Nome da categoria", example="Atleta", max_length=50)]
    
class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description="Identificador da categoria")]