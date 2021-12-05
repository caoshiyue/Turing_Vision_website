##
# Author:
# Description:
# LastEditors: Shiyuec
# LastEditTime: 2021-12-02 22:52:10
##

import numpy as np
from image.user import *
import pandas as pd
from django.db.models import Avg, Max, Min, Count, Sum,Subquery,QuerySet
leaderboard_file = 'static/leaderboard.csv'


def generate_leaderboard_tofile():
    p=Submissions.objects.raw('''
    SELECT id, human, a.modelname, ap, ap50, ap75, aps, apm, apl, paper_url, timestamp FROM submissions as a, 
    (select modelname, 
    max(ap) as max_ap from submissions group by modelname) as b 
    WHERE a.modelname = b.modelname and a.ap = b.max_ap 
    ORDER BY ap DESC
    ''')
    #p=Submissions.objects.raw('''SELECT * FROM submissions''')
    df = pd.DataFrame([item.__dict__ for item in p[:100]])
    df=df.drop(columns='_state')
    df['ap']=round(df['ap'],2)
    df['ap50']=round(df['ap50'],2)
    df['ap75']=round(df['ap75'],2)
    df['aps']=round(df['aps'],2)
    df['apm']=round(df['apm'],2)
    df['apl']=round(df['apl'],2)
    for i,d in enumerate(df['timestamp']) :
        df['timestamp'][i]=d.date()
    df.to_csv(leaderboard_file, index=False)



def read_leaderboard_file():
    df = pd.read_csv(leaderboard_file)
    all_num=len(Submissions.objects.all())
    human_num=len(Submissions.objects.filter(human=1))
    machinenum=all_num-human_num
    return {
        'all_num':all_num,
        'human_num':human_num,
        'machine_num':machinenum,
        'df':df}
