"""Ordinary development smoke check; external replay is broader."""
from app import QuoteRequest, quote

request=QuoteRequest(customerId=' acme ', reference=7, memo=None, units=2, unitPrice='12.50')
response=quote(request)
assert response.customer_id=='acme'
assert response.total==25
print('development model smoke passed')
