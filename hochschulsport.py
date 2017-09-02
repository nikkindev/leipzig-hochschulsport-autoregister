import requests,re,sys
from bs4 import BeautifulSoup


#--Perosnal info/Form data--#
sex='M'
firstname='Bruce'
secondname='Wayne'
street_no='Philip Rosenthaal 56'
zipcode_city='04103 Leipzig'
status='S-UNIL'
matnr='373883'
email='bruce@wayne.corp'
telefon='017630897591'
newsletter='ja' #Empty string or 'ja'

#--URLs and header info--#      (1)URLs check
url='https://hochschulsport.uni-leipzig.de/angebote/aktueller_zeitraum/_Qi_Gong.html' #Sport info URL
url_reg='https://hochschulsport.uni-leipzig.de/cgi/anmeldung.fcgi' #URL for formdata post/Registration URL

#--Inspect element from browser and fill in the headers--#       (2)Headers check
headers1={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            #'Content-Length':63, #Check for specific sport/ignored mostly
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'hochschulsport.uni-leipzig.de',
            'Origin':'https://hochschulsport.uni-leipzig.de',
            'Referer':'https://hochschulsport.uni-leipzig.de/angebote/aktueller_zeitraum/_Qi_Gong.html', #Response Headers check!!!
            'Upgrade-Insecure-Requests':1,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }

headers2={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            #'Content-Length':279, #Check for specific sport/ignored mostly
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'hochschulsport.uni-leipzig.de',
            'Origin':'https://hochschulsport.uni-leipzig.de',
            'Referer':'https://hochschulsport.uni-leipzig.de/cgi/anmeldung.fcgi', #Response Headers check!!!
            'Upgrade-Insecure-Requests':1,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }


#--Start a session--#
with requests.Session() as s:
    #--Find BS_Code & Kursid--#
    r1=s.get(url)
    if r1.status_code!=200:
        print 'Error in Response(r1). Please check the code and verify URL'
        sys.exit()
    soup1=BeautifulSoup(r1.content,'html.parser')
    code=re.findall('<input name="BS_Code" type="hidden" value="(.*)"/>',soup1.prettify())
    kursid=re.findall('<input class="bs_btn_buchen" name="BS_Kursid_(.*)" title="booking" type="submit" value="buchen"/>',soup1.prettify())
    print 'BS_Code\t: %s' %code[0]
    print 'Kursid\t: %s' %kursid[0]
    form_data1={'BS_Code':code[0],'BS_Kursid_21932':'buchen'}       #(3)Kursid check

    #--Find fid--#
    r2=s.post(url_reg, headers=headers1, data=form_data1)
    if r2.status_code!=200:
        print 'Error in Response(r2). Please check the code and verify URL, headers and formdata'
        sys.exit()
    soup2=BeautifulSoup(r2.content,'html.parser')
    fid=re.findall('<input name="fid" type="hidden" value="(.*)"/>',soup2.prettify())
    ext=re.findall('<script src="/SysBilder/res/(.*)" type="text/javascript">',soup2.prettify())
    exturl='https://hochschulsport.uni-leipzig.de/SysBilder/res/'+ext[0]
    g2=s.get(exturl)
    print 'fid\t: %s' %fid[0]

    #--Fill the form, send a POST request, extract _formdata value from response--#
    form_data2={'fid':fid[0],
                'sex':sex,
                'vorname':firstname,
                'name':secondname,
                'strasse':street_no,
                'ort':zipcode_city,
                'statusorig':status,
                'matnr':matnr,
                'mitnr':'',
                'email':email,
                'telefon':telefon,
                'newsletter':newsletter,
                'tnbed':1
                }
    r3=s.post(url_reg, headers=headers1, data=form_data2)
    if r1.status_code!=200:
        print 'Error in Response(r3). Please check the code'
        sys.exit()
    soup3=BeautifulSoup(r3.content,'html.parser')
    formdata=re.findall('<input name="_formdata" type="hidden" value="(.*)"/>',soup3.prettify())
    g3_1=s.get(exturl)
    g3_2=s.get('https://hochschulsport.uni-leipzig.de/buchsys/lib/global/anmeldung.css')
    g3_3=s.get('https://hochschulsport.uni-leipzig.de/SysBilder/resex/anm_style.css')
    print '_formdata\t: %s' %formdata[0]


    #--Final phase of submission with _formdata value--#
    form_data3={'fid':fid[0],
                'Phase':'final',
                'tnbed':1,
                'sex':sex,
                'vorname':firstname,
                'name':secondname,
                'strasse':street_no,
                'ort':zipcode_city,
                'statusorig':status,
                'matnr':matnr,
                #'mitnr':'',
                'email':email,
                'telefon':telefon,
                'newsletter':newsletter,
                'preis_anz':'20,00 EUR',   #(4)Price check
                '_formdata':formdata[0]
                }
    r4=s.post(url_reg, headers=headers2, data=form_data3)
    soup4=BeautifulSoup(r4.content,'html.parser')
    f4=open('r4.txt','w')
    f4.write(soup4.prettify().encode('utf-8'))
    f4.close()
print 'Registration successful!'
