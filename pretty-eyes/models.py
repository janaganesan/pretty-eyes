from django.db import models

class Order(models.Model):
    order_id = models.CharField(max_length=200)

    def __str__(self):
        return self.order_id

class History(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    history = models.TextField()
