from django.db import models

from Common.models import Common
from product.models import Product
from authentication.models import Brands

class RecyclingCenter(Common):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True, blank=True)
    number = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        db_table = "Recycling Center"
        
    def __str__(self):
        return f"{self.name}-{self.address}"
    
class ItemRecycled(Common):
    recyclingcenter = models.ForeignKey(RecyclingCenter, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    target = models.IntegerField(null=True, blank=True)
    recycled = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = "Item Recycled"
        
    def __str__(self):
        return f"{self.recyclingcenter}-{self.product}-{self.target}-{self.recycled}"
    