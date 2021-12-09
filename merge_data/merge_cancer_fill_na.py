# %%
import pandas as pd
from utils import *
import argparse
pd.set_option('display.max_columns', None)

def define_argparser():
    p = argparse.ArgumentParser()

    p.add_argument('--folder', required=True)
    p.add_argument('--dataset_name', required=True)
    config = p.parse_args()

    return config
# %%
config = define_argparser()
parser = csv_parser('../%s/%s.cov.csv'%(config.folder, config.dataset_name))
parser.read_csv()
# %%
csv = parser.check_cancer(risk_path='../etc_data/건진 CANCER 관리 대상자-위암_2021_10_12.xlsx',
                         bx_path='../etc_data/hp_stomach_cancer.csv',
                        histology_path='../data/apply_exclusion.csv')
# %%
csv = fill_bmi(csv, bmi_csv_path='../etc_data/HP-bmi.csv')
csv = fill_smoking(csv, smoke_csv_path='../etc_data/HP-smoking-missing.csv')
# %%
if 'Unnamed: 0' in csv.columns:
    csv = csv.drop('Unnamed: 0', axis='columns')
csv = csv.drop(['환자번호#1', 'cancer_date_histology', 'cancer_date_bx', 'cancer_date_risk'], axis='columns')
csv = csv.drop_duplicates(subset='환자번호')

# %%
csv.to_csv('../%s/%s.cov.fillna_cancer.csv'%(config.folder, config.dataset_name), index=False)