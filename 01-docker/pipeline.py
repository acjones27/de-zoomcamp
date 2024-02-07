import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import pandas as pd

print(sys.argv)

day = sys.argv[1]  # First argument
# Do some stuff

print(f"Job finished successfully for day = {day}!")
