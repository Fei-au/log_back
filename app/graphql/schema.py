import strawberry
from app.graphql.queries.refund import Query, Mutation


schema = strawberry.Schema(query=Query, mutation=Mutation)
