# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tableone import TableOne
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
pd.set_option('display.max_columns', None)

# %%
csv = pd.read_csv('../data_for_analysis/')
csv['처방일자'] = pd.to_datetime(csv['처방일자'])
csv['first_fu'] = pd.to_datetime(csv['first_fu'])
csv['last_fu'] = pd.to_datetime(csv['last_fu'])
