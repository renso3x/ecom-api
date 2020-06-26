from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register("address", views.AddressViewSet)
router.register("store", views.StoreViewSet)
router.register("category", views.CategoryViewSet)
router.register("product", views.ProductViewSet)

app_name = "api"

urlpatterns = [path("", include(router.urls))]
