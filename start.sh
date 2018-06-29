python3 manage.py migrate django_cron
python3 manage.py makemigrations prettyeyes
python3 manage.py migrate prettyeyes
python3 manage.py runcrons prettyeyes.cron.ReadLogFileCron --force

