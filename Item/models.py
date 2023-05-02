from django.db import models

from Common.models import Common

class Item(Common):
    item_code = models.CharField(max_length=100)
    target = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = "Item"
        
    def __str__(self):
        return f"Item {self.item_code}"
    
class ItemSalePurchaseInvoice(Common):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    salepurchaseinvoice = models.FileField(upload_to='media/item/salepurchaseinvoice/')
    
    class Meta:
        db_table = "ItemSalePurchaseInvoice"
        
    def __str__(self):
        return f"{self.item} - {self.salepurchaseinvoice}"
    
class ItemProofOfDelivery(Common):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    proofofdelivery = models.FileField(upload_to='media/item/proofofdelivery/')
    
    class Meta:
        db_table = "ItemProofOfDelivery"
        
    def __str__(self):
        return f"{self.item} - {self.proofofdelivery}"
    
class ItemMaterialRecoveryReport(Common):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    materialrecoveryreport = models.FileField(upload_to='media/item/materialrecoveryreport/')
    
    class Meta:
        db_table = "ItemMaterialRecoveryReport"
        
    def __str__(self):
        return f"{self.item} - {self.materialrecoveryreport}"
    
class ItemRecyclingCertificate(Common):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    recyclingcertificate = models.FileField(upload_to='media/item/recyclingcertificate/')
    
    class Meta:
        db_table = "ItemRecyclingCertificate"
        
    def __str__(self):
        return f"{self.item} - {self.recyclingcertificate}"