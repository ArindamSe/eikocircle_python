from rest_framework import serializers

from Item.models import Item, ItemMaterialRecoveryReport, ItemProofOfDelivery, ItemRecyclingCertificate, ItemSalePurchaseInvoice

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'item_code', 'created_by', 'updated_by']
        
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }
        
    def save(self, **kwargs):
        item = super().save()
        sale_purchase_invoice = self.context.get("salepurchaseinvoice")
        proof_of_delivery = self.context.get("proofofdelivery")
        material_recovery_report = self.context.get("materialrecoveryreport")
        recycling_certificate = self.context.get("recyclingcertificate")
        
        if sale_purchase_invoice:
            sale = [
                ItemSalePurchaseInvoice(item=item, salepurchaseinvoice=file) for file in sale_purchase_invoice
            ]
            ItemSalePurchaseInvoice.objects.bulk_create(sale)
            
        if proof_of_delivery:
            proof = [
                ItemProofOfDelivery(item=item, proofofdelivery=file) for file in proof_of_delivery
            ]
            ItemProofOfDelivery.objects.bulk_create(proof)
            
        if material_recovery_report:
            material = [
                ItemMaterialRecoveryReport(item=item, materialrecoveryreport=file) for file in material_recovery_report
            ]
            ItemMaterialRecoveryReport.objects.bulk_create(material)
            
        if recycling_certificate:
            recycling = [
                ItemRecyclingCertificate(item=item, recyclingcertificate=file) for file in recycling_certificate
            ]
            ItemRecyclingCertificate.objects.bulk_create(recycling)
            
        return item
        
