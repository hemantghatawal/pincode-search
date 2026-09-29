from pydantic import BaseModel, field_validator


def validate_pincode(value: str) -> str:
    if len(value) != 6 or not value.isdigit():
        raise ValueError("Pincode must be exactly of 6 digits")
    return value


class PincodeRequest(BaseModel):
    pincode: str

    # pincode must be exactly of 6 digits
    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, value):
        validate_pincode(value)


class LocationResponse(BaseModel):
    pincode: str
    city: str
    state: str
    district: str


class BulkRequest(BaseModel):
    pincodes: list[str]

    @field_validator("pincodes")
    @classmethod
    def validate_pincodes(cls, values):
        if len(values) == 0:
            raise ValueError("At least one pincode is required.")

        if len(values) > 20:
            raise ValueError("Max 20 pincodes allowed per request.")

        for code in values:
            PincodeRequest.validate_pincode(code)
        return values


class BulkResponse(BaseModel):
    status: str = "success"
    found: int
    not_found: int
    results: list[LocationResponse]
    missing: list[str]
