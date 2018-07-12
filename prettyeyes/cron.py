import time
import re

from .models import Order, Report
from django_cron import CronJobBase, Schedule
from .config import read_config, write_config

class ReadLogFileCron(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'prettyeyes.sampleCron'

    def clear_db(self):
        Report.objects.all().delete()
        Order.objects.all().delete()

    def logfile(self):
        config = read_config()
        if config['logfile'] != '':
            return config['logfile']
        time.sleep(0.5)
        return None

    def follow(self):
        logfile = None
        while True:
            if logfile is None:
                logfile = self.logfile()
                continue
            with open(logfile, "r") as f:
                try:
                    while True:
                        try:
                            #if logfile != self.logfile():
                            #    self.clear_db()
                            #    logfile = None
                            #    break
                            line = f.readline()
                        except FileNotFoundError:
                            time.sleep(2)
                            break
                        except:
                            continue
                        if not line:
                            time.sleep(0.1)
                            continue
                        yield line
                except Exception as e:
                    print(e)
                    pass

    def do(self):
        self.clear_db()
        write_config({'logfile': '', 'filters': {}})
        pattern_to_match = ("order_submitter_inl", "ExecutionReport")
        for line in self.follow():
            if any(x in line for x in pattern_to_match) is True:
                r = re.search("\sorder_id=(\S+)", line)
                if r is not None and 'source=SOURCE_NIMBUS' not in line:
                    order_id = r.group(1)
                    print(order_id)
                    if Order.objects.filter(order_id=order_id).exists() is False:
                        o = Order(order_id=order_id)
                        o.save()
                    order = Order.objects.get(order_id=order_id)
                    Report.objects.create(order=order, history=line)
