from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from src.constants.language_code import LanguageCode
from src.controllers.user.auth_controller import get_current_active_user
from src.db.models.user import PortalRole

localization_router = APIRouter(
    prefix="/localization",
    tags=["Localization"],
    dependencies=[Depends(get_current_active_user(required_roles=PortalRole.all_roles()))],
)
localization_router.tags_metadata = [
    {
        "name": "Localization",
        "description": "",
    }
]


@localization_router.get("/{lang_code}", response_model=None)
async def get_localization(lang_code: LanguageCode) -> FileResponse:
    file_path = Path("../common/localization") / f"{lang_code.value}.json"

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Localization file not found")

    return FileResponse(
        path=file_path,
        media_type="application/json",
        filename=f"{lang_code.value}.json",
    )


__all__ = [
    "localization_router",
]
