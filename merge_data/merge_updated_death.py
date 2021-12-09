# %%
import pandas as pd
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
csv = pd.read_csv('../%s/%s.cov.fillna_cancer.csv'%(config.folder, config.dataset_name))
death = pd.read_excel('../etc_data/건진사망자추가데이터_211007 기준.xlsx')
# %%
csv = pd.merge(csv, death, how='left',
         left_on='환자번호', right_on='CDW_ID').drop('CDW_ID', axis=1)
#%%
csv['사망일'] = csv['사망신고일'].fillna(csv['사망일'])
csv = csv.drop('사망신고일', axis=1)
csv['사망여부'] = csv['사망일'].map(lambda x: 'Y' if type(x) == str else None)
csv['cancer'] = csv['cancer_date'].map(lambda x: 'Y' if type(x) == str else None)
# %%
csv.to_csv('../%s/%s.cov.fillna_cancer.up_death.csv'%(config.folder, config.dataset_name), index=False)
# %%
