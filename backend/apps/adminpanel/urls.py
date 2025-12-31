from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminOverviewViewSet, AdminLogViewSet, NotificationTemplateViewSet

router = DefaultRouter()
router.register(r'admin', AdminOverviewViewSet, basename='admin')
router.register(r'admin-logs', AdminLogViewSet, basename='admin-log')
router.register(r'notification-templates', NotificationTemplateViewSet, basename='notification-template')

urlpatterns = [
    path('', include(router.urls)),
]
