#!~/.conda/envs/vel_percolation/bin/python
import argparse
import numpy as np
import pandas as pd
import os
import datetime as dt
from datetime import datetime
from tqdm import tqdm
from targetDF import *
from extract_ratio_df import *
from CheckOverRatio import *
from SinglePP import *

def ExtractQc(NodeLinkDF, dataset, Year, Month, time_term=10, q_step=False):
    target_times = []
    T_term = time_term # 몇 분 단위로 찾을 것인지
    for hour in range(24):
        for minute in range(0, 60, T_term):
            target_times.append((hour, minute))
            
    year_and_month = [(Year, Month)]
    dates = []
    for y, m in year_and_month:
        d0 = datetime(year=y, month=m, day=1)
        if m == 12:
            m = 0
            y = y+1
    
        d1 = datetime(year=y, month=m+1, day=1)
        monthrange = (d1 - d0).days
        dates.append(np.arange(1, monthrange + 1))
    
    day_list = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    df_qc = {'year':[], 'month':[], 'date':[], 'day':[], 'hour':[], 'min':[], 'q_c':[]}
    incomplete_date = []
    for (year, month), monthrange in tqdm(zip(year_and_month, dates), desc='Year & Month Loop'):
        for date in tqdm(monthrange, desc="Month's date Loop"):
            date_dataset = targetDF(dataset, year, month, date)
            try:
                date_dataset = extract_ratio_df(date_dataset)
            except Warning:
                print("Incomplete date_dataset Found!!  ", year, month, date)
                incomplete_date.append((year, month, date))
                continue

            for hour, minute in tqdm(target_times, desc='Time Loop'):
                time_dataset = targetDF(date_dataset, year, month, date, hour, minute)
                CheckOverRatio(time_dataset, varbose=False)

                # TODO_2: See the function of 'SinglePP'. 
                critical_point = SinglePP(NodeLinkDF, time_dataset, q_step=q_step, plot=False, varbose=False) 

                df_qc['year'].append(year)
                df_qc['month'].append(month)
                df_qc['date'].append(date)
                day = day_list[dt.date(year, month, date).weekday()]
                df_qc['day'].append(day)
                df_qc['hour'].append(hour)
                df_qc['min'].append(minute)
                df_qc['q_c'].append(critical_point)
    
    df_qc = pd.DataFrame(df_qc)
    return df_qc

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Data_Path', type=str, help="Indicate the absolute path including the dataset")
    parser.add_argument('Year', type=int, help="What is the 'Year' you would extract critical points?")
    parser.add_argument('Month', type=int, help="What is the 'Month' you would extract critical points?")
    parser.add_argument('--Prefix', type=str, default=None, help='Prefix_ for .csv filename')
    
    args = parser.parse_args()
    YEAR = args.Year
    MONTH = args.Month
    Prefix = args.Prefix
    DataPath = args.Data_Path
    YM = datetime(YEAR, MONTH, 1)
    YM = YM.strftime("%Y%m")
    FILENAME = 'Qc_' + YM + '.csv'
    if Prefix is not None:
        FILENAME = Prefix + "_" + FILENAME
    
    data_path = []
    for dirname, _, filenames in os.walk(DataPath):
        for file in filenames:
            if file.split("_")[-3] == YM:
                data_path.append(os.path.join(dirname, file))
            
            else:
                continue
                
    dataset = pd.DataFrame()
    for path in data_path:
        if dataset.empty:
            dataset = pd.read_csv(path)
            continue
            
        else:
            data = pd.read_csv(path)
            
        dataset = pd.concat([dataset, data], ignore_index=True)
    
    # TODO: NodeLink DataFrame should be inserted.
    NodeLink = pd.read_excel('STnodeLinks_withRatio.xlsx', engine='openpyxl')
    df_qc = ExtractQc(NodeLink, dataset, int(YEAR), int(MONTH), time_term=10, q_step=False)
    df_qc.to_csv(FILENAME, mode='w', index=False)
    print(FILENAME, " has saved on ", os.getcwd())