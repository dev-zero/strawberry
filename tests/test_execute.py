import pytest

import strawberry
from graphql import DirectiveLocation
from strawberry.graphql import execute


@pytest.mark.asyncio
async def test_handles_async_resolvers():
    @strawberry.type
    class Query:
        @strawberry.field
        async def async_field(self, info) -> str:
            return "async result"

    schema = strawberry.Schema(Query)

    result = await execute(schema, "{ asyncField }")

    assert not result.errors
    assert result.data["asyncField"] == "async result"


@pytest.mark.asyncio
async def test_runs_directives():
    @strawberry.type
    class Query:
        name: str = "Jess"

    @strawberry.directive(
        locations=[DirectiveLocation.FIELD], description="Make string uppercase"
    )
    def uppercase(value: str):
        return value.upper()

    @strawberry.directive(locations=[DirectiveLocation.FIELD])
    def replace(value: str, old: str, new: str):
        return value.replace(old, new)

    schema = strawberry.Schema(query=Query, directives=[uppercase, replace])

    query = """{
        name @uppercase
        jess: name @replace(old: "Jess", new: "Jessica")
    }"""

    result = await execute(schema, query)

    assert not result.errors
    assert result.data["name"] == "JESS"
    assert result.data["jess"] == "Jessica"
