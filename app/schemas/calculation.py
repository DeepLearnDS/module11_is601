
"""
Calculation Pydantic Schemas

This module defines Pydantic schemas for validating calculation data at the
API boundary. Pydantic provides automatic validation, serialization, and
documentation generation for FastAPI.

Key Concepts:
- Schemas define the shape of data coming in/out of the API
- Validation happens automatically before data reaches your code
- Field validators provide custom validation logic
- Model validators can validate across multiple fields
- ConfigDict controls schema behavior and documentation

Design Pattern: Data Transfer Objects (DTOs)
These schemas act as DTOs, defining contracts between API and clients.
"""

from enum import Enum
from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    model_validator,
    field_validator,
)


class CalculationType(str, Enum):
    """
    Enumeration of valid calculation types.
    """

    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"


class CalculationBase(BaseModel):
    """
    Base schema for calculation data.
    """

    type: CalculationType = Field(
        ...,
        description="Type of calculation to perform",
        examples=["addition"],
    )

    inputs: list[float] = Field(
        ...,
        min_length=2,
        description="List of numeric inputs for the calculation",
        examples=[[10.5, 3, 2]],
    )

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, value):
        """
        Normalize calculation type to lowercase.
        """

        allowed = {item.value for item in CalculationType}

        if not isinstance(value, str) or value.lower() not in allowed:
            raise ValueError(
                f"Type must be one of: {', '.join(sorted(allowed))}"
            )

        return value.lower()

    @model_validator(mode="after")
    def validate_inputs(self) -> "CalculationBase":
        """
        Validate calculation inputs.

        Division cannot have zero in any denominator position.
        The first input is the numerator and may be zero.
        """

        if self.type == CalculationType.DIVISION:
            if any(value == 0 for value in self.inputs[1:]):
                raise ValueError("Cannot divide by zero")

        return self

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "type": "addition",
                    "inputs": [10.5, 3, 2],
                },
                {
                    "type": "division",
                    "inputs": [100, 2],
                },
            ]
        },
    )


class CalculationCreate(CalculationBase):
    """
    Schema for creating a new Calculation.
    """

    user_id: UUID = Field(
        ...,
        description="UUID of the user who owns this calculation",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "type": "addition",
                "inputs": [10.5, 3, 2],
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        },
    )


class CalculationUpdate(BaseModel):
    """
    Schema for updating an existing Calculation.

    All fields are optional since partial updates are allowed.
    """

    inputs: Optional[list[float]] = Field(
        None,
        min_length=2,
        description="Updated calculation inputs",
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "inputs": [42, 7],
            }
        },
    )


class CalculationResponse(CalculationBase):
    """
    Schema for reading a Calculation from the database.
    """

    id: UUID = Field(
        ...,
        description="Unique UUID of the calculation",
        examples=["123e4567-e89b-12d3-a456-426614174999"],
    )

    user_id: UUID = Field(
        ...,
        description="UUID of the user who owns this calculation",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )

    created_at: datetime = Field(
        ...,
        description="Time when the calculation was created",
    )

    updated_at: datetime = Field(
        ...,
        description="Time when the calculation was last updated",
    )

    result: float = Field(
        ...,
        description="Result of the calculation",
        examples=[15.5],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174999",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "type": "addition",
                "inputs": [10, 5],
                "result": 15.0,
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00",
            }
        },
    )


# Alias for compatibility with code that imports CalculationRead
CalculationRead = CalculationResponse
