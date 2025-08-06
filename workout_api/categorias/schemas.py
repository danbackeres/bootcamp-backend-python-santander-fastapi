from workout_api.contrib.schemas import BaseSchema

from pydantic import Field
from typing import Annotated

class Categoria(BaseSchema):
    nome: Annotated[str, Field(title="Nome da categoria", example="Atleta", max_length=50)]