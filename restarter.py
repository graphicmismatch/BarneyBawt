from time import sleep
import os
from os import system
import random

sleep(7)
os.environ["port"] = str(random.randint(1000, 9999))
print(os.getenv("port"));
system("python main.py")
