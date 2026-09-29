from fastapi import FastAPI
from data import pincode_db
from exceptions import (
    PinCodeNotFoundError,
    pincode_not_found_handler,
    invalid_pincode_handler,
    InvalidPinCodeError,
)
from models import BulkRequest, BulkResponse, LocationResponse

app = FastAPI(
    title="Pincode search API",
    description="Auto fill city and state from Indian Pincode during checkout",
)

# register your custom exception handler
app.add_exception_handler(PinCodeNotFoundError, pincode_not_found_handler)
app.add_exception_handler(InvalidPinCodeError, invalid_pincode_handler)


@app.get("/")
def root():
    return {"message": "Welcome to Pincode Search API"}


@app.get("/pincode/{code}", response_model=LocationResponse)
def search_pincode(code: str):
    if len(code) != 6 or not code.isdigit():
        raise InvalidPinCodeError(code, "Must be exactly 6 digits")

    if code not in pincode_db:
        raise PinCodeNotFoundError(code)

    return pincode_db[code]


@app.post("/pincode/bulk", response_model=BulkResponse)
def bulk_search(request: BulkRequest):
    results = []
    missing = []

    for code in request.pincodes:
        if code in pincode_db:
            results.append(pincode_db[code])
        else:
            missing.append(code)
        
    return BulkResponse(
        status="success",
        found=len(results),
        not_found=len(missing),
        results=results,
        missing=missing,
    )
