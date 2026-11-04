
"""
Calculation Models with Polymorphic Inheritance

This module demonstrates SQLAlchemy's polymorphic inheritance pattern,
where multiple calculation types inherit from a base Calculation model.

All calculation types share one database table.
"""

from datetime import datetime
import uuid

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    JSON,
    Float,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr

from app.database import Base


class AbstractCalculation:
    """
    Abstract base class defining common attributes for all calculations.
    """

    @declared_attr
    def __tablename__(cls):
        return "calculations"

    @declared_attr
    def id(cls):
        return Column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            nullable=False,
        )

    @declared_attr
    def user_id(cls):
        return Column(
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )

    @declared_attr
    def type(cls):
        return Column(
            String(50),
            nullable=False,
            index=True,
        )

    @declared_attr
    def inputs(cls):
        return Column(
            JSON,
            nullable=False,
        )

    @declared_attr
    def result(cls):
        return Column(
            Float,
            nullable=False,
        )
    @declared_attr
    def created_at(cls):
        return Column(
            DateTime,
            default=datetime.utcnow,
            nullable=False,
        )

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False,
        )

    @declared_attr
    def user(cls):
        return relationship(
            "User",
            back_populates="calculations",
        )

    @classmethod
    def create(
        cls,
        calculation_type: str,
        user_id: uuid.UUID,
        inputs=None,
        b=None,
        **kwargs,
    ) -> "Calculation":
        """
        Factory method that creates the appropriate calculation subclass.
        Supports both inputs lists and the older two-number format.
        """

        calculation_classes = {
            "addition": Addition,
            "subtraction": Subtraction,
            "multiplication": Multiplication,
            "division": Division,
        }

        if "a" in kwargs:
            inputs = kwargs.pop("a")

        if kwargs:
            raise TypeError(f"Unexpected arguments: {', '.join(kwargs)}")

        if b is not None:
            inputs = [inputs, b]

        if not isinstance(inputs, list):
            raise ValueError("Inputs must be a list")

        if len(inputs) < 2:
            raise ValueError("At least two inputs are required")

        if not all(
            isinstance(value, (int, float)) and not isinstance(value, bool)
            for value in inputs
        ):
            raise ValueError("All inputs must be numeric")

        if calculation_type.lower() not in calculation_classes:
            raise ValueError(
                f"Unsupported calculation type: {calculation_type}"
            )

        calculation_class = calculation_classes[calculation_type.lower()]

        calculation = calculation_class(
            user_id=user_id,
            inputs=inputs,
        )

        calculation.result = calculation.get_result()

        return calculation

    def get_result(self) -> float:
        """
        Abstract method implemented by calculation subclasses.
        """
        raise NotImplementedError(
            "Subclasses must implement get_result() method"
        )

    def __repr__(self):
        return (
            f"<Calculation(type={self.type}, "
            f"inputs={self.inputs}, result={self.result})>"
        )
    def get_result(self) -> float:
        """
        Abstract method implemented by calculation subclasses.
        """
        raise NotImplementedError(
            "Subclasses must implement get_result() method"
        )

    def __repr__(self):
        return (
            f"<Calculation(type={self.type}, "
            f"inputs={self.inputs}, result={self.result})>"
        )


class Calculation(Base, AbstractCalculation):
    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "calculation",
    }


class Addition(Calculation):
    __mapper_args__ = {
        "polymorphic_identity": "addition",
    }

    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")

        if len(self.inputs) < 2:
            raise ValueError("Inputs must be a list with at least two numbers.")

        return sum(self.inputs)


class Subtraction(Calculation):
    __mapper_args__ = {
        "polymorphic_identity": "subtraction",
    }

    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")

        if len(self.inputs) < 2:
            raise ValueError("Inputs must be a list with at least two numbers.")

        result = self.inputs[0]

        for value in self.inputs[1:]:
            result -= value

        return result


class Multiplication(Calculation):
    __mapper_args__ = {
        "polymorphic_identity": "multiplication",
    }

    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")

        if len(self.inputs) < 2:
            raise ValueError("Inputs must be a list with at least two numbers.")

        result = 1

        for value in self.inputs:
            result *= value

        return result


class Division(Calculation):
    __mapper_args__ = {
        "polymorphic_identity": "division",
    }

    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")

        if len(self.inputs) < 2:
            raise ValueError("Inputs must be a list with at least two numbers.")

        result = self.inputs[0]

        for value in self.inputs[1:]:
            if value == 0:
                raise ValueError("Cannot divide by zero.")

            result /= value

        return result
