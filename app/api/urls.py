from rest_framework.routers import DefaultRouter

from .views import URLListCreateViewSet


router = DefaultRouter()
router.register(r'', URLListCreateViewSet, basename='url_viewset')

urlpatterns = router.urls



