from rest_framework import routers
from .views import SchoolViewSet, StudentViewSet

router = routers.DefaultRouter()
router.register(r'schools', SchoolViewSet)
router.register(r'students', StudentViewSet)