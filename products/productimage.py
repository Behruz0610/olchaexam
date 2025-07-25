from django.db import models

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/extra/', blank=False, null=False)
    alt = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"Image for {self.product.name}"
