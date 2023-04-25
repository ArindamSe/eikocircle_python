from django.contrib.auth.models import AbstractUser
from django.db import models

from Common.models import Common    

class Brand(Common):
    brand_name = models.CharField()
    
class User(AbstractUser, Common):
    ROLES = (
        ('brand', 'Brand'),
        ('refurbisher', 'Refurbisher'),
        ('collection_center', 'Collection Center'),
        ('recycling_unit', 'Recycling Unit'),
        ('individual_consumer', 'Individual Consumer'),
        ('bulk_consumer', 'Bulk Consumer')
    )

    role = models.CharField(max_length=20, choices=ROLES, default='brand')
    company_name = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    mobile = models.CharField(max_length=10, blank=True, null=True)
    

    class Meta:
        db_table = "Users"
        verbose_name = "User"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
