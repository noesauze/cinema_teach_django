from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("modules", views.modules, name="modules"),
    path("modules/point", views.point, name="point"),
    path("modules/point/resultats", views.resultats_point, name="resultats_point"),
    path("modules/solide",views.solide,name="solide")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

