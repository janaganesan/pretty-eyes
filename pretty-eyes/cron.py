from .models import Order, History
from django_cron import CronJobBase, Schedule
import os
import time
import re
import pdb

class ReadLogFileCron(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'pretty-eyes.sampleCron'

    def follow(self, name):
        with open(name, "r") as f:
            while True:
                try:
                    line = f.readline()
                except:
                    continue
                if not line:
                    time.sleep(0.1)
                    continue
                yield line

    def do(self):
        History.objects.all().delete()
        Order.objects.all().delete()
        fname = "/Users/jganesan/Downloads/OC_cme.log"
        for line in self.follow(fname):
            r = re.search("order_id=(\S+)", line)
            if r is not None:
                order_id = r.group(1)
                if Order.objects.filter(order_id=order_id).exists() is False:
                    o = Order(order_id=order_id)
                    o.save()
                order = Order.objects.get(order_id=order_id)
                History.objects.create(order=order, history=line)
                print(len(Order.objects.all()))
