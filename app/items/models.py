from django.db import models
from app.event.models import Event 
from django.contrib.auth.models import User 

class ItemList(models.Model):
    
    event = models.OneToOneField(
        Event, 
        on_delete=models.CASCADE, 
        related_name="item_list", 
        verbose_name="Event"
    )

    title = models.CharField(max_length=100, default="Lista de articulos")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Lista para {self.event.name}"

class Item(models.Model): 

    class Status(models.TextChoices): 
        PENDING = "pending"
        COMPLETED = "completed"

    item_list = models.ForeignKey(
        ItemList, 
        on_delete=models.CASCADE, 
        related_name='items', 
        verbose_name='Lista'
    )

    name = models.CharField(max_length=100)
    responsible = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='responsible_items', 
        verbose_name='responsible'
    )

    status = models.CharField(
        max_length=10, 
        choices=Status.choices, 
        default=Status.PENDING
    )

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return f"{self.name} - {self.get_status_display()}"
