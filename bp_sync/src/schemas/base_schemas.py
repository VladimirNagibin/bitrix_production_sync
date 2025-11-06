from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
)
from typing_extensions import Self


class CommonFieldMixin(BaseModel):  # type: ignore[misc]
    internal_id: UUID | None = Field(
        default=None,
        exclude=True,
        init_var=False,
    )
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
    is_deleted_in_bitrix: bool | None = Field(default=None)
    external_id: int | str | None = Field(
        default=None,
        validation_alias=AliasChoices("ID", "id"),
    )

    @property
    def id(self) -> UUID | None:
        return self.internal_id

    @id.setter
    def id(self, value: UUID) -> None:
        self.internal_id = value

    def get_changes(
        self, entity: Self, exclude_fields: set[str] | None = None
    ) -> dict[str, dict[str, Any]]:
        if exclude_fields is None:
            exclude_fields = {
                "internal_id",
                "created_at",
                "updated_at",
                "is_deleted_in_bitrix",
            }

        differences: dict[str, dict[str, Any]] = {}

        model_class = self.__class__
        fields = model_class.model_fields

        for field_name in fields:
            if field_name in exclude_fields:
                continue

            old_value = getattr(self, field_name)
            new_value = getattr(entity, field_name)

            # Сравниваем значения
            if not self._are_values_equal(field_name, old_value, new_value):
                differences[field_name] = {
                    "internal": old_value,
                    "external": new_value,
                }

        return differences

    def _are_values_equal(
        self, field_name: str, value1: Any, value2: Any
    ) -> bool:
        """
        Сравнивает два значения с учетом специальных типов данных.
        """
        # Оба значения None
        if value1 is None and value2 is None:
            return True

        if field_name == "company_id":
            if value1 in (0, None) and value2 in (0, None):
                return True

        # Одно из значений None
        if value1 is None or value2 is None:
            return False

        # Для Enum сравниваем значения
        if isinstance(value1, Enum) and isinstance(value2, Enum):
            return bool(value1.value == value2.value)
        # elif hasattr(value1, "value") and hasattr(value2, "value"):
        # Для других объектов с атрибутом value
        # return value1.value == value2.value

        # Для Pydantic моделей рекурсивно сравниваем все поля
        if isinstance(value1, BaseModel) and isinstance(value2, BaseModel):
            return bool(value1.model_dump() == value2.model_dump())

        # Для списков и словарей сравниваем содержимое
        if isinstance(value1, (list, dict)) and isinstance(
            value2, (list, dict)
        ):
            return bool(value1 == value2)

        # Стандартное сравнение
        return bool(value1 == value2)


class ListResponseSchema(BaseModel):  # type: ignore[misc]
    """Схема для ответа со списком сущностей"""

    result: list[CommonFieldMixin]
    total: int
    next: int | None = None

    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        extra="ignore",
    )
