from django.db import models

# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=100)
    on_discount = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=1, max_digits=15)
    discount_price = models.DecimalField(decimal_places=1, max_digits=15)
    description = models.CharField(max_length=255, blank=True, null=True)
    image_path = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_course'



