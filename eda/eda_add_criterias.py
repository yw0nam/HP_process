# %%
import pandas as pd
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
warnings.filterwarnings("ignore", category=DeprecationWarning) 
pd.set_option('display.max_columns', None)
# %%
csv = pd.read_csv('../data_for_analysis/bx_for_hp.cov.fillna_cancer.up_death.final_fu.add_fu.csv')
csv['cancer_fu_date'] = csv.apply(lambda x: '2021-10-12' if x['cancer_fu'] == 'N' else x['cancer_fu_date'], axis=1)
csv['final_fu_death'] = csv.apply(lambda x: '2021-10-12' if x['사망여부'] == 'N' else x['final_fu_death'], axis=1)
# %%
csv['사망여부'] = csv['사망여부'].replace({'N':0, 'Y':1})
csv['사망여부'] = csv['사망여부'].fillna(0).astype(int)
csv['cancer_fu'] = csv['cancer_fu'].replace({'N':0, 'Y':1})
csv['cancer_fu'] = csv['cancer_fu'].fillna(0).astype(int)
# %%
csv['처방일자'] = pd.to_datetime(csv['처방일자'])
csv['final_fu_death'] = pd.to_datetime(csv['final_fu_death'])
csv['cancer_fu_date'] = pd.to_datetime(csv['cancer_fu_date'])
csv['first_fu'] = pd.to_datetime(csv['first_fu'])
csv['index_date'] = pd.to_datetime(csv['index_date'])
csv['group_merged'] = csv['group'].replace({2: '2 and 3', 3: '2 and 3'})
# %%
fig = plt.figure(figsize=(20, 5))
sns.set_style('dark')
xlim = (0, 7500)
ylim = (0,170)
area1 = fig.add_subplot(1, 4, 1)
area1.set(xlim=xlim, ylim=ylim)
area1.set_title('Group 1 cancer follow up lengths')
area2 = fig.add_subplot(1, 4, 2)
area2.set(xlim=xlim, ylim=ylim)
area2.set_title('Group 2 cancer follow up lengths')
area3 = fig.add_subplot(1, 4, 3)
area3.set(xlim=xlim, ylim=ylim)
area3.set_title('Group 3 cancer follow up lengths')
area4 = fig.add_subplot(1, 4, 4)
area4.set(xlim=xlim, ylim=ylim)
area4.set_title('Group 4 cancer follow up lengths')
sns.histplot(csv.query('group == 1').apply(lambda x: (x['cancer_fu_date'] - x['index_date']).days, axis=1), ax=area1)
sns.histplot(csv.query('group == 2').apply(lambda x: (x['cancer_fu_date'] - x['index_date']).days, axis=1), ax=area2)
sns.histplot(csv.query('group == 3').apply(lambda x: (x['cancer_fu_date'] - x['index_date']).days, axis=1), ax=area3)
sns.histplot(csv.query('group == 4').apply(lambda x: (x['cancer_fu_date'] - x['index_date']).days, axis=1), ax=area4)
# %%
fig = plt.figure(figsize=(20, 5))
sns.set_style('dark')
area1 = fig.add_subplot(1, 4, 1)
area1.set(xlim=xlim, ylim=ylim)
area1.set_title('Group 1 death follow up lengths')
area2 = fig.add_subplot(1, 4, 2)
area2.set(xlim=xlim, ylim=ylim)
area2.set_title('Group 2 death follow up lengths')
area3 = fig.add_subplot(1, 4, 3)
area3.set(xlim=xlim, ylim=ylim)
area3.set_title('Group 3 death follow up lengths')
area4 = fig.add_subplot(1, 4, 4)
area4.set(xlim=xlim, ylim=ylim)
area4.set_title('Group 4 death follow up lengths')
sns.histplot(csv.query('group == 1').apply(lambda x: (x['final_fu_death'] - x['index_date']).days, axis=1), ax=area1)
sns.histplot(csv.query('group == 2').apply(lambda x: (x['final_fu_death'] - x['index_date']).days, axis=1), ax=area2)
sns.histplot(csv.query('group == 3').apply(lambda x: (x['final_fu_death'] - x['index_date']).days, axis=1), ax=area3)
sns.histplot(csv.query('group == 4').apply(lambda x: (x['final_fu_death'] - x['index_date']).days, axis=1), ax=area4)

