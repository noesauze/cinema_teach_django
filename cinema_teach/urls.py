from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("modules", views.modules, name="modules"),
    path("about", views.about, name="about"),
    path("modules/solide/etalonnage", views.etalonnage_solide, name="etalonnage_solide"),
    path("modules/point", views.point, name="point"),
    path("modules/point/resultats", views.resultats_point, name="resultats_point"),
    path("modules/solide",views.solide,name="solide"),
    
    path("modules/solide/resultats", views.resultats_solide, name="resultats_solide"),
    path("vider-cache", views.vider, name="vider"),
    path("modules/point/post-point", views.post_point, name="post-point"),
    path("getData", views.get_table_data, name="get-table-data")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

