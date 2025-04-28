# finance/models.py
import datetime
from django.db import models
from django.contrib.auth.models import User  # Add this import

class Category(models.Model):
    name = models.CharField(max_length=255)

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()  # 1 (Jan) to 12 (Dec)
    year = models.IntegerField(default=datetime.datetime.now().year)   # 2025, 2026 etc
    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year}: {self.amount}"