# %%
csv['hp_exam_count'] = csv['fu_names'].map(lambda x: len(x.split('|'))+1)
csv['fu_length'] = csv.apply(lambda x: (x['final_fu_death'] - x['index_date']).days, axis=1)
# %%
fig = plt.figure(figsize=(20, 5))
sns.set_style('dark')
xlim=(0, 3700)
area1 = fig.add_subplot(1, 4, 1)
area1.set(xlim=xlim, ylim=ylim)
area1.set_title('Group 1 follow up lengths / hp_exam_count')
area2 = fig.add_subplot(1, 4, 2)
area2.set(xlim=xlim, ylim=ylim)
area2.set_title('Group 2 follow up lengths / hp_exam_count')
area3 = fig.add_subplot(1, 4, 3)
area3.set(xlim=xlim, ylim=ylim)
area3.set_title('Group 3 follow up lengths / hp_exam_count')
area4 = fig.add_subplot(1, 4, 4)
area4.set(xlim=xlim, ylim=ylim)
area4.set_title('Group 4 follow up lengths / hp_exam_count')
sns.histplot(csv.query('group == 1').apply(lambda x: x['fu_length'] / x['hp_exam_count'], axis=1), ax=area1)
sns.histplot(csv.query('group == 2').apply(lambda x: x['fu_length'] / x['hp_exam_count'], axis=1), ax=area2)
sns.histplot(csv.query('group == 3').apply(lambda x: x['fu_length'] / x['hp_exam_count'], axis=1), ax=area3)
sns.histplot(csv.query('group == 4').apply(lambda x: x['fu_length'] / x['hp_exam_count'], axis=1), ax=area4)

# %%
year_dict_ls = []
for j in range(3):
    year_dict = dict()
    for i in range(2000, 2022):
        year_dict[str(i)] = 0
    year_dict_ls.append(year_dict)
    
def count_exam_by_year(fu_dates, fu_names, exam):
    fu_date_split = fu_dates.split('|')
    fu_name_split = fu_names.split('|')
    for fu_date, fu_name in zip(fu_date_split, fu_name_split):
        exam_name = exam[fu_name.split('_')[-1]]
        if exam_name == 'EGD':
            year_dict_ls[0][fu_date.split('-')[0]] += 1
        elif exam_name == 'Stomach_Bx':
            year_dict_ls[1][fu_date.split('-')[0]] += 1
        elif exam_name == 'UBT':
            year_dict_ls[2][fu_date.split('-')[0]] += 1
    
exam = {'CZ':'EGD', 'DF':'Stomach_Bx', 'DL':'UBT'}
csv.apply(lambda x: count_exam_by_year(x['fu_dates'], x['fu_names'], exam), axis=1)
# %%
exam_year_count_df = pd.DataFrame(year_dict_ls).T
exam_year_count_df = exam_year_count_df.reset_index()
exam_year_count_df.columns = ['year', 'EGD', 'Stomach_Bx', 'UBT']

# %%
fig = plt.figure(figsize=(12, 12))
sns.set_style('dark')
ylim = (0, 200)
area1 = fig.add_subplot(3, 1, 1)
area1.set_title('EGD count by year')
area2 = fig.add_subplot(3, 1, 2)
area2.set_title('Stomach_Bx count by year')
area3 = fig.add_subplot(3, 1, 3)
area3.set_title('UBT count by year')
area1.bar(exam_year_count_df['year'], exam_year_count_df['EGD'], edgecolor="white")
area1.set(ylim=ylim)
area2.bar(exam_year_count_df['year'], exam_year_count_df['Stomach_Bx'], edgecolor="white")
area2.set(ylim=ylim)
area3.bar(exam_year_count_df['year'], exam_year_count_df['UBT'], edgecolor="white")
area3.set(ylim=ylim)

# %%

eradication_csv_1 = pd.read_csv("../data/HP_drug_1_unlock.csv", 
                              index_col=0, encoding='CP949')
eradication_csv_2 = pd.read_csv("../data/HP_drug_2_unlock.csv", 
                              index_col=0, encoding='CP949')
# %%
erd_1 = eradication_csv_1[['환자번호#1', '처방일자#3']]
erd_2 = eradication_csv_2[['환자번호#1', '처방일자#3']]
erd = pd.concat([erd_1, erd_2])
erd = erd.sort_values(by='처방일자#3')
erd.columns = ['환자번호', '제균일자']
# %%
erd = erd.drop_duplicates(subset='환자번호')

# %%
erd_csv = pd.merge(csv, erd, how='left', left_on=['환자번호'],
         right_on=['환자번호'])
# %%
temp = erd_csv.query('group in (1, 2)')
temp['erdication_date_valid'] = temp['제균일자'].map(lambda x: 'Y' if type(x) == str else 'N')
# %%
temp = temp['erdication_date_valid'].value_counts()
fig1, ax1 = plt.subplots()
ax1.set_title('erdication_date_valid')
plt.pie([temp[0], temp[1]], labels=['Y','N'], autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
# %%
temp = erd_csv[~erd_csv['제균일자'].isna()]
temp['erdication_year'] = temp['제균일자'].map(lambda x: x.split('-')[0]).astype(int)
# %%
f, ax = plt.subplots(figsize=(15, 5))
sns.histplot(data=temp, x='erdication_year', hue='group',  multiple="stack")
ax.set_xticks([i for i in range(2000, 2022)])
# %%
