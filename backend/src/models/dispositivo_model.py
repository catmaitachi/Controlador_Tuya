from pydantic import BaseModel, Field

class Cor(BaseModel):
    
    r: int = Field(ge=0, le=255)
    g: int = Field(ge=0, le=255)
    b: int = Field(ge=0, le=255)

class Branco(BaseModel):

    temperatura: int = Field(ge=0, le=100)
    brilho: int = Field(ge=0, le=100)

class DispositivoState(BaseModel):

    modo: str
    cor: Cor | None = None
    branco: Branco | None = None

class DispositivoInfo(BaseModel):

    id: str
    name: str
    ip: str | None
    key: str
    ver: str | None
