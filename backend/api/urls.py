from rest_framework.routers import DefaultRouter

from api.views import HistoryViewSet

router = DefaultRouter()
router.register(r"histories", HistoryViewSet, basename="history")

urlpatterns = router.urls
