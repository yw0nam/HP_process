# %%
import pandas as pd
import argparse
import os
def define_argparser():
    p = argparse.ArgumentParser()

    p.add_argument('--data_path', required=True)
    p.add_argument('--output_path', required=True)
    config = p.parse_args()

    return config

# %%
config = define_argparser()
csv = pd.read_csv(config.data_path, index_col=0, encoding='CP949')
csv.to_excel(config.output_path, index=False)