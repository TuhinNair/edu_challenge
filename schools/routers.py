from rest_framework_nested import routers
from .views import SchoolViewSet, StudentViewSet


router = routers.DefaultRouter()
router.register(r'schools', SchoolViewSet, basename='school')
router.register(r'students', StudentViewSet, basename='student')

schools_router = routers.NestedSimpleRouter(router, r'schools', lookup='school')
schools_router.register(r'students', StudentViewSet, basename='school-students')

