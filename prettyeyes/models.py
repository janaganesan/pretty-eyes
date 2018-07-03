import json

from django.db import models
from .parse_log import parse_text

class Order(models.Model):
    order_id = models.CharField(max_length=200)

    def __str__(self):
        return self.order_id


class Report(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    history = models.TextField()
    name_text = models.CharField(max_length=200, default='')
    json_text = models.TextField(default='')

    def __str__(self):
        return self.history

    def json(self):
        if self.json_text == '':
            self.json_text = json.dumps(parse_text(self.history))
            self.save(update_fields=['json_text'])
        return self.json_text

    def report_json(self):
        return json.loads(self.json())

    def name(self):
        if self.name_text == '':
            name = []
            json_text = self.report_json()
            name.append(json_text['report_type'])
            for field in ('exec_type', 'side'):
                if field in json_text['report']:
                    name.append(json_text['report'][field])
            self.name_text = ' '.join(name)
            self.save(update_fields=['name_text'])
        return self.name_text
