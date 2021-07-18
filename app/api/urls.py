from rest_framework.routers import DefaultRouter

from .views import URLListCreateViewSet


router = DefaultRouter()
router.register(r'', URLListCreateViewSet, basename='url_list_create')

urlpatterns = router.urls



