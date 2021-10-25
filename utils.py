import pandas as pd
import re
import numpy as np
from pd_map_funcs import *

def split_date(csv):
    csv_2001_2010 = csv[(csv['처방일자#3'] >= '2001-01-01') & (csv['처방일자#3'] <= '2010-12-31')]
    csv_2011_2016_06 = csv[(csv['처방일자#3'] >= '2011-01-01') & (csv['처방일자#3'] <= '2016-07-01')]
    csv_2016_06_2020 = csv[(csv['처방일자#3'] >= '2016-07-02') & (csv['처방일자#3'] <= '2020-12-31')]
    return csv_2001_2010, csv_2011_2016_06, csv_2016_06_2020

class csv_parser:
    def __init__(self, csv_path):
        self.csv_path = csv_path
    def read_csv(self):
        self.csv = pd.read_csv(self.csv_path)
        self.csv['처방일자'] = pd.to_datetime(self.csv['처방일자'])
    def cancer_risk_check(self, path):
        cancer = pd.read_excel(path)
        cancer = cancer.query("HLSC_CTRL_CHRC_VL2 == '암확인'")
        self.csv = pd.merge(self.csv, cancer[['CDW_ID', 'ORDR_YMD']], how='left', 
                            left_on=['환자번호'], right_on=['CDW_ID'])
        self.csv['ORDR_YMD'] = pd.to_datetime(self.csv['ORDR_YMD'])
        self.csv = self.csv.assign(cancer_risk = self.csv.apply(lambda x: self.check_day_is_avaliable(x['처방일자'], 
                                                                                                      x['ORDR_YMD']), axis='columns'))
        self.csv = self.csv.drop(['CDW_ID', 'ORDR_YMD'], axis='columns')
        
    def cancer_bx_check(self, path):
        cancer = pd.read_csv(path, encoding='CP949', index_col=0)
        self.csv = pd.merge(self.csv, cancer[['환자번호#1', '처방일자#2']], how='left', 
                       left_on=['환자번호'], right_on=['환자번호#1'])
        self.csv['처방일자#2'] = pd.to_datetime(self.csv['처방일자#2'])
        self.csv = self.csv.assign(cancer_bx = self.csv.apply(lambda x: self.check_day_is_avaliable(x['처방일자'], 
                                                                                               x['처방일자#2']), axis='columns'))
        self.csv = self.csv.drop(['환자번호#1', '처방일자#2'], axis='columns')
        
    def cancer_histology_check(self, path):
        orig_csv = pd.read_csv(path, index_col=0)
        orig_csv = orig_csv[~orig_csv['본원진단일자(최초1) #118'].isna()]
        orig_csv['최초진단일자(최초1) #119'] = pd.to_datetime(orig_csv['최초진단일자(최초1) #119'])
        self.csv = pd.merge(self.csv,  orig_csv[['환자번호#1', '최초진단일자(최초1) #119']], how='left', 
                 left_on=['환자번호'], right_on=['환자번호#1'])
        self.csv = self.csv.assign(cancer_histology = self.csv.apply(lambda x: self.check_day_is_avaliable(x['처방일자'],
                                                                                                      x['최초진단일자(최초1) #119']), axis='columns'))
        self.csv = self.csv.drop(['환자번호#1', '최초진단일자(최초1) #119'], axis='columns')
    
    def check_cancer(self, risk_path, bx_path, histology_path):
        self.cancer_histology_check(histology_path)
        self.cancer_bx_check(bx_path)
        self.cancer_risk_check(risk_path)
        csv = self.csv.assign(cancer = (self.csv['cancer_risk'] == 1) | 
                                           (self.csv['cancer_bx'] == 1 )| 
                                           (self.csv['cancer_histology'] == 1))
        csv['cancer'] = csv['cancer'].replace({True: 1, False: 0})
        return csv
    
    def check_day_is_avaliable(self, day_1, day_2):
        try:
            if (day_2 - day_1).days >= 0:
                return 1
            else:
                return 0
        except AttributeError:
            return 0
        
def fill_bmi(csv, bmi_csv_path):
    bmi_csv = pd.read_csv(bmi_csv_path, index_col=0, encoding='CP949')
    bmi_csv = bmi_csv[bmi_csv['BMI#3'] != 0.00]
    bmi_csv = bmi_csv.drop_duplicates(subset='환자번호#1')
    csv = pd.merge(csv, bmi_csv[['환자번호#1', 'BMI#3']], left_on=['환자번호'],
            right_on=['환자번호#1'], how='left')
    csv['BMI'] = csv['BMI'].fillna(csv['BMI#3'])
    csv = csv.drop('BMI#3', axis='columns')
    return csv

def fill_smoking(csv, smoke_csv_path):
    smoke = pd.read_csv(smoke_csv_path, index_col=0, encoding='CP949')
    smoke = smoke[~smoke['2 귀하는 담배를 피우고 있거나 피우신 적이 있습니까?#4'].isna()]
    smoke = smoke.drop_duplicates(subset='환자번호#1')
    smoke.columns = ['환자번호', '처방날짜', '시행일자', 'smoke']
    smoke['smoke'] = smoke['smoke'].map(lambda x: smoke_map_fn(x))
    csv = pd.merge(csv, smoke[['환자번호', 'smoke']], left_on=['환자번호'],
        right_on=['환자번호'], how='left')
    csv['smoking'] = csv['smoking'].fillna(csv['smoke'])
    csv = csv.drop('smoke', axis='columns')
    return csv

def cal_percent_group(csv, col1, col2):
    temp = csv.groupby([col1, col2])
    t = pd.DataFrame(temp.size())
    percent = {}
    idx = 1
    for i in range(0, len(t.values), 2):
        percent['group {0}'.format(idx)] = float(t.values[i+1] /(t.values[i] + t.values[i+1]))
        idx += 1
    return t, percent

