from django.contrib import admin

from recycling_center.models import RecyclingCenter, ItemRecycled

admin.site.register(RecyclingCenter)
admin.site.register(ItemRecycled)