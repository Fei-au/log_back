from typing import Generic, TypeVar, Optional
from pydantic import BaseModel


T = TypeVar("T") 
    

class ResponseBase(BaseModel, Generic[T]):
    status: str = "success"
    message: Optional[str] = "OK"
    data: Optional[T]
    
class InsertOneResponse(BaseModel):
    inserted_id: str
    
class InsertManyResponse(BaseModel):
    inserted_ids: list[str]
    
class UpdateResponse(BaseModel):
    modified_count: int
    
class DeleteResponse(BaseModel):
    deleted_count: int