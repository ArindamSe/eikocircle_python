from django.db import models

from Common.models import Common
from product.models import Product
from brand_product.models import Brand_product

class ItemCollected(Common):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand_product, on_delete=models.CASCADE)
    target = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = "ItemCollected"
        
    def __str__(self):
        return f"{self.product.item}-{self.product}-{self.weight}"
    
    
class ItemCollectedPictures(Common):
    item_collected = models.ForeignKey(ItemCollected, on_delete=models.CASCADE)
    picture = models.FileField(upload_to='media/itemcollected/pictures')
    
    class Meta:
        db_table = "ItemCollected Pictures"
        
    def __str__(self):
        return f"{self.item_collected}-{self.picture}"