from slowapi import Limiter


def get_rate_limit_key(request):
    return request.state.api_key


limiter = Limiter(key_func=get_rate_limit_key)