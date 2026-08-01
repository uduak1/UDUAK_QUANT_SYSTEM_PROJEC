import os
import sys

print("Current working directory:")
print(os.getcwd())

print("\nScript directory:")
print(os.path.dirname(__file__))

print("\nPython search path:")

for path in sys.path:
    print(path)