from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from server import hooks
from . import oauth_urls

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    def sentry_test(request):
        a = 1 / 0
        print(a)

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        # Test only
        path("__sentry_test__/", sentry_test, name="error_text"),
        path("__error_test__/", TemplateView.as_view(template_name="404.html")),
        path("__debug__/", include("debug_toolbar.urls")),
    ]

i18n_patterns_list = [
    # path("", include("dash.urls")),
]

# Get registered global i18n urls from hooks
i18n_patterns_hooks = hooks.get_hooks("APP_I18N_URL_PATTERNS")
for hook in i18n_patterns_hooks:
    url_path, urls_module = hook()
    i18n_patterns_list.append(path(url_path, include(urls_module)))

i18n_patterns_list = i18n_patterns_list + [
    path("admin/docs/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += i18n_patterns(
    *i18n_patterns_list,
    prefix_default_language=True,
)

urlpatterns += [
    path("api/", include("server.api.urls")),
    path("oauth/", include(oauth_urls, namespace="oauth2_provider")),
]
