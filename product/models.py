from django.db import models

from Common.models import Common
from Item.models import Item

class Product(Common):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "Product Category"
        
    def __str__(self):
        return f"{self.name} - {self.item}"