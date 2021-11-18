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
csv = pd.read_csv('./data_for_analysis/hp_bx.csv')
csv['처방일자'] = pd.to_datetime(csv['처방일자'])
csv['first_fu'] = pd.to_datetime(csv['first_fu'])
csv['last_fu'] = pd.to_datetime(csv['last_fu'])
# csv['사망일'] = csv['사망일'].map(lambda x: x.split()[0] if type(x) == str else None)
# %%
# csv.loc[6177]
# %%
# csv['사망일'].loc[6177] = '2100-12-31' # 사망일이 2999-12-31로 적혀있음
# csv['사망일'] = pd.to_datetime(csv['사망일'])
# csv['암확인일자'] = pd.to_datetime(csv['암확인일자'])
# csv_3 = csv.query('last_fu != first_fu')
# %%
csv['fu_days_2'] = (csv['last_fu'] - csv['first_fu']).map(lambda x: x.days)
csv['fu_days_1'] = (csv['first_fu'] - csv['처방일자']).map(lambda x: x.days)
csv['final_fu'] 
# %%
expr = '(fu_days_1 < 1825) and (fu_days_1 > 365)'
temp = csv.query(expr)
sns.histplot(temp['fu_days_1'])
# %%
sns.histplot(temp['fu_days_2'])
# %%
# csv_3 = csv_3.drop('fu_days', axis=1)
csv_3_fu_365 = csv_3.query('fu_days_1 >= 365').query('fu_days_2 >= 365')
# %%
# Study Enroll(첫번째 Follow up) 이전에 cancer인 사람이있는지 확인
csv_3_fu_365[(csv_3_fu_365['처방일자'] -csv_3_fu_365['암확인일자']).map(lambda x: x.days).map(lambda x: x > 0)]
# %%
# Study Enroll(첫번째 Follow up) 이전에 사망한 사람이있는지 확인
csv_3_fu_365[(csv_3_fu_365['처방일자'] - csv_3_fu_365['사망일']).map(lambda x: x.days).map(lambda x: x > 0)]
# %%
# Study Enroll(첫번째 Follow up) 이후 1년이내에 cancer가 있는지 확인
csv_3_fu_365[(csv_3_fu_365['처방일자'] -csv_3_fu_365['암확인일자']).map(lambda x: x.days).map(lambda x: abs(x) <= 365)]
# %%
# Study Enroll(첫번째 Follow up) 이후 1년이내에 사망이 있는지 확인
csv_3_fu_365[(csv_3_fu_365['처방일자'] - csv_3_fu_365['사망일']).map(lambda x: x.days).map(lambda x: abs(x) <= 365)]
# %%
# 2번째 Follow up 이후 1년이내에 암이 있는지 확인
csv_3_fu_365[(csv_3_fu_365['first_fu'] -csv_3_fu_365['암확인일자']).map(lambda x: x.days).map(lambda x: abs(x) <= 365)]
# %%
# 2번째 Follow up 이후 1년이내에 사망이 있는지 확인
csv_3_fu_365[(csv_3_fu_365['first_fu'] -csv_3_fu_365['사망일']).map(lambda x: x.days).map(lambda x: abs(x) <= 365)]
# %%
# %%
fig = plt.figure(figsize=(20, 5))
sns.set_style('dark')
area1 = fig.add_subplot(1, 4, 1)
area1.set_title('Group 1 first follow up lengths')
area2 = fig.add_subplot(1, 4, 2)
area2.set_title('Group 2 first follow up lengths')
area3 = fig.add_subplot(1, 4, 3)
area3.set_title('Group 3 first follow up lengths')
area4 = fig.add_subplot(1, 4, 4)
area4.set_title('Group 4 first follow up lengths')
sns.histplot(csv_3_fu_365.query('group == 1')['fu_days_1'], ax=area1)
sns.histplot(csv_3_fu_365.query('group == 2')['fu_days_1'], ax=area2)
sns.histplot(csv_3_fu_365.query('group == 3')['fu_days_1'], ax=area3)
sns.histplot(csv_3_fu_365.query('group == 4')['fu_days_1'], ax=area4)
plt.show()
# %%
fig = plt.figure(figsize=(20, 5))
sns.set_style('dark')
area1 = fig.add_subplot(1, 4, 1)
area1.set_title('Group 1 second follow up lengths')
area2 = fig.add_subplot(1, 4, 2)
area2.set_title('Group 2 second follow up lengths')
area3 = fig.add_subplot(1, 4, 3)
area3.set_title('Group 3 second follow up lengths')
area4 = fig.add_subplot(1, 4, 4)
area4.set_title('Group 4 second follow up lengths')
sns.histplot(csv_3_fu_365.query('group == 1')['fu_days_2'], ax=area1)
sns.histplot(csv_3_fu_365.query('group == 2')['fu_days_2'], ax=area2)
sns.histplot(csv_3_fu_365.query('group == 3')['fu_days_2'], ax=area3)
sns.histplot(csv_3_fu_365.query('group == 4')['fu_days_2'], ax=area4)
plt.show()
# %%
t = pd.read_csv('./data_for_analysis/any_bx.all.group.csv')
# %%
t = t[['환자번호#1', '처방일자#12', '검사코드#13', '검사코드#18', '처방일자#21', '검사코드#22', 
   '검사코드#26', '검사코드(최초1) #102', '검사코드(최초1) #108', 
   '검사코드(최초1) #114']]
t['검사코드#22'] = t[t['처방일자#12'] != t['처방일자#21']]['검사코드#22']
# %%
t = t.drop(['처방일자#12', '처방일자#21'], axis=1)
# %%
t['exam_count'] = t.apply(lambda x: x.drop('환자번호#1').isna().sum(), axis=1)
# %%
csv_3_fu_365 = pd.merge(csv_3_fu_365, t[['환자번호#1', 'exam_count']], how='left',
         left_on='환자번호', right_on='환자번호#1').drop('환자번호#1', axis=1)

# %%
csv_3_fu_365['사망여부'] =csv_3_fu_365['사망여부'].fillna('N')
cols = ['age', 'BMI', 'CCI', 'Hb', 'TG', 
                'HDL', 'LDL', 'glucose', 'fu_days_1', 'fu_days_2',
                'sex', 'smoking', 'alcohol_drinking', 
                'physical_activity', 'EGD', 'Adenoma', 'cancer', '사망여부', 'exam_count']

category_cols = ['sex', 'smoking', 'alcohol_drinking', 
                'physical_activity', 'EGD', 'Adenoma'
                 , 'cancer', '사망여부', 'exam_count']

mytable = TableOne(csv_3_fu_365, columns=cols, categorical=category_cols,
                   groupby='group', pval=True, nonnormal='bili')
# %%
print(mytable.tabulate(tablefmt="rst"))
# %%
csv_3_fu_365.to_csv('./data_for_analysis/hp_bx.fu_1_2_365.fu_cdw.exam_count.csv', index=False)
# %%
