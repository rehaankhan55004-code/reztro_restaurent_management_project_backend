from pydantic import (
    BaseModel,
    Field,
    EmailStr
)


class OnlineOrderCreate(BaseModel):

    delivery_address: str = Field(
        ...,
        min_length=10,
        max_length=500
    )

    city: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    state: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    postal_code: str = Field(
        ...,
        min_length=4,
        max_length=20
    )

    contact_person: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    contact_phone: str = Field(
        ...,
        min_length=10,
        max_length=20
    )

    contact_email: EmailStr | None = None

    delivery_notes: str | None = Field(
        None,
        max_length=500
    )


class OnlineOrderUpdate(BaseModel):

    delivery_address: str = Field(
        ...,
        min_length=10,
        max_length=500
    )

    city: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    state: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    postal_code: str = Field(
        ...,
        min_length=4,
        max_length=20
    )

    contact_person: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    contact_phone: str = Field(
        ...,
        min_length=10,
        max_length=20
    )

    contact_email: EmailStr | None = None

    delivery_notes: str | None = Field(
        None,
        max_length=500
    )