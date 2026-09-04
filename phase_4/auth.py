from fastapi import Depends,HTTPException,Request
from fastapi.security import APIKeyHeader



api_key_header = APIKeyHeader(
    name="X-API-Key", 
    auto_error=True)


VALID_API_KEYS = {
    "test-user-1",
    "test-user-2"
}

def get_api_key(request: Request, 
                api_key: str = Depends(api_key_header)) -> str:
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
    request.state.api_key = api_key
    return api_key

