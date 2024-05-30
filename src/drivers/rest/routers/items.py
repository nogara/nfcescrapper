from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from drivers.rest.dependencies import get_items_services
from drivers.rest.schemas.items import (
    ItemModel,
    ItemPatchRequestModel,
    ItemPostRequestModel,
)
from services import ItemService

__all__ = ["router"]

router = APIRouter(prefix="/items")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_items(
    service: Annotated[ItemService, Depends(get_items_services)]
) -> list[ItemModel]:

    return service.find_all()


@router.get("/{item_id}", status_code=status.HTTP_200_OK)
async def get_item(
    item_id: int,
    service: Annotated[ItemService, Depends(get_items_services)],
) -> None:
    try:
        item_id = int(item_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID da empresa é obrigatório",
        )

    if item_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID da empresa inválido"
        )

    item = service.find_by_id(item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada"
        )

    return item


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_item(
    id: int,
    item: ItemPatchRequestModel,
    service: Annotated[ItemService, Depends(get_items_services)],
) -> None:
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID da empresa é obrigatório",
        )

    if id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID da empresa inválido"
        )

    service.update(id, item)

    return item


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemPostRequestModel,
    service: Annotated[ItemService, Depends(get_items_services)],
) -> ItemModel:
    entity = service.save(item)

    return entity


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    service: Annotated[ItemService, Depends(get_items_services)],
) -> None:
    """Delete a item by it's ID

    Args:
        item_id (int): The item ID
    """
    try:
        item_id = int(item_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID do item é obrigatório",
        )

    if item_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID do item inválido"
        )

    service.delete(item_id)


@router.get("/invoices/{id}", status_code=status.HTTP_200_OK)
async def get_by_invoice_id(
    id: int,
    service: Annotated[ItemService, Depends(get_items_services)],
) -> list[ItemModel]:
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID da nota é obrigatório",
        )
    if id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID da nota fiscal inválido"
        )

    return service.find_all(invoice_id=id)
