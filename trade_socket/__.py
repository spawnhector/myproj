import os
import sys
from pathlib import Path

current_path = Path(__file__).parent.resolve()
parent_dir = os.path.dirname(current_path)
sys.path.append(str(parent_dir))

os.system('python trade_socket/connectToDjango.py')
