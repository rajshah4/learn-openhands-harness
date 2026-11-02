from decimal import Decimal
from typing import Optional, Union

from fastapi import FastAPI
from pydantic import BaseModel, Field, validator

app = FastAPI(title='Quote API', version='1.0')

class QuoteRequest(BaseModel):
    customer_id: str = Field(alias='customerId')
    reference: Union[int, str]
    memo: Optional[str]
    units: int = Field(gt=0, le=1000)
    unit_price: Decimal = Field(alias='unitPrice', gt=0)

    @validator('customer_id')
    def normalize_customer(cls, value):
        value = value.strip()
        if not value:
            raise ValueError('customer ID cannot be blank')
        return value

    class Config:
        allow_population_by_field_name = True
        extra = 'forbid'

class QuoteResponse(BaseModel):
    customer_id: str = Field(alias='customerId')
    reference: Union[int, str]
    memo: Optional[str]
    total: Decimal

    class Config:
        allow_population_by_field_name = True

@app.post('/quotes', response_model=QuoteResponse)
def quote(request: QuoteRequest):
    return QuoteResponse(customer_id=request.customer_id,
        reference=request.reference, memo=request.memo,
        total=request.unit_price * request.units)
