from django.db import models

from Common.models import Common
from Item_collected.models import ItemCollected

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
    
class CollectedCenterItemCollected(Common):
    collection_center = models.ForeignKey(CollectionCenter, on_delete=models.CASCADE)
    item_collected = models.ForeignKey(ItemCollected, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "Collection Center Item Collected"
        
    def __str__(self):
        return f"{self.collection_center}-{self.item_collected}"