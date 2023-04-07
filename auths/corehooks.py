from server import hooks


@hooks.register("API_V1_URL_PATTERNS")
def register_api_v1_path():
    return "", "auths.api.v1.urls"
