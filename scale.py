import numpy as np
import pandas as pd
import datetime
import json
from exceptions import DateFormatIsWrong

class Scale:
    def __init__(self, payload):
        self.payload = payload
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    def scaleToDate(self):
        today_date = datetime.datetime.today()
        today_date = today_date.replace(hour=0, minute=0, second=0, microsecond=0)
        _end_date = self.payload['to_date']
        try:
            end_date = datetime.datetime.strptime(_end_date, '%Y-%m-%d')
            df_all_days = pd.DataFrame(index=pd.date_range(start=today_date, end=end_date))
        except:
            raise DateFormatIsWrong('DateFormatIsWrong {}'.format(_end_date), status_code=500)

        
        df_all_days['weekday'] = df_all_days.index.weekday

        # Remove all saturdays and sundays
        df_business_days = df_all_days.copy()
        df_business_days = df_business_days[df_business_days.weekday != 5]
        df_business_days = df_business_days[df_business_days.weekday != 6]

        temp = [0]
        for x in range(1, len(df_business_days)):
            temp.append(np.sqrt(x) * self.payload['risk'])
        
        df_business_days['risk'] = temp

        df_all_days = df_all_days.join(df_business_days['risk'], rsuffix='_')
        df_all_days = df_all_days.fillna(method='ffill')
        df_all_days = df_all_days.drop(['weekday'], axis=1)

        df_all_days['date'] = df_all_days.index
        df_all_days['pair'] = self.payload['pair']
        return df_all_days.to_json(orient='records', date_format='iso').replace('T00:00:00.000Z','')


    def scaleFromDateToDate(self):
        pass
    
    def scaleXdays(self):
        pass
    

    def __scale(self):
        pass