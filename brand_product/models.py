from django.db import models

from Common.models import Common
from product.models import Product
from authentication.models import Brands

class Brand_product(Common):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    target = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = "BrandProduct"
        
    def __str__(self):
        return f"{self.brand}-{self.product}-{self.target}"