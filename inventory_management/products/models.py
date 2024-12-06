from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="No description")
    sku = models.CharField(max_length=100, unique=True)
    stock_level = models.PositiveIntegerField()
    reorder_level = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    low_stock_alert = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns a string representation of the Product.
        """
        return self.name

    def needs_reorder(self):
        """
        Determines if the product needs to be reordered by comparing stock_level
        and reorder_level. Returns False if either value is None, otherwise compares
        the two values.
        """
        if self.stock_level is None or self.reorder_level is None:
            return False  # You can return True if it's preferable when values are None
        return self.stock_level <= self.reorder_level

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically update the low_stock_alert field 
        based on the needs_reorder method before saving the product.
        """
        # Update low_stock_alert before saving
        self.low_stock_alert = self.needs_reorder()
        # Call the parent save method to save the instance
        super().save(*args, **kwargs)
