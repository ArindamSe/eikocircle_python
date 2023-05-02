from django.db import models

from Common.models import Common
from product.models import Product

class ItemCollected(Common):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.IntegerField()
    
    
class ItemCollectedPictures(Common):
    item_collected = models.ForeignKey(ItemCollected, on_delete=models.CASCADE)
    picture = models.FileField(upload_to='media/itemcollected/pictures')
    
    class Meta:
        db_table = "ItemCollected Pictures"
        
    def __str__(self):
        return f"{self.item_collected}-{self.picture}"