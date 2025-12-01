from typing import List

from fastapi import APIRouter, HTTPException

from src.api.models import ANIMALS, Animal

router = APIRouter(prefix="/animals", tags=["Animals"])


# PUBLIC_INTERFACE
@router.get("", summary="List animals")
def list_animals() -> List[Animal]:
    """Return all animals."""
    return list(ANIMALS.values())


# PUBLIC_INTERFACE
@router.get("/{animal_id}", summary="Get animal by id")
def get_animal(animal_id: str) -> Animal:
    """Return animal by id or 404."""
    if animal_id not in ANIMALS:
        raise HTTPException(status_code=404, detail="Animal not found")
    return ANIMALS[animal_id]
