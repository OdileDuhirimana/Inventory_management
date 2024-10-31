from django.db import models
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    sku = models.CharField(max_length=100, unique=True)
    stock_level = models.PositiveIntegerField()
    reorder_level = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    low_stock_alert = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def needs_reorder(self):
        """Check if product needs to be reordered."""
        return self.stock_level <= self.reorder_level

    def save(self, *args, **kwargs):
        """Override save method to update low_stock_alert before saving."""
        self.low_stock_alert = self.needs_reorder()
        super().save(*args, **kwargs)
