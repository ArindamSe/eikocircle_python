from django.db import models

from Common.models import Common
from product.models import Product
from brand_product.models import Brand_product

class AwarenessPlan(Common):
    Medium = (
        ('school_program', 'School Program'),
        ('polular_places_program', 'Popular Places Program'),
        ('awareness_drive', 'Awareness Drive'),
        ('advertisements', 'Advertisements'),
        ('online_campaigns', 'Online Campaigns'),
        ('city_awareness_and_collection_drive', 'City Awareness and Collection Drive'),
        ('radios', 'Radios'),
        ('rwas', 'RWAs')
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    theme = models.CharField(max_length=200, null=True, blank=True)
    medium = models.CharField(max_length=50, choices=Medium, default="online_campaigns")
    city = models.CharField(max_length=30, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    communication = models.TextField(null=True, blank=True)
    target_audience = models.IntegerField(null=True, blank=True)
    brand = models.ForeignKey(Brand_product, null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "Awareness Plan"
        
    def __str__(self):
        return f"{self.product}-{self.theme}-{self.city}-{self.date}"
    
class AwarenessPlanPics(Common):
    awarenessplan = models.ForeignKey(AwarenessPlan, on_delete=models.CASCADE)
    pics = models.FileField(upload_to='media/awarenessplan/pics')
    
    class Meta:
        db_table = "Awareness Plan Pics"
        
    def __str__(self):
        return f"{self.awarenessplan.theme}-{self.pics}"
    