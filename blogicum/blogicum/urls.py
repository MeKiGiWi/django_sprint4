from blog import views as blog_views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/registration/", blog_views.registration, name="registration"),
    path("auth/", include("django.contrib.auth.urls")),
    path("", include("blog.urls")),
    path("pages/", include("pages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "pages.views.page_not_found"
handler500 = "pages.views.server_error"
handler403 = "pages.views.permission_denied"
