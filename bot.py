# coding=utf-8

from PIL import Image, ImageDraw, ImageFont
import random
from botcore import bot
import tweepy
import facebook
import time

#pip install matplotlib
#pip install PIL
#pip install python-resize-image
#pip install pandas
#pip install BeautifulSoup

trying = True 

imm = 380 #Numero de imagens na pasta source

testing = False       #Bool que controla se é um teste ou não

while trying:

        try:
               
                if testing:
                        imgt = "1.png"          #Caso isso seja um teste, ele pega a imagem dummy de tests
                else:                           #Caso não seja, ele pega uma aleatoria da pasta source
                        imgt = "sources/h_" + str(random.randint(0,imm)) + '.png'   
                                                              

                print("Carregando imagem..."+imgt)   #Carregando as imagem usando PIL
                img0 = Image.open(imgt).convert('RGB') #Note que usamos RGB, não RGBA, algumas imagens vem 
                                                        #Como RGBA, então a conversão é necessaria
                img = img0.load()              

                s1,sn = bot.censorsearch(img0) #Chama a função que identifica as censuras
                                                #Ela retorna uma lista com as coordenadas de cara censura
                                                #E o numero de censuras 
                

                ps = [1,1,1,1,1,1,1,1,1,1,
                      1,1,1,1,1,1,1,1,1,1,
                      1,1,1,1,1,1,1,1,1,1,
                      2,2,2,2,2,2,2,2,2,2,
                      2,2,2,2,2,2,2,2,2,2,
                      2,2,2,2,2,2,2,2,2,2,      #Esse array é utilizado pra um sistema de %
                      3,3,4,4,4,4,4,4,4,4,      #Não é algo pra se orgulhar, mas funciona
                      5,5,5,5,5,6,6,6,6,6,
                      7,1,1,2,2,1,2,8,8,8,
                      9,9,9,9,2,2,2,10,10,1,
                      1,2,3,4,5,1,2,3,5,5,
                      1,2,3,4,5,1,2,3,5,5]

                n = [-1] * sn #Se cria uma lista com o numero de censuras
                for i in range (sn):
                        while True:
                                dummy = random.randint(1,100)
                                if not dummy in n:
                                        n[i]= ps[dummy]    #E é atribuido um quadro numero para cada censura
                                        break              #Ele tenta não repetir o mesmo numero, e assim não repetir quadros
                                if 23 <= i:               
                                        break              #A forma com que isso acontece é meio falha, e esta "sucetivel ao azar probabilistco"
                                                           #But hey, as long as it works.
             
                if True:
                        for j in range (sn): #Então, pra cada quadro ele chama o numero da funçao sorteada

                                print("Preenchendo censura "+str(j+1)+"...")
                                i = int(n[j])

                                #Todas as funçoes pegam como argumento a imagem (img), e as coordenadas (s1 e j)
                                #As taxas de cambio e stocks tbm levam um int extra pra decidir a cotação

                                if i == 1: #Taxas de cambio

                                        ran = random.randint(0,18)          #São taxas 19 possiveis, ele sorteia uma
                                        img = bot.cambiosD(img, s1, j, ran)
                                                                
                                if i == 2: #Stocks
                                        
                                        ran = random.randint(0,12)       #São stocks 13 possiveis, ele sorteia uma
                                        img = bot.acoesD(img, s1, j, ran)

                                if i == 3: #Inflação
                                        img = bot.inflacaoD(img, s1, j)
                                           
                                if i == 4: #Grafico com dolar
                                        img = bot.gradolarD(img, s1, j)

                                if i == 5: #Grafico Bovespa
                                        img = bot.bovespaD(img, s1, j)

                                if i == 6: #@ do boi gordo
                                        img = bot.boiD(img, s1, j)

                                if i == 7: #Saca da Soja
                                        img = bot.sojaD(img, s1, j)

                                if i == 8: #Saca do Feijão
                                        img = bot.feijaoD(img, s1, j)

                                if i == 9: #Barril de petroleo 
                                        img = bot.barrilD(img, s1, j)

                                if i == 10: #Selic
                                        img = bot.selicD(img, s1, j)
                                        


                d = ImageDraw.Draw(img0)        #Cria um objeto de desenho para que possamos escrever na imagem
                fnt = ImageFont.truetype('TNR.ttf', 15)         #Justa a fonte e tamanho
                d.text((20,20), "@gostosas2d_bot", font = fnt, fill=(100,100,100,30))   #Escreve a @ do twitter

                img0.save("finished.png")       #Salvamos a imagem 

                
                trying = False #Estamos prontos sair do loop pois a imagem foi feita da forma correta
                

        except Exception as e:
                print(e)

        texto = ''

        try:
                manchete, link = bot.noticiaT()  #Pegamos uma noticia e o link dela
                prefixos = ["senpai", "chan", "san", "sama"]    
               
                #E fazemos um textinho
                texto = "Infomoney-" + prefixos[random.randint(0,3)] + ": \"" + manchete + "\" \n" + link + " via @Infomoney"
                
        except Exception as e:
                        print(e)

        print(texto)
        
        if not testing: #Caso não esteja testando, postaremos nas redes sociais
                try:    
                        #As tokens obtidas pelo https://developer.twitter.com/
                        consumer_secret = ""
                        consumer_key = ""
                        
                        access_token = ""
                        access_token_secret = ""

                        #Logando com elas no twitter
                        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                        auth.set_access_token(access_token, access_token_secret)
                        api = tweepy.API(auth) #Cria objeto da api

                        file = open('finished.png', 'rb') #Abre o arquivo previamente salvo

                        r1 = api.media_upload(filename='ttest.png', file=file) #No twitter voce primeiro faz o upload das foto
                        media = [r1.media_id_string]    #[r1.media_id_string] vai nos retornar uma lista com os ids das medias upadas

                        api.update_status(media_ids=media, status=texto) #E so então, usamos esse ID pra postar
                        trying = False

                except Exception as e:
                        print(e)


                try:
                        #Id do perfil e token obtidos no https://developers.facebook.com
                        ProfileId = "" 
                        AcessToken = ""
                        
                        graph = facebook.GraphAPI(AcessToken)   #Loga e cria o objeto da api

                        graph.put_photo(image=open('finished.png', 'rb'), message=texto) #No facebook n é necessario upar primeiro ou coisa do tipo
                                                                                         #Se manda a imagem direto e é isso
                except Exception as e:
                        print(e)

