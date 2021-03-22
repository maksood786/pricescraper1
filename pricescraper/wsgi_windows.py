import os
import sys
import site
from django.core.wsgi import get_wsgi_application

# add python site packages, you can use virtualenvs also
site.addsitedir("C:/Users/Maksood.Alam/Anaconda3/Lib/site-packages")

# Add the app's directory to the PYTHONPATH
sys.path.append('D:/Python/Django/Practice/pricescraper')
sys.path.append('D:/Python/Django/Practice/pricescraper/pricescraper')

os.environ['DJANGO_SETTINGS_MODULE'] = 'pricescraper.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricescraper.settings")

application = get_wsgi_application()
