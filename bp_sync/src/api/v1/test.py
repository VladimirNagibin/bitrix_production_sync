from fastapi import APIRouter, status  # , Depends
from fastapi.responses import JSONResponse

test_router = APIRouter()  # dependencies=[Depends(request_context)])


@test_router.get(
    "/",
    summary="check",
    description="Information about.",
)  # type: ignore
async def check(
    id_entity: int | str | None = None,
) -> JSONResponse:

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": id_entity,
        },
    )
