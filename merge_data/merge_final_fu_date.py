# %%
import pandas as pd
pd.set_option('display.max_columns', None)
# %%
csv_admission = pd.read_csv('./etc_data/hp_base_입원.csv', index_col=0, encoding='CP949')
# csv_admission.head()
csv_admission = csv_admission.drop('처방일자#2', axis=1)
csv_admission.columns = ['환자번호', 'final_observe_admission']
# %%
csv_screening = pd.read_csv('./etc_data/hp_base_건진.csv', index_col=0, encoding='CP949')
# csv_screening.head()
csv_screening = csv_screening.drop('처방일자#2', axis=1)
csv_screening.columns = ['환자번호', 'final_observe_screening']
# %%
csv_outpatient = pd.read_csv('./etc_data/hp_base_외래.csv', index_col=0, encoding='CP949')
# csv_outpatient.head()
csv_outpatient.columns = ['환자번호', 'final_observe_outpatient']
# %%
temp = pd.merge(csv_screening, csv_outpatient, how='left', left_on='환자번호',
         right_on='환자번호')
temp = pd.merge(temp, csv_admission, how='left',left_on='환자번호',
         right_on='환자번호')
# %%
temp['final_observe_screening'] = pd.to_datetime(temp['final_observe_screening'])
temp['final_observe_admission'] = pd.to_datetime(temp['final_observe_admission'])
temp['final_observe_outpatient'] = pd.to_datetime(temp['final_observe_outpatient'])
# %%
temp['final_fu_cdw'] = temp.apply(lambda x: max(x['final_observe_screening'], 
           x['final_observe_outpatient'], x['final_observe_admission']), axis=1)
# %%
csv = pd.read_csv('./data_for_analysis/bx_for_hp.cov.fillna_cancer.up_death.csv')
csv = pd.merge(csv, temp[['환자번호', 'final_fu_cdw']], how='left', left_on='환자번호',
         right_on='환자번호')

# %%
csv.to_csv('./data_for_analysis/bx_for_hp.cov.fillna_cancer.up_death.final_fu.csv', index=False)
# %%
