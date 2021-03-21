from rest_framework import routers
from .views import *
from django.urls import path
from .views import get_courses

router = routers.SimpleRouter()

router.register(r'course', CourseViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('course', get_courses)

]