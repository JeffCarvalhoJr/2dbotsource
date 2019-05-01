import urllib
from urllib.request import Request, urlopen
import re
from bs4 import *
from PIL import Image, ImageDraw, ImageFont
from resizeimage import resizeimage
from math import sqrt
import math

class bot:

        def censorsearch(img0):

                print("Procurando Censuras...")
                y,x = img0.size
                img = img0.load()
                sn = 0                 
                s1 = []
                print("Imagem carregada!")

                for j in range (x):             #Corremos pela imagem achando os quadrados da censura
                        for i in range (y):     #Tais quadrados devem ser em vermelho 255,0,0
                        
                                c1,c2,c3,c4 = (0,0),(0,0),(0,0),(0,0)
                                hold = i,j
                                
                                if (img[i,j] == (255,0,0) and
                                img[i-1,j] != (255,0,0) and img[i,j-1] != (255,0,0) and img[i-1,j-1] != (255,0,0) and
                                img[i+1,j] == (255,0,0) and img[i,j+1] == (255,0,0) and img[i+1,j+1] == (255,0,0)):
                                        c1 = i,j
                                        a, b = c1
                                        
                                        while True:
                                                if img[a,b] == (255,0,0):
                                                        a = a + 1
                                                else:
                                                        c2 = a-1,b
                                                        break
                        
                                        a, b = c2
                                        while True:
                                                if img[a,b] == (255,0,0):
                                                        b = b + 1
                                                else:
                                                        c3 = a,b-1
                                                        break

                                        a, b = c1
                                        c, d = c3
                                        c4 = a,d
                                        sn = sn + 1
                                        cor = c1,c2,c3,c4
                                        s1.append(cor)
                                        i = i + 1
                print("Done! Censuras encontradas!")
                return s1,sn #Retorna as coordenadas das censuras e quantas são

        def inflacaoD(img, s1, j):

                from bancocentral import Inflacao

                print("Buscando dados sobre inflação...")

                c1,c2,c3,c4 = s1[j]
                a,b = c1
                c,d = c2
                e,f = c3                                        #Abre a imagem e seleciona a censura que sera usada
                g,h = c4
                xs = int(sqrt( (a - c)**2 + (b - d)**2 ))
                ys = int(sqrt( (c - e)**2 + (d - f)**2 ))

                print("Abrindo smug.png")
                box = Image.open("inflation.png").convert('RGB') #Abre imagem que sera usada como fundo
                d = ImageDraw.Draw(box)
                        
                inflacao = Inflacao()
                inf = str(inflacao.get_meta_tax())
                fnt = ImageFont.truetype('TNR.ttf', 30)
                d.text((20,15), "Nesse exato instante a" +"\n"+"       inflação é de", font = fnt, fill=(90,90,90))
                fnt = ImageFont.truetype('TNR.ttf', 45)
                d.text((18,80), "       " + inf + "%              ", font = fnt, fill=(30,30,30))

                inf = str(inflacao.get_acumulada_tax())                 #Nos utilizamos da API do bancocentral para achar os dados
                fnt = ImageFont.truetype('TNR.ttf', 26)
                d.text((23,130), "A inflação acumulada é"+"\n"+"           de ", font = fnt, fill=(90,90,90))
                d.text((134,157), inf +"%.", font = fnt, fill=(30,30,30))

                print("Redimensionando smug.png")
                resizedbox0 = box.resize((xs+1,ys+1), Image.ANTIALIAS)
                resizedbox = resizedbox0.load()
                print("Salvando quadro...")
                
                for j in range (xs+1):
                        for k in range (ys+1):
                                img[j+a,k+b]=resizedbox[j,k]  #Colocamos a recem criada imagem com as informações 
                                                              #No lugar da censura

                return img   

        def cambiosD(img, s1, j, ender):
                
                c1,c2,c3,c4 = s1[j]
                a,b = c1
                c,d = c2
                e,f = c3
                g,h = c4
                xs = int(sqrt( (a - c)**2 + (b - d)**2 ))
                ys = int(sqrt( (c - e)**2 + (d - f)**2 ))
             

                
                nomes = ['     A Libra Esterlina',' O DogeCoin','  O BitCoin','O Ethereum',' O LiteCoin','   O Ripple',
                'O BTC Cash', ' O Guarani Paraguaio', '   O Peso Argentino','   O Dolar','   O Euro',
                '      O Rublo Russo    ','    O Iene', '       O Dolar Aussie    ','         O Franco Suiço']

                urls = ['https://br.investing.com/currencies/gbp-brl',
                        'https://br.investing.com/crypto/dogecoin/doge-brl',
                        'https://br.investing.com/crypto/bitcoin/btc-brl',
                        'https://br.investing.com/crypto/ethereum/eth-brl',
                        'https://br.investing.com/crypto/litecoin/ltc-brl',
                        'https://br.investing.com/crypto/ripple/xrp-brl',
                        'https://br.investing.com/crypto/bitcoin-cash/bch-brl',
                        'https://br.investing.com/currencies/pyg-brl',
                        'https://br.investing.com/currencies/ars-brl',
                        'https://br.investing.com/currencies/usd-brl',          #Temos uma lista de cambios que podemos pegar
                        'https://br.investing.com/currencies/eur-brl',          #A estrutura de HTML deles é a msm
                        'https://br.investing.com/currencies/rub-brl',          #Então podemos so trocar o site sem problemas maiores
                        'https://br.investing.com/currencies/jpy-brl',
                        'https://br.investing.com/currencies/aud-brl',          #Nesse caso, temos uma lista de nomes pra evitar
                        'https://br.investing.com/currencies/chf-brl']          #que fiquem feios demais quando escritos

                print("Buscando cambio do" + nomes[ender] +"...")
                req = Request(urls[ender], headers={'User-Agent': 'Mozilla/5.0'})
                s = urlopen(req).read()
                                                                #Usando Resquest a gente abre o site 
                soup = BeautifulSoup(s, "lxml")
                ips = soup.find_all(class_='top bold inlineblock')     #E com BeautifulSoup procarando as classes especificas
                                                                       #Sabemos que a classe 'top bold inlineblock' guarda as informações
                valores = ips[0].get_text().split()                    #que queremos

                cotacao = valores[0]            #"ips = soup.find_all(class_='top bold inlineblock')" retorna uma lista de valores na pagina
                variacao = valores[2]           #Usamos .split() pra separar esses valores em uma lista    
                                                #As cotações que queremos vão ficar nos valores [0] e [2], sempre
                if str(variacao[0]) == '-':
                        box = Image.open("bitcoinchansad.png").convert('RGB')   #Baseado na cotação ele seleciona 
                else:                                                           #A imagem correta 
                        box = Image.open("bitcoinchan.png").convert('RGB')

                d = ImageDraw.Draw(box)        
                ncc = nomes[ender]      #Alguns detalhes sobre a formatação
                wd = 40
                tm = 45

                if len(ncc) > 13:
                        wd = 0
                        tm = 33         #Formatação baseada no tamanho da nome
                        
                if len(ncc) < 6:
                        wd = 77

                fnt = ImageFont.truetype('TNR.ttf', tm)

                wm = 42

                if len(cotacao) > 6:
                        wm = 18

                d.text((wd,5), ncc, font = fnt, fill=(90,90,90))
                fnt = ImageFont.truetype('TNR.ttf', 45)
                d.text((40, 40), "esta valendo", font = fnt, fill=(90,90,90))
                fnt = ImageFont.truetype('TNR.ttf', 55)        #Escrevendo as informações
                d.text((wm,80), cotacao + "R$", font = fnt, fill=(30,30,30))
                fnt = ImageFont.truetype('TNR.ttf', 40)

                if str(variacao[0]) == '-':
                        d.text((90,140),variacao, font = fnt, fill=(130,0,0))
                else:           #Selecionado a cor da variação da cotação
                        d.text((90,140),variacao, font = fnt, fill=(0,130,0))

                print("Redimensionando smug.png")
                resizedbox0 = box.resize((xs+1,ys+1), Image.ANTIALIAS)
                resizedbox = resizedbox0.load()
                

                for j in range (xs+1):
                        for k in range (ys+1):
                                img[j+a,k+b]=resizedbox[j,k]

                return img

        def selicD(img, s1, j):

                from bancocentral import Selic, Poupanca

                c1,c2,c3,c4 = s1[j]
                a,b = c1
                c,d = c2
                e,f = c3
                g,h = c4
                xs = int(sqrt( (a - c)**2 + (b - d)**2 ))
                ys = int(sqrt( (c - e)**2 + (d - f)**2 ))

                print("Abrindo smug.png")
                box = Image.open("smug.png").convert('RGB')
                d = ImageDraw.Draw(box)

                print("Buscando dados sobre a poupança e selic...")
                selic = Selic()         #Usamos a API do banco central
                poupanca = Poupanca()
                
                fnt = ImageFont.truetype('TNR.ttf', 33)
                d.text((19,8), "A taxa SELIC fica a", font = fnt, fill=(90,90,90))
                fnt = ImageFont.truetype('TNR.ttf', 45)
                d.text((103,40), selic, font = fnt, fill=(30,30,30))
                fnt = ImageFont.truetype('TNR.ttf', 33)
                d.text((24,80), " E a poupança em", font = fnt, fill=(90,90,90))
                fnt = ImageFont.truetype('TNR.ttf', 45)
                d.text((72,120), str(poupanca.get_poupanca_tax())+"%", font = fnt, fill=(30,30,30))
                fnt = ImageFont.truetype('TNR.ttf', 33)
                d.text((40,160), "       ao mês         ", font = fnt, fill=(90,90,90))
                
                print("Redimensionando smug.png")
                resizedbox0 = box.resize((xs+1,ys+1), Image.ANTIALIAS)
                resizedbox = resizedbox0.load()
                print("Salvando quadro...")

                for j in range (xs+1):                  #O resto do processo é o mesmo
                        for k in range (ys+1):
                                img[j+a,k+b]=resizedbox[j,k]

                return img

        def bovespaD(img, s1, j):

                from sgs import SGS, series
                import datetime
                import matplotlib.pyplot as plt
                
                print("Buscando dados sobre a BOVESPA")

                c1,c2,c3,c4 = s1[j]
                a,b = c1
                c,d = c2
                e,f = c3
                g,h = c4
                xs = int(sqrt( (a - c)**2 + (b - d)**2 ))
                ys = int(sqrt( (c - e)**2 + (d - f)**2 ))

                print("Abrindo smug.png")
                box = Image.open("smug.png").convert('RGB')
                d = ImageDraw.Draw(box)

                now = datetime.datetime.now()
                sgs = SGS()
                hoje = str(now.day)+"/"+str(now.month)+"/"+str(now.year)
                ontem = str((now.day))+"/"+str(now.month-1)+"/"+str(now.year)
                df = sgs.get_valores_series(series.BOVESPA_INDICE, ontem, hoje)
                df.head()                       #Usando a API do banco central, pegamos os dados da bovespa
                df = df.values                  #Ele vai nos retornar uma lista com os valores
                cots = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                dates = ['1','','','','','','','','','','','','','','','','','','','']

                for i in range(20):
                        cots[i] = df[i][1]              #Formatação basica dos valores
                        dates[i] = str(df[i][0])[:-8]
                plt.clf()          
                plt.rc('lines', linewidth=6, color='red')
                plt.plot(dates,cots)            #Usando matplotlib plotar o grafico e salvar-lo

                plt.savefig('output.png')

                fnt = ImageFont.truetype('TNR.ttf', 20)
                d.text((8,1), "Indice bovespa dos ultimos 30 dias", font = fnt, fill=(90,90,90))

                print("Redimensionando smug.png e grafico")
                gra0 = Image.open("output.png").convert('RGB')
                resizedgra0 = gra0.resize((xs+1,ys+1), Image.ANTIALIAS)
                resizedbox0 = box.resize((xs+1,ys+1), Image.ANTIALIAS)
                resizedgra = resizedgra0.load()
                resizedbox = resizedbox0.load()

                
                print("Salvando quadro...")
                for j in range (xs+1):
                        for k in range (ys+1):
                                if resizedgra[j,k] != (255,255,255): #Jogamos o grafico na imagem, ignorando pixels brancos
                                        resizedbox[j,k]=resizedgra[j,k] #Isso da uma falsa sensação de trasnparencia
                print("Salvando quadro...")
                for j in range (xs+1):
                        for k in range (ys+1):
                                img[j+a,k+b]=resizedbox[j,k]
                return img

        def acoesD(img, s1, j, ender):
        
                c1,c2,c3,c4 = s1[j]
                a,b = c1                        #A logica dessa função é quase a msm da cambiosD()
                c,d = c2
                e,f = c3
                g,h = c4
                xs = int(sqrt( (a - c)**2 + (b - d)**2 ))
                ys = int(sqrt( (c - e)**2 + (d - f)**2 ))

                sites = ['https://br.advfn.com/bolsa-de-valores/bovespa/vale-VALE3/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/petrobras-PETR4/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/itausa-ITSA4/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/tesla-inc-drn-TSLA34/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/nasdaq/AMD/cotacao'
                        'https://br.advfn.com/bolsa-de-valores/bovespa/intel-drn-ITLC34/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/microsoft-drn-MSFT34/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/apple-drn-AAPL34/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/amazon-drn-AMZO34/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/walt-disney-drn-DISB34/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/netflix-drn-NFLX34/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/carrefour-br-CRFB3/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/santander-br-SANB4/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/bradesco-BBDC4/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/brasilagro-on-AGRO3/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/gerdau-GGBR4/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/braskem-pna-BRKM5/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/petro-rio-PRIO3/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/magazine-luiza-MGLU3/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/ambev-ABEV3/cotacao',
                        'https://br.advfn.com/bolsa-de-valores/bovespa/cielo-CIEL3/cotacao',
                        ]

                print("Buscando dados sobre "+sites[ender])
                req = Request(sites[ender], headers={'User-Agent': 'Mozilla/5.0'})
                s = urlopen(req).read()
                                                        #A estrutura HTML de todas as urls são a msm
                soup = BeautifulSoup(s, "lxml")         #Sabemos que os dados que estão nessas classes
                                                        #de HTML
                ips2 = soup.find_all(class_='PriceTextUp')
                if ips2 != []:
                        cotacao = ips2[2].get_text()            #As cotação tem 3 possibilidades, subir, descer e neutral
                        cotacaov = ips2[1].get_text()           #E o nome da classe muda com isso
                        
                ips2 = soup.find_all(class_='PriceTextDown')   #Por isso usamos 3 ifs diferentes. 
                if ips2 != []:
                        cotacao = ips2[2].get_text()
                        cotacaov = ips2[1].get_text()
                
                ips2 = soup.find_all(class_='PriceTextUnchanged')
                if ips2 != []:
                        cotacao = ips2[2].get_text()
                        cotacaov = ips2[1].get_text()
                
                ipsn = soup.find_all('strong')                  #O resto do codigo é identico as outras funções
                nome = ipsn[0].get_text()

                if str(cotacaov)[0] == '-':
                        box = Image.open("bitcoinchansad.png").convert('RGB')
                else:
                        box = Image.open("bitcoinchan.png").convert('RGB')

                d = ImageDraw.Draw(box)

                fnt = ImageFont.truetype('TNR.ttf', 30)
                d.text((60,0), "As cotações da", font = fnt, fill=(90,90,90))

                if 10 < len(nome[7:]):
                        tws = 40
                if 15 < len(nome[7:]):
                        tws = 29                #Alguns ajustes baseado no tamanho do nome da cotação
                if 20 < len(nome[7:]):          #Ja que dessa vez n usamos uma lista de nomes
                        tws = 10
                if 30 < len(nome[7:]):
                        tws = -2
                        
                d.text((tws,29), nome[7:], font = fnt, fill=(90,90,90))
                d.text((105,54), "estão em", font = fnt, fill=(90,90,90))
                fnt = ImageFont.truetype('TNR.ttf', 55)
                d.text((60,80), cotacao + "R$", font = fnt, fill=(0,0,0))

                fnt = ImageFont.truetype('TNR.ttf', 45)
                if str(cotacaov)[0] == '-':
                        d.text((83,140), cotacaov, font = fnt, fill=(200,0,0))
                else:                                                           #E por fim, n tem nada de diferente
                        d.text((83,140), cotacaov, font = fnt, fill=(0,130,0))
                
                print("Redimensionando smug.png")
                resizedbox0 = box.resize((xs+1,ys+1), Image.ANTIALIAS)
                resizedbox = resizedbox0.load()
                print("Salvando quadro...")
                for j in range (xs+1):
                        for k in range (ys+1):
                                img[j+a,k+b]=resizedbox[j,k]

                return img

        def boiD(img, s1, j):
        
                c1,c2,c3,c4 = s1[j]
                a,b = c1
                c,d = c2
                e,f = c3
                g,h = c4
                xs = int(sqrt( (a - c)**2 + (b - d)**2 ))
                ys = int(sqrt( (c - e)**2 + (d - f)**2 ))
                

                print("Buscando dados sobre boi gordo")
                req = Request('https://canalrural.uol.com.br/cotacao/boi-gordo/', headers={'User-Agent': 'Mozilla/5.0'})
                s = urlopen(req).read()

                soup = BeautifulSoup(s, "lxml")
                ips = soup.find_all('td')               #Mesma logica de webscrapping das outras funções
                                                        #Sabemos em quais tags a informação esta
                valor = ips[1].get_text()
                local = ips[0].get_text()

                box = Image.open("boigordochan.png").convert('RGB')
                d = ImageDraw.Draw(box)

                fnt = ImageFont.truetype('TNR.ttf', 40)
                d.text((40,3), "  A arroba do", font = fnt, fill=(90,90,90))
                fnt = ImageFont.truetype('TNR.ttf', 39)
                d.text((2,39), "Boi Gordo esta em", font = fnt, fill=(90,90,90))
                fnt = ImageFont.truetype('TNR.ttf', 55)
                d.text((50,81), valor + "R$", font = fnt, fill=(0,0,0))
                fnt = ImageFont.truetype('TNR.ttf', 35)
                d.text((45,140), "(" + local + ")", font = fnt, fill=(90,90,90))
                
                print("Redimensionando smug.png")
                resizedbox0 = box.resize((xs+1,ys+1), Image.ANTIALIAS)
                resizedbox = resizedbox0.load()                         #A função corre normalmente como as outras
                print("Salvando quadro...")
                for j in range (xs+1):
                        for k in range (ys+1):          
                                img[j+a,k+b]=resizedbox[j,k]

                return img

        def sojaD(img, s1, j):
        
                c1,c2,c3,c4 = s1[j]
                a,b = c1
                c,d = c2
                e,f = c3
                g,h = c4
                xs = int(sqrt( (a - c)**2 + (b - d)**2 ))
                ys = int(sqrt( (c - e)**2 + (d - f)**2 ))
                

                print("Buscando dados sobre soja")
                req = Request('https://canalrural.uol.com.br/cotacao/soja/', headers={'User-Agent': 'Mozilla/5.0'})
                s = urlopen(req).read()

                soup = BeautifulSoup(s, "lxml")
                ips = soup.find_all("td")

                valor = ips[43].get_text()
                praca = ips[42].get_text()

                print("Abrindo smug.png")
                box = Image.open("smug.png").convert('RGB')
                d = ImageDraw.Draw(box)

                fnt = ImageFont.truetype('TNR.ttf', 42)
                d.text((40,3), "  A saca da ", font = fnt, fill=(90,90,90))
                d.text((5,39), "     Soja sai a", font = fnt, fill=(90,90,90))
                fnt = ImageFont.truetype('TNR.ttf', 55)
                d.text((55,85), valor + "R$", font = fnt, fill=(0,0,0))
                fnt = ImageFont.truetype('TNR.ttf', 35)
                d.text((37,140), "(" + praca + ")", font = fnt, fill=(90,90,90))
                
                print("Redimensionando smug.png")
                resizedbox0 = box.resize((xs+1,ys+1), Image.ANTIALIAS)
                resizedbox = resizedbox0.load()
                print("Salvando quadro...")
                for j in range (xs+1):
                        for k in range (ys+1):
                                img[j+a,k+b]=resizedbox[j,k]

                return img

        def feijaoD(img, s1, j):
        
                c1,c2,c3,c4 = s1[j]
                a,b = c1
                c,d = c2
                e,f = c3
                g,h = c4
                xs = int(sqrt( (a - c)**2 + (b - d)**2 ))
                ys = int(sqrt( (c - e)**2 + (d - f)**2 ))
                

                print("Buscando dados sobre feijao")
              
                req = Request('https://canalrural.uol.com.br/cotacao/feijao/', headers={'User-Agent': 'Mozilla/5.0'})
                s = urlopen(req).read()

                soup = BeautifulSoup(s, "lxml")
                ips = soup.find_all("td")

                praca = ips[0].get_text()
                valor = ips[1].get_text()

                print("Abrindo smug.png")
                box = Image.open("smug.png").convert('RGB')
                d = ImageDraw.Draw(box)

                fnt = ImageFont.truetype('TNR.ttf', 42)
                d.text((40,3), "  A saca do ", font = fnt, fill=(90,90,90))
                d.text((5,39), "    Feijão sai a", font = fnt, fill=(90,90,90))
                fnt = ImageFont.truetype('TNR.ttf', 55)
                d.text((46,80), valor + "R$", font = fnt, fill=(0,0,0))
                fnt = ImageFont.truetype('TNR.ttf', 35)
                d.text((37,140), "   (" + praca + ")", font = fnt, fill=(90,90,90))
                
                print("Redimensionando smug.png")
                resizedbox0 = box.resize((xs+1,ys+1), Image.ANTIALIAS)
                resizedbox = resizedbox0.load()
                print("Salvando quadro...")
                for j in range (xs+1):
                        for k in range (ys+1):
                                img[j+a,k+b]=resizedbox[j,k]

                return img

        def barrilD(img, s1, j):
        
                c1,c2,c3,c4 = s1[j]
                a,b = c1
                c,d = c2
                e,f = c3
                g,h = c4
                xs = int(sqrt( (a - c)**2 + (b - d)**2 ))
                ys = int(sqrt( (c - e)**2 + (d - f)**2 ))
                

                print("Buscando dados sobre petroleo")
                req = Request('https://br.investing.com/commodities/brent-oil-historical-data', headers={'User-Agent': 'Mozilla/5.0'})
                s = urlopen(req).read()

                soup = BeautifulSoup(s, "lxml")
                ips = soup.find_all(class_='top bold inlineblock')

                valores = ips[0].get_text().split()

                preco = valores[0]
                variacao = valores[2]

                print("Abrindo smug.png")
                box = Image.open("smug.png").convert('RGB')
                d = ImageDraw.Draw(box)

                
                fnt = ImageFont.truetype('TNR.ttf', 42)
                d.text((40,3), "  O barril do ", font = fnt, fill=(90,90,90))
                d.text((9,39), "Petroleo esta em", font = fnt, fill=(90,90,90))
                fnt = ImageFont.truetype('TNR.ttf', 55)
                d.text((44,80), preco + "USD", font = fnt, fill=(0,0,0))

                fnt = ImageFont.truetype('TNR.ttf', 45)
                if str(variacao)[0] == '-':
                        d.text((86,140), variacao, font = fnt, fill=(200,0,0))
                else:
                        d.text((86,140), variacao, font = fnt, fill=(0,130,0))
                
                print("Redimensionando smug.png")
                resizedbox0 = box.resize((xs+1,ys+1), Image.ANTIALIAS)
                resizedbox = resizedbox0.load()
                print("Salvando quadro...")
                for j in range (xs+1):
                        for k in range (ys+1):
                                img[j+a,k+b]=resizedbox[j,k]

                return img

        def gradolarD(img, s1, j):

                import matplotlib.pyplot as plt
                
                print("Buscando grafico dolar")

                c1,c2,c3,c4 = s1[j]
                a,b = c1
                c,d = c2
                e,f = c3
                g,h = c4
                xs = int(sqrt((a - c)**2 + (b - d)**2))
                ys = int(sqrt((c - e)**2 + (d - f)**2))

                print("Abrindo smug.png")
                box = Image.open("smug.png").convert('RGB')
                d = ImageDraw.Draw(box)
                
                with urlopen("https://www.infomoney.com.br/mercados/cambio") as url:
                        s = url.read()
    
                soup = BeautifulSoup(s, "lxml")
                ips = soup.find_all("tbody")
                ips2 = ips[1]                           #Mesma logica de webscrapping das outras
                ips3 = ips2.find_all('tr')              #Mas salvamos um grafico

                n = [0,0,0,0,0]
                n2 = ["","","","",""]

                for i in range (5):
                        e = ips3[i].find_all('td')[1]           #Formatação pra ajustar os valores
                        n[4-i] = e.get_text()
                        dummy = n[4-i][3] +  '.' +  n[4-i][5] +  n[4-i][6]
                        n[4-i] =  float(dummy)

                        e = ips3[i].find_all('td')[0]
                        n2[4-i] = e.get_text()
                plt.clf()           #è importante usar plt.clf(), caso contrario teremos problemas com plotar outros graficos na msm run              
                plt.rc('lines', linewidth=6, color='red')       ##Usamos matplotlib pra plotar o grafico
                plt.plot(n2,n)

                plt.savefig('output.png')

                fnt = ImageFont.truetype('TNR.ttf', 20)
                d.text((4,1), "Cotação do Dolar nos ultimos 5 dias", font = fnt, fill=(90,90,90))

                print("Redimensionando smug.png e grafico")
                gra0 = Image.open("output.png").convert('RGB')
                resizedgra0 = gra0.resize((xs+1,ys+1), Image.ANTIALIAS)
                resizedbox0 = box.resize((xs+1,ys+1), Image.ANTIALIAS)
                resizedgra = resizedgra0.load()
                resizedbox = resizedbox0.load()
                
                print("Salvando quadro...")
                for j in range (xs+1):
                        for k in range (ys+1):
                                if resizedgra[j,k] != (255,255,255):    #Colocamos o grafico na imagem
                                        resizedbox[j,k]=resizedgra[j,k]

                print("Salvando quadro...")                             #O resto da função segue normalmente
                for j in range (xs+1):
                        for k in range (ys+1):
                                img[j+a,k+b]=resizedbox[j,k]

                return img

        def bovespCD(img, s1, j):               #Não ta funcionando God knows why
        
                c1,c2,c3,c4 = s1[j]
                a,b = c1
                c,d = c2
                e,f = c3
                g,h = c4
                xs = int(sqrt( (a - c)**2 + (b - d)**2 ))
                ys = int(sqrt( (c - e)**2 + (d - f)**2 ))
                

                print("Buscando dados sobre a bovespa")
                req = Request('https://br.advfn.com/bolsa-de-valores/bovespa/bovespa-index-IBOV/cotacao', headers={'User-Agent': 'Mozilla/5.0'})
                s = urlopen(req).read()

                try:
                        soup = BeautifulSoup(s, "lxml")
                        ips2 = soup.find_all(class_='PriceTextDown')
                        
                        cotacao = ips2[2].get_text()
                        cotacaov = ips2[1].get_text()

                except:
                        soup = BeautifulSoup(s, "lxml")
                        ips2 = soup.find_all(class_='PriceTextUp')

                        cotacao = ips2[2].get_text()
                        cotacaov = ips2[1].get_text()

                print("Abrindo smug.png")
                box = Image.open("smug.png").convert('RGB')
                d = ImageDraw.Draw(box)

                
                fnt = ImageFont.truetype('TNR.ttf', 42)
                d.text((40,3), "  O indice ", font = fnt, fill=(90,90,90))
                d.text((9,39), "Bovespa esta em", font = fnt, fill=(90,90,90))
                fnt = ImageFont.truetype('TNR.ttf', 55)
                d.text((65,80), cotacao + "R$", font = fnt, fill=(0,0,0))

                fnt = ImageFont.truetype('TNR.ttf', 45)
                if str(cotacaov)[0] == '-':
                        d.text((86,140), cotacaov, font = fnt, fill=(200,0,0))
                else:
                        d.text((86,140), cotacaov, font = fnt, fill=(0,130,0))
                
                print("Redimensionando smug.png")
                resizedbox0 = box.resize((xs+1,ys+1), Image.ANTIALIAS)
                resizedbox = resizedbox0.load()
                print("Salvando quadro...")
                for j in range (xs+1):
                        for k in range (ys+1):
                                img[j+a,k+b]=resizedbox[j,k]

                return img

        def noticiaT():       #Mesma logica basica do webscrapping

                import random
                req = Request("https://www.infomoney.com.br/mercados/ultimas-noticias/pagina/" + str(random.randint(1,4)), headers={'User-Agent': 'Chrome/60.0.3112.113'})
                s = urlopen(req).read()         #Pegamos uma das paginas de noticia do infomoney

                soup = BeautifulSoup(s, "lxml")
                ips = soup.find_all(class_="column")   #E sabemos que a class "column" guarda as machentes e links
                data = ips[random.randint(0,14)].find_all(class_="title-box title-box-medium")
                manchete = data[0].get_text()   #Selecionamos uma das classes column, cada pagina tem 14 delas
                data = str(data)                #E pegamos o texto, sabemos que o primeiro sera a manchete
                link = "https://www.infomoney.com.br" + data.split('"')[5] #E o quinto, caso separarmos com ' " ', sera o link
                
                return manchete, link   #Retornamos a manchete e o link

        def testD(img, s1, j):
        
                c1,c2,c3,c4 = s1[j]
                a,b = c1
                c,d = c2
                e,f = c3                #Class de teste basica
                g,h = c4
                xs = int(sqrt( (a - c)**2 + (b - d)**2 ))
                ys = int(sqrt( (c - e)**2 + (d - f)**2 ))
                
                box = Image.open("smug.png").convert('RGB')
                
                
                print("Redimensionando smug.png")
                resizedbox0 = box.resize((xs+1,ys+1), Image.ANTIALIAS)
                resizedbox = resizedbox0.load()
                print("Salvando quadro...")
                for j in range (xs+1):
                        for k in range (ys+1):
                                img[j+a,k+b]=resizedbox[j,k]

                return img





        
