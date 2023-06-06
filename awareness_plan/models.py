from django.db import models
from django.core.exceptions import ValidationError

from multiselectfield import MultiSelectField

from Common.models import Common
from authentication.models import Brands

def validate_medium_count(value):
    max_choices = 8
    if len(value) > max_choices:
        raise ValidationError(f"Please select a maximum of {max_choices} choices.")
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
    
    theme = models.CharField(max_length=300, null=True, blank=True)
    medium = MultiSelectField(choices=Medium, validators=[validate_medium_count], default=["online_campaigns"])
    city = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    communication = models.TextField(null=True, blank=True)
    target_audience = models.IntegerField(null=True, blank=True)
    brand = models.ForeignKey(Brands, null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "Awareness Plan"
        
    def __str__(self):
        return f"{self.theme}-{self.city}-{self.date}"
    
class AwarenessPlanPics(Common):
    awarenessplan = models.ForeignKey(AwarenessPlan, on_delete=models.CASCADE)
    pics = models.FileField(upload_to='media/awarenessplan/pics')
    
    class Meta:
        db_table = "Awareness Plan Pics"
        
    def __str__(self):
        return f"{self.awarenessplan.theme}-{self.pics}"
    