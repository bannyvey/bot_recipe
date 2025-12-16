import json
import logging

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict

logger = logging.getLogger(__name__)

class BaseModel(PydanticBaseModel):
    """Базовая модель с настройками по умолчанию"""
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        validate_assignment=True,
    )
    
    def to_dict(self, *, by_alias: bool = True, exclude_unset: bool = False) -> dict:
        """Преобразовать в словарь"""
        result: dict = json.loads(self.model_dump_json(exclude_none=True))
        logger.info(f"{result}")
        return result