from server import hooks


@hooks.register("APP_I18N_URL_PATTERNS")
def register_boards_app_urls():
    return "", "boards.urls"
