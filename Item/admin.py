from django.contrib import admin

from Item.models import Item, ItemSalePurchaseInvoice, ItemProofOfDelivery, ItemMaterialRecoveryReport, ItemRecyclingCertificate

admin.site.register(Item)
admin.site.register(ItemSalePurchaseInvoice)
admin.site.register(ItemProofOfDelivery)
admin.site.register(ItemMaterialRecoveryReport)
admin.site.register(ItemRecyclingCertificate)