from django.contrib.auth.models import AbstractUser
from django.db import models

from Common.models import Common


class Brands(Common):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "Brands"
        verbose_name = "Brand name"
        
    def __str__(self):
        return self.name
    
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
    company_name = models.CharField(max_length=100, null=True, blank=True)
    brand_name = models.ForeignKey(Brands, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    mobile = models.CharField(max_length=10, blank=True, null=True)
    
    class Meta:
        db_table = "Users"
        verbose_name = "User"
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    