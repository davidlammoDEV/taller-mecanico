from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class User_LogSalida(BaseModel):
    iduser : str
    idrol : int
   


class User_LogEntrada(BaseModel):
    iduser : str
    idrol : int
   

class User_LogUpdata(BaseModel):
    iduser : Optional[str] | None = None
    idrol : Optional[int] | None = None
    