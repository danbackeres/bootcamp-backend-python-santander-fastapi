from sqlalchemy.orm import DeclarativeBase

class BaseModel(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)