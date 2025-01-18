from django.db import models
from users.models import CustomUser

# Create your models here.

RARITY = [
            ("common", "Common"),
            ("uncommon", "Uncommon"),
            ("rare", "Rare"),
            ("epic", "Epic"),
            ("legendary", "Legendary")
        ]

class Accessory(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Name of the accessory")
    description = models.TextField(blank=True, help_text="Description of the accessory")
    image_filename = models.CharField(max_length=255, help_text="Relative path to the image file.")
    rarity = models.CharField(
        max_length=50,
        choices=RARITY,
        default="common",
        help_text="Rarity of the accessory"
    )
    
    def __str__(self):
        return self.name
    
class UserAccessory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_accessories')
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, related_name='user_accessories')
    quantity = models.PositiveIntegerField(default=1, help_text="Number of this accessory the user owns")
    number_used = models.PositiveIntegerField(default=0, help_text="Number of this accessory the user has used")
    
    class Meta:
        unique_together = ("user", "accessory")
        
    def use_accessory(self, amount):
        """Use a specified number of accessories."""
        if amount > (self.quantity - self.number_used):
            raise ValueError("Not enough unused accessories available.")
        self.number_used += amount
        self.save()

    def stop_using_accessory(self, amount):
        """Stop using a specified number of accessories."""
        if amount > self.number_used:
            raise ValueError("Cannot stop using more accessories than are currently in use.")
        self.number_used -= amount
        self.save()

    def __str__(self):
        return f"{self.user.display_name} owns {self.quantity}x {self.accessory.name} (Using: {self.number_used})"
        