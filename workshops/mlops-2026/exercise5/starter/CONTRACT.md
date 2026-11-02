# Quote API migration contract

Move this API to fastapi==0.115.12 and pydantic==2.11.7, keeping uvicorn==0.34.3. Use native v2 models/configuration/validators/serialization; no pydantic.v1 imports or vendored v1. Python 3.12.

POST /quotes accepts customerId or customer_id, reference (integer or string), units (1..1000), unitPrice (>0), optional memo. Existing clients send numeric customer IDs; these must continue to normalize to strings. Trim customer IDs and reject blank IDs. Digit-only references normalize to integer values; nonnumeric references remain strings. Omitted memo defaults to null, as does explicit null. Reject unknown fields, missing required fields, nonpositive price, invalid units and container-valued references. Successful responses contain exactly customerId, reference, memo, total. Total remains a JSON number. Existing string/number coercion remains accepted for integral units and prices. Preserve behavior described here, not undocumented validation defects. Rejection status is 422; exact framework error wording is not part of the contract.

The controller has a frozen replay acceptance suite including positive and negative requests. A native completion hook runs it automatically. You may run your own checks at any time. Do not change controller files. Work only in your isolated service directory. Finish with changes and test results.
