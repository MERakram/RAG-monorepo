from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime, timezone
from app.schema.user import Roles


class PyObjectId(ObjectId):
    """
    A custom Pydantic-compatible ObjectId field to handle MongoDB's ObjectId.

    Provides:
    - Validation: Ensures that the ObjectId is valid.
    - Schema modification: Adjusts OpenAPI schema to treat the field as a string.
    """

    @classmethod
    def __get_validators__(cls):
        """Yield the validator for ObjectId to be used by Pydantic."""
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        """
        Validate that the input is a valid ObjectId.

        Args:
            v: The value to validate.
            info: Field validation info (added for Pydantic v2 compatibility)

        Returns:
            A valid ObjectId.

        Raises:
            ValueError: If the ObjectId is invalid.
        """
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        """Modify the field schema to represent ObjectId as a string."""
        field_schema.update(type="string")



class UserDB(BaseModel):
    """
    A Pydantic model representing a user in the database.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str = Field(unique=True)
    hashed_password: str
    active: bool = Field(default=False)
    role: Roles = Field(default="agent")
    username: str = Field(unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


    class Config:
        """
        Configuration for the Pydantic model.
        
        Settings:
            validate_by_name: Allows the model to populate fields using the field's alias.
            arbitrary_types_allowed: Allows the use of arbitrary Python types like ObjectId.
            json_encoders: Custom JSON encoder for ObjectId to convert it to a string.
        """
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}



