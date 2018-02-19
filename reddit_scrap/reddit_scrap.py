import requests
from bs4 import BeautifulSoup
import datetime
import csv



def save_page(BASE_DIR):

    # pega o html. Checa se é pagina de erro. Se não for salva página. Se for pega o tempo de espera, aguarda e tenta novamente.
    # Se não conseguir pegar o  tempo de espera printa erro

    r = requests.get('https://www.reddit.com/r/microsoft/')

    soup = BeautifulSoup(r.text, 'html.parser')
    if soup.title.text  != 'Too Many Requests':
        text_file = open(BASE_DIR + "data/msft_reddit.html", "w")
        text_file.write(r.text)
        text_file.close()
    else:

        time_wait = int(soup.find_all('p')[2].text.split(' ')[2])
        time.sleep(time_wait+2)
        save_page(BASE_DIR)

            # print('erro')

    return 'ok'

def extrair_dados(BASE_DIR):
    #abrindo html e salvando em variavel
    with open (BASE_DIR + 'data/msft_reddit.html', "r") as html_file:
        data=html_file.read()
    #salvando variavel na sopa
    soup = BeautifulSoup(data, 'html.parser')

    #pegando os topics
    table = soup.find(id="siteTable")
    topics = table.find_all('div',{'data-context':'listing'})

    #abrindo csv
    filename = 'msft_reddit_' + str(datetime.datetime.now())

    with open(BASE_DIR + 'data/' + filename  , 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        #titulos
        writer.writerow(['Hora','Titulo'])
        for topic in topics:
            #extrair titulo e hora dos topicos
            title_topic = topic.find('a',{'data-event-action':'title'}).text
            time_topic = topic.find('time')['datetime']
            #escrever no arquivo
            writer.writerow([time_topic,title_topic])




    return 'ok'


if __name__ == '__main__':

    BASE_DIR = '/home/alexandre/seminario_python/reddit_scrap/'
    save_page(BASE_DIR)
    extrair_dados(BASE_DIR)
