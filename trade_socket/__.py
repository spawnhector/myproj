import os
import sys
from pathlib import Path

# os.system('python trade_socket/hectperconnbind.py')
os.system('python trade_socket/connectToDjango.py')

# import sys
# from pathlib import Path
# import sysconfig
# # print(sysconfig.get_path("purelib"))
# ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# fy = f"{ROOT_DIR}app/"
# sys.path.append(str(fy))
# print(sys.path)
# os.system('pip list')

# # get the current working directory

# # from pathlib import Path
# # current_dir = os.getcwd()

# # # get the parent directory
# print(fy)
# parent_dir = os.path.dirname(fy)

# # # list all folders in the parent directory
# folders = [folder for folder in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, folder))]

# # # print the folders
# print(os.listdir(parent_dir))
