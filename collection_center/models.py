from django.db import models

from Common.models import Common

class CollectionCenter(Common):
    Medium = (
        ('refurbisher', 'Refurbisher'),
        ('aggregator', 'Aggregator'),
        ('individuals', 'Individuals'),
        ('bulk_consumer', 'Bulk_Consumers')
    )
    
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True, blank=True)
    number = models.CharField(max_length=10, blank=True, null=True)
    medium = models.CharField(max_length=50, choices=Medium, default='bulk_consumer')
    city = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        db_table = "Collection Centers"
        
    def __str__(self):
        return f"{self.name}-{self.medium}-{self.city}"
    