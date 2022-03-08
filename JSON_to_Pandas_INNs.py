import pandas as pd

#Перегоняем из json с компаниями у которых главный ОКВЭД - 25.9
okved_259000 = pd.read_json('okved_259000_companies_only_main_okved.json')
okved_259000 = okved_259000.transpose()

okved_259000_df = pd.DataFrame(columns=['INN', 'OGRN'])

for j in okved_259000['companies_list']:
    for i in j:
        df_temp = pd.DataFrame({'INN': i['inn'],
                                'OGRN': i['ogrn']}, index=[0])
        okved_259000_df = okved_259000_df.append(df_temp) 

#okved_259000_df #датафрейм с основными компаниями с оквэд 25.9

#Перегоняем из json с доп компаниями 22197
okved_22197 = pd.read_json('okved_22197_companies_not_only_main_okved.json')
okved_22197 = okved_22197.transpose()

okved_22197_df = pd.DataFrame(columns=['INN', 'OGRN'])

for j in okved_22197['companies_list']:
    for i in j:
        df_temp = pd.DataFrame({'INN': i['inn'],
                                'OGRN': i['ogrn']}, index=[0])
        okved_22197_df = okved_22197_df.append(df_temp) 

#okved_22197_df #датафрейм с доп компаниями с оквэд 22.19.7

#Перегоняем из json с доп компаниями 2594000
okved_259400 = pd.read_json('okved_259400_companies_not_only_main_okved.json')
okved_259400 = okved_259400.transpose()

okved_259400_df = pd.DataFrame(columns=['INN', 'OGRN'])

for j in okved_259400['companies_list']:
    for i in j:
        df_temp = pd.DataFrame({'INN': i['inn'],
                                'OGRN': i['ogrn']}, index=[0])
        okved_259400_df = okved_259400_df.append(df_temp) 

#okved_259400_df #датафрейм с доп компаниями с оквэд 25.9.4
