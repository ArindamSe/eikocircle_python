from django.db import models

from Common.models import Common
from authentication.models import Brands
from product.models import Product

class RepairShop(Common):
    name = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    number = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    
    class Meta:
        db_table = "Repair Shop"
        
    def __str__(self):
        return f'{self.name}-{self.city}'

class RepairShopRecord(Common):
    Product_Status = (
        ('reusable', 'Reusable'),
        ('to_be_discarded', 'To Be Discarded')
    )
    
    Item_status = (
        ('sold_to_collection_center', "Sold To Collection Center"),
        ('sold_to_recycler', 'Sold To Recycler'),
        ('still_in_shop', 'Still in Shop')
    )
    
    shop = models.ForeignKey(RepairShop, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_status = models.CharField(max_length=100, choices=Product_Status, default='reusable')
    reusable = models.TextField(null=True, blank=True)
    form = models.TextField(null=True, blank=True)
    discard_item_status = models.CharField(max_length=100, choices=Item_status, default="still_in_shop")
    price = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = "Repair Shop Record"
        
    def __str__(self):
        return f"{self.product}-{self.product_status}"
    
class RepairShopItemPics(Common):
    record_item = models.ForeignKey(RepairShopRecord, on_delete=models.CASCADE)
    pics = models.FileField(upload_to='media/repairshop/pics')
    
    class Meta:
        db_table = "Repair Shop Item Pics"
        
    def __str__(self):
        return f'{self.record_item.product}-{self.pics}'
