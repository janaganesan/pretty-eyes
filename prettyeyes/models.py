import re

from django.db import models

class Order(models.Model):
    order_id = models.CharField(max_length=200)

    def __str__(self):
        return self.order_id

class History(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    history = models.TextField()

    def __str__(self):
        return self.history

    def name(self):
        name = []
        for type in ("NewOrderSingle", "OrderCancelReplaceRequest", "OrderCancelRequest", "ExecutionReport"):
            if type in self.history:
                name.append(type)
        r = re.search("exec_type=(\S+)", self.history)
        if r is not None:
            name.append(r.group(1))
        r = re.search("side=(\S+)", self.history)
        if r is not None:
            name.append(r.group(1))
        return ' '.join(name)
