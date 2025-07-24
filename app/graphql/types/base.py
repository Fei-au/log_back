import strawberry

@strawberry.type
class BaseInsertOneResponse:
    inserted_id: str
    
@strawberry.type
class BaseUpdateOneResponse:
    modified_count: int
    