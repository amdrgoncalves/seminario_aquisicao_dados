import requests
import json
import csv
import datetime


# Salvar dados da API
def salvar_dados_api(BASE_DIR, params):
    r = requests.get('https://www.alphavantage.co/query',params=params)
    data = r.json()
    with open(BASE_DIR + 'data/msft.json', 'w') as outfile:
        json.dump(data, outfile)
    return 'ok'

def escrever_csv(BASE_DIR,data):
    filename = 'msft_%s.csv' % (datetime.datetime.now())
    with open(BASE_DIR + 'data/' + filename  , 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(['Hora','Open','High','Low','Close','Volume'])
        for time,values in data['Time Series (15min)'].items():
            spamwriter.writerow([time,values['1. open'],values['2. high'],values['3. low'],values['4. close'],values['5. volume']])
    return 'ok'


def transformar_dados_csv(BASE_DIR):
    with open(BASE_DIR + 'data/msft.json') as json_file:
        data = json.load(json_file)
        escrever_csv(BASE_DIR,data)

if __name__ == '__main__':
    BASE_DIR = '/home/alexandre/seminario_python/AV_api/'

    params = {
    'function':'TIME_SERIES_INTRADAY',
    'symbol':'MSFT',
    'interval':'15min',
    'apikey':'0TNJ2QLAA8B9V22G'
    }
    salvar_dados_api(BASE_DIR,params)
    transformar_dados_csv(BASE_DIR)
    print('ok')
