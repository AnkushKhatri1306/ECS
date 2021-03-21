from rest_framework import serializers
from .models import *

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('id', 'title', 'on_discount', 'price', 'discount_price', 'description', 'image_path',
                  'date_created','date_updated')

