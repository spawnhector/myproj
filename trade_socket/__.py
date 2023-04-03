import os
import sys
from pathlib import Path
import django

current_path = Path(__file__).parent.resolve()
parent_dir = os.path.dirname(current_path)
sys.path.append(str(parent_dir))
# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

os.system('python trade_socket/connectToDjango.py')
