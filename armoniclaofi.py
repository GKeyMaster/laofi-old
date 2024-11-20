#armoniclaofi 3.00 03/11/2018
#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import webapp2
import os
import datetime
import MySQLdb
from google.appengine.api import users
from google.appengine.ext.webapp import template
from datetime import timedelta


# BASE DE DATOS
################################

# These environment variables are configured in app.yaml
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
CLOUDSQL_DATABASE= os.environ.get('CLOUDSQL_DATABASE')

def connect_to_cloudsql():
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):

        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD,
            db=CLOUDSQL_DATABASE,
            charset='utf8')

    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db



def get_db():
    conn = connect_to_cloudsql()
    return conn


#INICI APLICACIO
class MainPage(webapp2.RequestHandler):
    def get(self):
            self.redirect("/Inicio") #Redirecciona a Inicio


            


# FUNCIONS GENERALS
################################ 
def novar(variable):
    if variable is not None and variable != '':
        variable = variable
    else:
        variable = ""
    return variable

def noimp(variable):
    if variable is not None and variable != '':
        variable = variable
    else:
        variable = ""
    return variable



          
#-- FUNCIO DATA FORMAT
#-- Convertix una data al format 2016-09-26
def dataFormat(data):
    try:
        dataF= data.strftime("%Y-%m-%d") # data amb format 
    except:
        dataF= ""
    return dataF

#-- FUNCIO TEMPS FORMAT
#-- Convertix una data al format 2016-09-26 11:22:10
def tempsFormat(temps):
    try:
        tempsF = temps.strftime("%Y-%m-%d %H:%M:%S")
    except:
        tempsF=""
    return tempsF

#-- FUNCIO TELFON FORMAT
#-- Converteix les 9 primeres xifres de una cadena de text en format telefon 619 84 04 57
def telFormat(tel):
    telF = tel[0:3]+" "+tel[3:5]+" "+tel[5:7]+" "+tel[7:9]+" "+tel[9:]
    return telF

#-- FUNCIO PROXIM DIA DE LA SETMANA
#-- Dona la data del proxim dia de la setmana que se indique, per exemple del proxim dilluns  0 = Monday, 1=Tuesday, 2=Wednesday...
def proxDia(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def dillunsDosSem(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(7) + datetime.timedelta(days_ahead)

def dillunsDeuSem(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(63) + datetime.timedelta(days_ahead)

def dillunsActual(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d - datetime.timedelta(8) + datetime.timedelta(days_ahead)

#-- FUNCIO ESQUEMA SEGUENT
#-- Entrada: numExpedient del ultim expedient
#-- Resultat: numExpedient seguent
def esquemaSeguent(numExpedient):
    esqU = numExpedient[0:5]
    esqUn = int(esqU)
    esqSn = esqUn+1
    esqS = str(esqSn)+"C"
    return esqS

#-- FUNCIO PRESSUP SEGUENT
#-- Entrada: numPressup del ultim expedient
#-- Resultat: numPres seguent
def pressupostSeguent(numPressupost):
    an = numPressupost[0:2]
    num = numPressupost[3:6]
    total = an+num
    try:
        total = int(total)
    except:
        total=0
    seguent = total+1
    seguent = str(seguent)
    segNum = seguent[2:6]
    pressup = an+"/"+segNum+"A"
    return pressup

#-- FUNCIO PROFORMA SEGUENT
#-- Entrada: proforma ultima
#-- Resultat: proforma seguent
def proformaSeguent(proforma):
    an = proforma[0:2]
    num = proforma[3:6]
    total = an+num
    total = int(total)
    seguent = total+1
    seguent = str(seguent)
    segNum = seguent[2:6]
    profS = an+"/"+segNum+"P"
    return profS

#-- FUNCIO DATA FORMAT
#-- ara per a capsules segons horari estiu hivern ESTIU CANVI HORA
def araHora():
    horariEstiu = 1 # 1=estiu  0=hivern
    if horariEstiu == 1:
        ara=datetime.datetime.now()+ timedelta(hours=2) # data amb format 
    else:
        ara=datetime.datetime.now()+ timedelta(hours=1) # data amb format 
    return ara

# FUNCIO ELIMINA COMES

def eliminaComes(cadena):
    buscar = ","
    reemplazar = ";"
    try:
        noComa = cadena.replace(buscar, reemplazar)
    except:
        noComa=cadena
    return noComa
            
###########################################################################################################################################################
# CONTROL D'ACCES      CONTROL D'ACCES      CONTROL D'ACCES      CONTROL D'ACCES      CONTROL D'ACCES      CONTROL D'ACCES     
########################################################################################################################################################### 
    
def autentificacio(self, users):
    user = users.get_current_user()
    lista = treballadorsNivell()
    dernierePos = len(lista)-1
    idTreballador= -1
    
    
    if user:
        
        i=0
        while(i<=dernierePos):
            treballador=lista[i]
            if user.nickname() ==treballador.mailTreballador:           
                idTreballador= treballador.idTreballador
                i=dernierePos+1
                
            else :
                idTreballador=-1
                i+=1
    if(idTreballador == -1):
        self.redirect(users.create_login_url(self.request.uri,))
                          
    return idTreballador

def treballadorsNivell():
    db= get_db()
    cursor = db.cursor()
    lista= tablaTreballadorsNivell(cursor)
    db.commit()
    db.close()
    return lista






        
###########################################################################################################################################################
# INICI     INICI    INICI     INICI    INICI     INICI    INICI     INICI    INICI     INICI    INICI     INICI    INICI     
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariInicio (usuari):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)

    
    #desconectar de la bd
    db.commit()
    db.close()
    
    

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class Inicio(webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):   
            self.redirect("/LiniatempsTreballador") 


class Index(webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #obtenim valors per al html
            values = formulariInicio(usuari)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'index.html') 
            self.response.out.write(template.render(path, values,))
            



###########################################################################################################################################################
# TREBALLADOR          TREBALLADOR          TREBALLADOR          TREBALLADOR          TREBALLADOR          TREBALLADOR          TREBALLADOR         
###########################################################################################################################################################


def tablaTreballadorSelect(cursor, idTreballador):
    cursor.execute('SELECT idTreballador, claveTreballador, nomTreballador, telfTreballador, mailTreballador, nomina, complement, ssTreballador, ssEmpresa, irpfTreballador, irpfAut, enActiu, nivell FROM treballadors WHERE idTreballador=%s',(idTreballador,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista
        lista = Treballador(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12]) #Modificar si anyadim columna
    return lista        


def tablaTreballadorTots(cursor):   
    cursor.execute('SELECT idTreballador, claveTreballador, nomTreballador, telfTreballador, mailTreballador, nomina, complement, ssTreballador, ssEmpresa, irpfTreballador, irpfAut, enActiu, nivell FROM treballadors  ORDER BY enActiu DESC, nivell DESC, idTreballador')
    expedients = cursor.fetchall()
    conta=0
    indice=0
    for i in expedients: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in expedients: #cada fila es converteix en un objecte de lista
        lista[indice] = Treballador(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12]) #Modificar si anyadim columna
        indice=indice+1   
    return lista

def tablaTreballadorsNivell(cursor):   
    cursor.execute('SELECT idTreballador, claveTreballador, nomTreballador, telfTreballador, mailTreballador, nomina, complement, ssTreballador, ssEmpresa, irpfTreballador, irpfAut, enActiu, nivell FROM treballadors WHERE nivell>%s',(0,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Treballador(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11], i[12]) #Modificar si anyadim columna
        indice=indice+1   
    return lista

def tablaTreballadorAct(cursor):   
    cursor.execute('SELECT idTreballador, claveTreballador, nomTreballador, telfTreballador, mailTreballador, nomina, complement, ssTreballador, ssEmpresa, irpfTreballador, irpfAut, enActiu, nivell FROM treballadors WHERE enActiu=%s ORDER BY ordre',(1,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Treballador(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11], i[12]) #Modificar si anyadim columna
        indice=indice+1   
    return lista 
           
class Treballador: 
    def __init__(self, idTreballador=0, claveTreballador='', nomTreballador='', telfTreballador='',
                 mailTreballador='', nomina=0, complement=0, ssTreballador=0, ssEmpresa=0 ,irpfTreballador=0,
                 irpfAut=0, enActiu=0, nivell=0):
        self.idTreballador = idTreballador
        self.claveTreballador = claveTreballador
        self.nomTreballador = nomTreballador
        self.telfTreballador = telfTreballador
        self.mailTreballador = mailTreballador
        self.nomina = nomina
        self.complement = complement
        self.ssTreballador = ssTreballador
        self.ssEmpresa = ssEmpresa
        self.irpfTreballador = irpfTreballador
        self.irpfAut = irpfAut
        self.enActiu = enActiu
        self.nivell = nivell           

###########################################################################################################################################################
# CONTROL             CONTROL             CONTROL             CONTROL             CONTROL             CONTROL             CONTROL             
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariUsuari (usuari, idTreballador):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    
    if idTreballador == -1: #sense seleccio
        usuariSelect = ''
        treballadorTots = tablaTreballadorTots(cursor)
        
    elif idTreballador == -2: #treballador en blanc
        usuariSelect = ''
        treballadorTots = ''
        
    else: #treballador select
        usuariSelect = tablaTreballadorSelect(cursor,idTreballador)
        treballadorTots = ''
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'idTreballador': idTreballador,
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'usuariSelect': usuariSelect,
             'treballadorTots': treballadorTots,
             
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class UsuariTots (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            nivell=nivellUsuari(usuari)
            if(nivell==2):   
                #parametres
                idTreballador = -1
            
                #obtenim valors per al html
                values = formulariUsuari(usuari, idTreballador)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'usuari.html') 
                self.response.out.write(template.render(path, values,))
            else:
                #obtenim valors per al html
                values = formulariInicio(usuari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'accesDenegat.html') 
                self.response.out.write(template.render(path, values,))
            

class UsuariNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            nivell=nivellUsuari(usuari)
            if(nivell==2):   
                #parametres
                idTreballador = -2
            
                #obtenim valors per al html
                values = formulariUsuari(usuari, idTreballador)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'usuari.html') 
                self.response.out.write(template.render(path, values,))
            else:
                #obtenim valors per al html
                values = formulariInicio(usuari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'accesDenegat.html') 
                self.response.out.write(template.render(path, values,))
            
class UsuariSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTreballador= novar(self.request.get('idTreballador'))
            
            #parametres

            
            #obtenim valors per al html
            values = formulariUsuari(usuari, idTreballador)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'usuari.html') 
            self.response.out.write(template.render(path, values,))
            
class UsuariEdita (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTreballador= novar(self.request.get('idTreballador'))
            claveTreballador = novar(self.request.get('claveTreballador'))
            nomTreballador = novar(self.request.get('nomTreballador'))
            mailTreballador = novar(self.request.get('mailTreballador'))
            enActiu = novar(self.request.get('enActiu'))
            nivell = novar(self.request.get('nivell'))
            

            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('UPDATE treballadors SET claveTreballador=%s, nomTreballador=%s, mailTreballador=%s, enActiu=%s, nivell=%s WHERE idTreballador=%s', (claveTreballador, nomTreballador, mailTreballador, enActiu, nivell, idTreballador,))
            
            db.commit()
            db.close()
            
            #redirecciona
            self.redirect("/UsuariTots")

class UsuariCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            claveTreballador = novar(self.request.get('claveTreballador'))
            nomTreballador = novar(self.request.get('nomTreballador'))
            mailTreballador = novar(self.request.get('mailTreballador'))
            enActiu = novar(self.request.get('enActiu'))
            nivell = novar(self.request.get('nivell'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('INSERT INTO treballadors (claveTreballador, nomTreballador, mailTreballador, enActiu, nivell, telfTreballador, nomina, complement, ssTreballador, ssEmpresa, irpfTreballador, irpfAut) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (claveTreballador, nomTreballador, mailTreballador, enActiu, nivell, 0, 0, 0, 0, 0, 0, 0,))
            cursor.execute('SELECT idTreballador FROM treballadors ORDER BY idTreballador DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idTreballador = lista[0][0]
            cursor.execute('UPDATE treballadors SET ordre=%s WHERE idTreballador=%s', (idTreballador, idTreballador,))
            #inserta fitxa a 0
            treballant = 0
            ara = araHora()
            iniciFitxa = tempsFormat(ara)

                               
            cursor.execute('INSERT INTO fitxar (idTreballador, treballant, hora) VALUES (%s, %s, %s)', (idTreballador, treballant, iniciFitxa))

           
    
            
            db.commit()
            db.close()

            #redirecciona
            self.redirect("/UsuariTots")
            
# FUNCIONS SECUNDARIES DEL FORMULARI
####################################



def nivellUsuari(idTreballador):
    db= get_db()
    cursor = db.cursor()
    cursor.execute('SELECT  nivell FROM treballadors  WHERE idTreballador=%s', (idTreballador,))
    tabla = cursor.fetchall()
    idTreballador = tabla [0][0]
    db.commit()
    db.close()
    return idTreballador

###########################################################################################################################################################
# TOTS ELS ESQUEMES        TOTS ELS ESQUEMES        TOTS ELS ESQUEMES         TOTS ELS ESQUEMES         TOTS ELS ESQUEMES     
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariEsquemesTots (usuari,limit):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    
    limit=int(limit)
    if limit==0:
        esquemesTots=tablaEsquemesTots(cursor)
    else:
        esquemesTots=tablaEsquemesUltims(cursor)
    #desconectar de la bd
    db.commit()
    db.close()
    
    

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'esquemesTots': esquemesTots,
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class EsquemesTots(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            limit=0
            #obtenim valors per al html
            values = formulariEsquemesTots(usuari,limit)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'esquemesTots.html') 
            self.response.out.write(template.render(path, values,))
            
class EsquemesUltims(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            limit=1
            #obtenim valors per al html
            values = formulariEsquemesTots(usuari, limit)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'esquemesTots.html') 
            self.response.out.write(template.render(path, values,))


# FUNCIONS SECUNDARIES DEL FORMULARI
####################################

#--Llistat de tots els esquemes amb dades importants per a poder buscar amb ctrl+F
def tablaEsquemesTots(cursor):   
    cursor.execute('SELECT es.idEsquema, es.numExpedient, es.nomExpedient, es.direcLocal, cl.nomClient FROM clients cl INNER JOIN esquemes es ON es.idClient = cl.idClient WHERE es.numExpedient>%s ORDER BY es.idEsquema DESC', ('0',))
    expedients = cursor.fetchall()
    conta=0
    indice=0
    for i in expedients: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in expedients: #cada fila es converteix en un objecte de lista
        lista[indice] = EsquemaTots(i[0],i[1],i[2],i[3],i[4]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

def tablaEsquemesUltims(cursor):   
    cursor.execute('SELECT es.idEsquema, es.numExpedient, es.nomExpedient, es.direcLocal, cl.nomClient FROM clients cl INNER JOIN esquemes es ON es.idClient = cl.idClient WHERE es.numExpedient>%s ORDER BY es.idEsquema DESC LIMIT 300', ('0',))
    expedients = cursor.fetchall()
    conta=0
    indice=0
    for i in expedients: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in expedients: #cada fila es converteix en un objecte de lista
        lista[indice] = EsquemaTots(i[0],i[1],i[2],i[3],i[4]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

class EsquemaTots:
    def __init__(self, idEsquema=0, numExpedient='', nomExpedient='', direcLocal='', nomClient=''):
        self.idEsquema = idEsquema
        self.numExpedient = numExpedient
        self.nomExpedient = nomExpedient
        self.direcLocal = direcLocal
        self.nomClient = nomClient 
        

###########################################################################################################################################################
# ESQUEMES        ESQUEMES        ESQUEMES         ESQUEMES         ESQUEMES         ESQUEMES         ESQUEMES         ESQUEMES    
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def esquema (usuari, idEsquema, idTarea, idHistoria):
    #dataHui
    ara = datetime.datetime.today()
    dataHui = ara.strftime('%Y-%m-%d')
    idEsquema=int(idEsquema)

    if idEsquema == -1:
        #connexio
        db= get_db()
        cursor = db.cursor()
        
        treballadorSelect=tablaTreballadorSelect(cursor, usuari)
        iniciCapsula = tablaCapsulaUltima(cursor, usuari)
        capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
        fitxa=estatFitxa(cursor,usuari)
        intermediariAct=tablaIntermediariAct(cursor)
        ubicacioTots=tablaUbicacioTots(cursor)
        treballadorAct = tablaTreballadorAct(cursor)
        
        #ultim numEsquema
        cursor.execute('SELECT numExpedient FROM esquemes WHERE numExpedient<%s ORDER BY numExpedient DESC LIMIT 0,1', ('a',))
        numEsqUlt = cursor.fetchall()
        numEsqUlt = numEsqUlt[0][0]
            
        #numEsquema Seguent
        numEsqSeg = esquemaSeguent(numEsqUlt)
        
        db.commit()
        db.close()
        
        esquemaSelect =''
        intermediariTots=''
        clientSelect=''
        tareaSelect=''
        tareaCurs=''
        treballadorTots=''
        historiaSelect=''
        historiaEsq=''
        incidenciaAct=''
        incidenciaTots=''
        pressupostEsq=''
        proformaEsq=''
        proformaEsqTot=''
        movimentEsq=''
        liniatemps=''
        eixTemps=''
        linkTarea=''
        rolEsq=''
        color=''
        estat =''
        pressupostPercent=''
        treballPressupost=''
        valeva=''
    else:
        #connexio
        db= get_db()
        cursor = db.cursor()
        treballadorSelect=tablaTreballadorSelect(cursor, usuari)
        iniciCapsula = tablaCapsulaUltima(cursor, usuari)
        capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
        fitxa=estatFitxa(cursor,usuari)
        esquemaSelect=tablaEsquemaSelect(cursor, idEsquema)
        intermediariAct=tablaIntermediariAct(cursor)
        intermediariTots=tablaIntermediariTots(cursor)
        ubicacioTots=tablaUbicacioTots(cursor)
        rolEsq = tablaRolEsq(cursor, idEsquema)
        color = tablaColor(cursor)
        estat = tablaEstat(cursor)
        treballPressupost=tablaTreballPressupost(cursor, idEsquema)
        
        cursor.execute('SELECT valeva FROM pressupostos WHERE idEsquema=%s AND numPressupost IS NOT NULL  ORDER BY idPressupost DESC LIMIT 0,1', (idEsquema,))
        lista2 = cursor.fetchall()
        try:
            valeva = int(lista2[0][0])
        except:
            valeva =''
        
        cursor.execute('SELECT idClient FROM esquemes WHERE idEsquema=%s', (idEsquema,))
        lista = cursor.fetchall()
        try:
            idClient = lista[0][0]
        except:
            idClient = 0
        if idClient > 0:
            clientSelect=tablaClientSelect(cursor,idClient)
        else:
            clientSelect=''
            
        treballadorAct = tablaTreballadorAct(cursor)
        treballadorTots = tablaTreballadorTots(cursor)
        tareaCurs = tablaTareaCurs(cursor, idEsquema)
        
        if idTarea >0:
            tareaSelect=tablaTareaSelect(cursor,idTarea)           
        else:
            tareaSelect=Tarea(-1,'','','','','','','')

        if idHistoria >0:
            historiaSelect=tablaHistoriaSelect(cursor,idHistoria)           
        else:
            historiaSelect= Historia(-1,'','','','','')
            
        historiaEsq = tablaHistoriaEsq(cursor, idEsquema)
        incidenciaAct = tablaIncidenciaAct(cursor)
        incidenciaTots = tablaIncidenciaTots(cursor)
        pressupostEsq= tablaPressupostEsq(cursor, idEsquema)
        numEsqSeg=''
        proformaEsq = tablaProformaEsq(cursor, idEsquema)
        proformaEsqTot = tablaProformaEsqTot(cursor, idEsquema)
        movimentEsq = tablaMovimentsEsquema(cursor, idEsquema)
        
        #toggl = tablaToggl(cursor, idEsquema)
        
        grafica = tablaTareaEsquema(cursor,idEsquema)
        liniatempsVec = grafica
        liniatemps = liniatempsVec[0]
        linkTarea = liniatempsVec[2]
        
        pressupostPercent=tablaPressupostPercent(cursor, idEsquema)
       
        db.commit()
        db.close()
        
        ara = datetime.datetime.today()
        dillunsFinD = dillunsDeuSem(ara,6)
        
        dillunsFin = dataFormat(dillunsFinD)
        
        zoomE = str(6000)
        
        eixTemps = zoomE+","+dillunsFin

    #pasem les llistes al arxiu html
    values = {
             'idEsquema': idEsquema,
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'esquemaSelect': esquemaSelect,
             'intermediariTots': intermediariTots,
             'intermediariAct': intermediariAct,
             'ubicacioTots': ubicacioTots,
             'clientSelect': clientSelect,
             'tareaSelect': tareaSelect,
             'tareaCurs': tareaCurs,
             'treballadorAct': treballadorAct,
             'treballadorTots': treballadorTots,
             'historiaSelect': historiaSelect,
             'historiaEsq': historiaEsq,
             'incidenciaAct': incidenciaAct,
             'incidenciaTots': incidenciaTots,
             'dataHui': dataHui,
             'pressupostEsq': pressupostEsq,
             'numEsqSeg': numEsqSeg,
             'proformaEsq': proformaEsq,
             'proformaEsqTot': proformaEsqTot,
             'movimentEsq': movimentEsq,
             'valeva': valeva,
             'liniatemps':liniatemps,
             'eixTemps': eixTemps,
             'linkTarea': linkTarea,
             'rolEsq': rolEsq,
             'color': color,
             'estat': estat,
             'pressupostPercent': pressupostPercent,
             'treballPressupost': treballPressupost,
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class EsquemaSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            idEsquema= novar(self.request.get('idEsquema'))
            idEsquemaN = int(idEsquema)
            if idEsquemaN == 3848:
                self.redirect("/VacancesSelect")
            idTarea = -1
            idHistoria = -1
            #obtenim valors per al html
            values = esquema(usuari, idEsquema, idTarea, idHistoria)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
            self.response.out.write(template.render(path, values,))

class EsquemaEdita (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idEsquema= novar(self.request.get('idEsquema'))
            idUbicacio= novar(self.request.get('idUbicacio'))
            numExpedient = novar(self.request.get('numExpedient'))
            nomExpedient = novar(self.request.get('nomExpedient'))
            nomClientPos = novar(self.request.get('nomClientPos'))
            telClientPos = novar(self.request.get('telClientPos'))
            direcPos = novar(self.request.get('direcPos'))
            idIntermediari= novar(self.request.get('idIntermediari'))
            direcLocal = novar(self.request.get('direcLocal'))
            titolLlicencia = novar(self.request.get('titolLlicencia'))
            refCatastral = novar(self.request.get('refCatastral'))
            numBoutique = novar(self.request.get('numBoutique'))
            idTreballador = novar(self.request.get('idTreballador'))
            check8 = novar(self.request.get('check8'))
            mapa = novar(self.request.get('mapa'))
            drive = novar(self.request.get('drive'))
            gmap = novar(self.request.get('gmap'))
            

            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('UPDATE esquemes SET idUbicacio=%s, numExpedient=%s, nomExpedient=%s, nomClientPos=%s, telClientPos=%s, direcPos=%s, idIntermediari=%s, direcLocal=%s, titolLlicencia=%s, refCatastral=%s, numBoutique=%s, idTreballador=%s, check8=%s, mapa=%s, drive=%s, gmap=%s WHERE idEsquema=%s', (idUbicacio, numExpedient, nomExpedient, nomClientPos, telClientPos, direcPos, idIntermediari, direcLocal, titolLlicencia, refCatastral, numBoutique, idTreballador, check8, mapa, drive, gmap, idEsquema,))
            
            db.commit()
            db.close()
            
            
            idTarea = -1
            idHistoria = -1
            
            #obtenim valors per al html
            values = esquema(usuari, idEsquema, idTarea, idHistoria)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
            self.response.out.write(template.render(path, values,))

class EsquemaNou(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            idEsquema= -1
            idTarea = -1
            idHistoria = -1
            #obtenim valors per al html
            values = esquema(usuari, idEsquema, idTarea, idHistoria)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
            self.response.out.write(template.render(path, values,))
            
class EsquemaCrea(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            idUbicacio= novar(self.request.get('idUbicacio'))
            numExpedient = novar(self.request.get('numExpedient'))
            nomExpedient = novar(self.request.get('nomExpedient'))
            nomClientPos = novar(self.request.get('nomClientPos'))
            telClientPos = novar(self.request.get('telClientPos'))
            direcPos = novar(self.request.get('direcPos'))
            idIntermediari= novar(self.request.get('idIntermediari'))
            direcLocal = novar(self.request.get('direcLocal'))
            titolLlicencia = novar(self.request.get('titolLlicencia'))
            refCatastral = novar(self.request.get('refCatastral'))
            numBoutique = novar(self.request.get('numBoutique'))
            idTreballador = novar(self.request.get('idTreballador'))
            mapa = novar(self.request.get('mapa'))
            drive = novar(self.request.get('drive'))
            gmap = novar(self.request.get('gmap'))
            idClient = 0
            idTarea = -1
            idHistoria = -1
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            #inserta fila en esquema
            cursor.execute('INSERT INTO esquemes (idUbicacio, idIntermediari, idClient, numExpedient, nomExpedient, nomClientPos, telClientPos, direcPos, direcLocal, titolLlicencia, refCatastral, numBoutique, idTreballador,mapa, drive, gmap) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (idUbicacio, idIntermediari, idClient, numExpedient, nomExpedient, nomClientPos, telClientPos, direcPos, direcLocal, titolLlicencia, refCatastral, numBoutique, idTreballador, mapa, drive, gmap,))
            #obtenir el idEsquema de la fila que hem insertat
            cursor.execute('SELECT idEsquema FROM esquemes ORDER BY idEsquema DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idEsquema = lista[0][0]
            #inserta fila en pressupostos
            cursor.execute('INSERT INTO pressupostos(idEsquema) VALUES (%s)', (idEsquema,))
            #obtenir el idPressupost de la fila que hem insertat
            cursor.execute('SELECT idPressupost FROM pressupostos ORDER BY idPressupost DESC LIMIT 0,1')
            idPressupost = cursor.fetchall()
            #inserta fila en treballs
            cursor.execute('INSERT INTO treballs(idTipoTreball, idPressupost, acceptat, patras, presentat) VALUES (%s, %s, %s, %s, %s)', (69, idPressupost, 1, 0, 0,))
            #obtenir el idTreball de la fila que hem insertat
            
            db.commit()
            db.close()
     
            #obtenim valors per al html
            values = esquema(usuari, idEsquema, idTarea, idHistoria)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
            self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################
def tablaEsquemaSelect(cursor, idEsquema):
    
    cursor.execute('SELECT idEsquema, idUbicacio, idIntermediari, idClient, numPossible, dataPossible, nomClientPos, telClientPos, direcPos, activitat, tramit, esqTancat, nomExpedient, numExpedient, dataExpedient, direcLocal, titolLlicencia, refCatastral, situacioActual, districte, check1, check2, check3, check4, check5, check6, check7, check8, numBoutique, idTreballador, mapa, drive, gmap FROM esquemes WHERE idEsquema=%s', (idEsquema,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista
        lista = Esquema(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22],i[23],i[24],i[25],i[26],i[27], i[28],i[29],i[30],i[31],i[32]) #Modificar si anyadim columna
    return lista 

class Esquema:
    def __init__(self, idEsquema=0, idUbicacio=0, idIntermediari=0, idClient=0, numPossible='', dataPossible='', nomClientPos='', telClientPos='', direcPos='',  activitat='', tramit=0, esqTancat=0, nomExpedient='', numExpedient='', dataExpedient='', direcLocal='', titolLlicencia='', refCatastral='', situacioActual='', districte='', check1=0, check2=0, check3=0, check4=0, check5=0, check6=0, check7=0, check8=0, numBoutique='', idTreballador=0, mapa='', drive='', gmap=''):
        self.idEsquema = idEsquema
        self.idUbicacio = idUbicacio
        self.idIntermediari = idIntermediari
        self.idClient = idClient
        self.numPossible = numPossible
        self.dataPossible = dataPossible
        self.nomClientPos = nomClientPos
        self.telClientPos = telClientPos
        self.direcPos = direcPos
        self.activitat = activitat
        self.tramit = tramit
        self.esqTancat = esqTancat
        self.nomExpedient = nomExpedient
        self.numExpedient = numExpedient
        self.dataExpedient = dataExpedient
        self.direcLocal = direcLocal
        self.titolLlicencia = titolLlicencia
        self.refCatastral = refCatastral
        self.situacioActual = situacioActual
        self.districte = districte
        self.check1 = check1
        self.check2 = check2
        self.check3 = check3
        self.check4 = check4
        self.check5 = check5
        self.check6 = check6
        self.check7 = check7
        self.check8 = check8
        self.numBoutique = numBoutique
        self.idTreballador = idTreballador
        self.mapa = mapa
        self.drive = drive
        self.gmap = gmap
     
def tablaUbicacioTots(cursor):   
    cursor.execute('SELECT idUbicacio, ubicacio, codiUb FROM ubicacions ORDER BY idUbicacio')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Ubicacio(i[0],i[1],i[2]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

class Ubicacio:
    def __init__(self, idUbicacio=0, ubicacio='', codiUb=''):
        self.idUbicacio = idUbicacio
        self.ubicacio = ubicacio
        self.codiUb = codiUb

def tablaToggl(cursor, idEsquema):
    cursor.execute('SELECT  sum(hores), data FROM toggl WHERE idEsquema=%s', (idEsquema,))
    tabla = cursor.fetchall()
    tcoste=0

    for i in tabla: #cada fila es converteix en un objecte de lista
        hores = i[0]
        data = i[1]
        if data:
            cursor.execute('SELECT ch FROM costes WHERE data=%s', (data,))
            valor = cursor.fetchall()
            ch = valor [0][0]
        else:
            hores=0
            ch=0
        coste = ch*hores
        tcoste=coste+tcoste
    
    #Teniendo en cuenta los suplidos y el iva
    #cursor.execute('SELECT  sum(mo.quantitat)-(SELECT SUM(preuSuplido) FROM liniessuplidos as l JOIN factures as f ON l.idFactura=f.idFactura JOIN esquemes as e ON e.idEsquema=f.idEsquema WHERE e.idEsquema=%s) - ((sum(mo.quantitat)-(SELECT SUM(preuSuplido) FROM liniessuplidos as l JOIN factures as f ON l.idFactura=f.idFactura JOIN esquemes as e ON e.idEsquema=f.idEsquema WHERE e.idEsquema=%s,))/1.21)    FROM factures fa INNER JOIN moviments mo ON mo.idFactura = fa.idFactura WHERE fa.idEsquema=%s', (idEsquema,idEsquema,idEsquema,))    
   
    #Antes de tener en cuenta los suplidos
    cursor.execute('SELECT sum(mo.quantitat) FROM factures fa INNER JOIN moviments mo ON mo.idFactura = fa.idFactura WHERE fa.idEsquema=%s', (idEsquema,))
    valor= cursor.fetchall()
    '''
    
    #Caso de no tener que quitar el iva --> caso en el cual no exista numero de factura 
    cursor.execute('SELECT  sum(mo.quantitat) FROM factures fa INNER JOIN moviments mo ON mo.idFactura = fa.idFactura WHERE fa.idEsquema=%s AND fa.factura='' ', (idEsquema,))
    valorUno= cursor.fetchall()
    if(valorUno==None): 
        valorUno=0
    #Caso de tener solo iva de mas y sin suplidos
    cursor.execute('SELECT (sum(mo.quantitat)/1.21) FROM factures fa INNER JOIN moviments mo ON mo.idFactura = fa.idFactura WHERE fa.idEsquema=%s AND fa.factura!=''  ', (idEsquema,))
    valorDos = cursor.fetchall()
    #Caso de tener IVA+SUPLIDOS
    cursor.execute('SELECT ((sum(mo.quantitat)-(SELECT SUM(preuSuplido) FROM liniessuplidos as l JOIN factures as f ON l.idFactura=f.idFactura JOIN esquemes as e ON e.idEsquema=f.idEsquema WHERE e.idEsquema=%s,))/1.21) FROM factures fa INNER JOIN moviments mo ON mo.idFactura = fa.idFactura WHERE fa.idEsquema=%s', (idEsquema,idEsquema,))
    valorTres = cursor.fetchall()
    ingres = valorUno[0][0] + valorDos[0][0]+valorTres[0][0]
    
    '''
    ingres = valor[0][0]
    try:
        rentabilitat=ingres-tcoste
    except:
        rentabilitat=-tcoste

    rentabilitat = "%.2f" %rentabilitat     
  
    return rentabilitat 




###########################################################################################################################################################
#  VIP        VIP         VIP        VIP        VIP        VIP        VIP        VIP        VIP        VIP           
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariVip (usuari):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    
    vipTots = tablaVipTots(cursor)
    
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'vipTots': vipTots,        
              }
    return values

# ACCIONS DEL FORMULARI
####################################
class VipTots (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres

            
                #obtenim valors per al html
                values = formulariVip(usuari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'vip.html') 
                self.response.out.write(template.render(path, values,))   

# ACCIONS DEL FORMULARI
####################################

def tablaVipTots(cursor):   
    cursor.execute('SELECT idEsquema, numBoutique, nomClientPos, telClientPos, direcPos, numExpedient, nomExpedient FROM esquemes WHERE numBoutique>%s AND numBoutique <%s  ORDER BY numBoutique',(0,4))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Vip(i[0],i[1],i[2],i[3],i[4],i[5],i[6]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

class Vip:
    def __init__(self, idEsquema, numBoutique, nomClientPos, telClientPos, direcPos, numExpedient, nomExpedient):
        self.idEsquema = idEsquema
        self.numBoutique = numBoutique
        self.nomClientPos = nomClientPos
        self.telClientPos = telClientPos
        self.direcPos = direcPos
        self.numExpedient = numExpedient
        self.nomExpedient = nomExpedient

###########################################################################################################################################################
# INTERMEDIARIS              INTERMEDIARIS              INTERMEDIARIS              INTERMEDIARIS              INTERMEDIARIS              INTERMEDIARIS            
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariIntermediari (usuari, idIntermediari, idEsquema):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    
    if idIntermediari == -1: #tots intermediaris
        intermediariSelect = ''
        intermediariAct =''
        intermediariTots = tablaIntermediariTots(cursor)
        
    elif idIntermediari == -2: #treballador en blanc
        intermediariSelect = ''
        intermediariTots = ''
        intermediariAct = ''
        
    else: #treballador select
        intermediariSelect = tablaIntermediariSelect(cursor,idIntermediari)
        intermediariAct = ''
        intermediariTots = ''
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'idIntermediari': idIntermediari,
             'idEsquema': idEsquema,
             'intermediariSelect': intermediariSelect,
             'intermediariAct': intermediariAct,
             'intermediariTots': intermediariTots,          
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class IntermediariTots (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idIntermediari = -1
                idEsquema = novar(self.request.get('idEsquema'))
                if idEsquema == "":
                    idEsquema = -1
            
                #obtenim valors per al html
                values = formulariIntermediari(usuari, idIntermediari, idEsquema)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'intermediari.html') 
                self.response.out.write(template.render(path, values,))

class IntermediariGen (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idIntermediari = -1
                idEsquema = -1
            
                #obtenim valors per al html
                values = formulariIntermediari(usuari, idIntermediari, idEsquema)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'intermediari.html') 
                self.response.out.write(template.render(path, values,))


class IntermediariNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1): 
                #parametres
                idIntermediari = -2
                idEsquema = novar(self.request.get('idEsquema'))
            
                #obtenim valors per al html
                values = formulariIntermediari(usuari, idIntermediari, idEsquema)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'intermediari.html') 
                self.response.out.write(template.render(path, values,))
                
            
class IntermediariSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idIntermediari= novar(self.request.get('idIntermediari'))
            idEsquema = novar(self.request.get('idEsquema'))
            
            #parametres

            
            #obtenim valors per al html
            values = formulariIntermediari(usuari, idIntermediari, idEsquema)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'intermediari.html') 
            self.response.out.write(template.render(path, values,))
            
class IntermediariEdita (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idIntermediari= novar(self.request.get('idIntermediari'))
            idEsquema= novar(self.request.get('idEsquema'))
            identificador = novar(self.request.get('identificador'))
            mail = novar(self.request.get('mail'))
            nom = novar(self.request.get('nom'))
            comis = novar(self.request.get('comis'))
            telf = novar(self.request.get('telf'))
            contacte = novar(self.request.get('contacte'))
            comentari = novar(self.request.get('comentari'))
            enActiu = novar(self.request.get('enActiu'))
          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
                       
            cursor.execute('UPDATE intermediaris SET  identificador=%s, mail=%s, nom=%s, comis=%s, telf=%s, contacte=%s, comentari=%s , enActiu=%s WHERE idIntermediari=%s', (identificador, mail, nom, comis, telf, contacte, comentari, enActiu, idIntermediari,))
            
            db.commit()
            db.close()
            
            #obtenim valors per al html
            values = formulariIntermediari(usuari, idIntermediari, idEsquema)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'intermediari.html') 
            self.response.out.write(template.render(path, values,))

class IntermediariCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idEsquema= novar(self.request.get('idEsquema'))
            identificador = novar(self.request.get('identificador'))
            mail = novar(self.request.get('mail'))
            nom = novar(self.request.get('nom'))
            comis = novar(self.request.get('comis'))
            telf = novar(self.request.get('telf'))
            contacte = novar(self.request.get('contacte'))
            comentari = novar(self.request.get('comentari'))
            enActiu = novar(self.request.get('enActiu'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('INSERT INTO intermediaris (identificador, mail, nom, comis, telf, contacte, comentari, enActiu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (identificador, mail, nom, comis, telf, contacte, comentari, enActiu,))
            
            db.commit()
            db.close()

            #parametres
            idIntermediari = -1
            
            #obtenim valors per al html
            values = formulariIntermediari(usuari, idIntermediari, idEsquema)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'intermediari.html') 
            self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaIntermediariTots(cursor):   
    cursor.execute('SELECT idIntermediari, idUbicacio, identificador, mail, nom, comis, telf, contacte, comentari, enActiu FROM intermediaris ORDER BY enActiu DESC, identificador')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        texte = i[7]
        contacte = texte
        texte=i[8]
        comentari=texte
        lista[indice] = Intermediari(i[0],i[1],i[2],i[3],i[4],i[5],i[6],contacte,comentari,i[9]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

def tablaIntermediariAct(cursor):   
    cursor.execute('SELECT idIntermediari, idUbicacio, identificador, mail, nom, comis, telf, contacte, comentari, enActiu FROM intermediaris WHERE enActiu=%s', (1,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Intermediari(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

def tablaIntermediariSelect(cursor, idIntermediari):
    cursor.execute('SELECT idIntermediari, idUbicacio, identificador, mail, nom, comis, telf, contacte, comentari, enActiu FROM intermediaris WHERE idIntermediari=%s', (idIntermediari,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista = Intermediari(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]) #Modificar si anyadim columna 
    return lista 


class Intermediari: 
    def __init__(self, idIntermediari=1, idUbicacio=2, identificador='identificador', mail='mail@mail.com', nom='nom',comis=0,telf='telf',
                 contacte='contacte',comentari='comentari', enActiu=0):
        self.idIntermediari = idIntermediari
        self.idUbicacio= idUbicacio
        self.identificador = identificador
        self.mail = mail
        self.nom = nom
        self.comis= comis
        self.telf= telf
        self.contacte= contacte
        self.comentari= comentari
        self.enActiu = enActiu
        
###########################################################################################################################################################
# CLIENT              CLIENT                CLIENT               CLIENT               CLIENT               CLIENT               CLIENT               CLIENT          
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariClient (usuari, idClient, idEsquema):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    
    if idClient== -1: #tots intermediaris
        clientSelect = ''
        clientTots = tablaClientTots(cursor)
        
    elif idClient==-2:
        clientSelect = ''
        clientTots = ''
        
    else: # select
        clientSelect = tablaClientSelect(cursor,idClient)
        clientTots = tablaClientTots(cursor)
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'idClient': idClient,
             'idEsquema': idEsquema,
             'clientSelect': clientSelect,
             'clientTots': clientTots,          
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class ClientTots (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idClient = -1
                idEsquema = novar(self.request.get('idEsquema'))
            
                #obtenim valors per al html
                values = formulariClient(usuari, idClient, idEsquema)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'client.html') 
                self.response.out.write(template.render(path, values,))
                
class ClientNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idClient = -2
                idEsquema = novar(self.request.get('idEsquema'))
            
                #obtenim valors per al html
                values = formulariClient(usuari, idClient, idEsquema)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'client.html') 
                self.response.out.write(template.render(path, values,))

                
            
class ClientSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idClient= novar(self.request.get('idClient'))
            idEsquema = novar(self.request.get('idEsquema'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('UPDATE esquemes SET idClient=%s WHERE idEsquema=%s', (idClient, idEsquema,)) 
            db.commit()
            db.close()
            
            
            idTarea = -1
            idHistoria = -1
            #obtenim valors per al html
            values = esquema(usuari, idEsquema, idTarea, idHistoria)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
            self.response.out.write(template.render(path, values,))

            

class ClientEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idClient= novar(self.request.get('idClient'))
            idEsquema= novar(self.request.get('idEsquema'))
            nomClient = novar(self.request.get('nomClient'))
            direccio = novar(self.request.get('direccio'))
            codiPostal = novar(self.request.get('codiPostal'))
            cifClient = novar(self.request.get('cifClient'))
            telClient = novar(self.request.get('telClient'))
            contacte = novar(self.request.get('contacte'))
            nomRepres1 = novar(self.request.get('nomRepres1'))
            nifRepres1 = novar(self.request.get('nifRepres1'))
            nomRepres2 = novar(self.request.get('nomRepres2'))
            nifRepres2 = novar(self.request.get('nifRepres2'))
            mailClient = novar(self.request.get('mailClient'))
          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('SELECT cifClient FROM clients WHERE idClient=%s',(idClient,))
            cifANT = cursor.fetchall()
            cifANT = cifANT [0][0]
            cifNOU = cifClient
            
            cursor.execute('SELECT cifClient FROM clients WHERE cifClient=%s',(cifClient,))
            cifs = cursor.fetchall()

            if cifs:
                if cifANT == cifNOU:
                    cursor.execute('UPDATE clients SET nomClient=%s, direccio=%s, codiPostal=%s, cifClient=%s, telClient=%s, contacte=%s, nomRepres1=%s, nifRepres1=%s, nomRepres2=%s, nifRepres2=%s, mailClient=%s WHERE idClient=%s', (nomClient, direccio, codiPostal, cifClient, telClient, contacte, nomRepres1, nifRepres1, nomRepres2, nifRepres2, mailClient, idClient,))          
                    db.commit()
                    db.close()
                else:                    
                    db.commit()
                    db.close()
                    values = formulariInicio(usuari)
                    path = os.path.join(os.path.dirname(__file__), 'clientDuplicat.html') 
                    self.response.out.write(template.render(path, values,))
            else:                       
                cursor.execute('UPDATE clients SET nomClient=%s, direccio=%s, codiPostal=%s, cifClient=%s, telClient=%s, contacte=%s, nomRepres1=%s, nifRepres1=%s, nomRepres2=%s, nifRepres2=%s, mailClient=%s WHERE idClient=%s', (nomClient, direccio, codiPostal, cifClient, telClient, contacte, nomRepres1, nifRepres1, nomRepres2, nifRepres2, mailClient, idClient,))          
                db.commit()
                db.close()
            
            idTarea = -1
            idHistoria = -1
            
            #obtenim valors per al html
            values = esquema(usuari, idEsquema, idTarea, idHistoria)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
            self.response.out.write(template.render(path, values,))

class ClientCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idEsquema= novar(self.request.get('idEsquema'))
            nomClient = novar(self.request.get('nomClient'))
            direccio = novar(self.request.get('direccio'))
            codiPostal = novar(self.request.get('codiPostal'))
            cifClient = novar(self.request.get('cifClient'))
            telClient = novar(self.request.get('telClient'))
            contacte = novar(self.request.get('contacte'))
            nomRepres1 = novar(self.request.get('nomRepres1'))
            nifRepres1 = novar(self.request.get('nifRepres1'))
            nomRepres2 = novar(self.request.get('nomRepres2'))
            nifRepres2 = novar(self.request.get('nifRepres2'))
            mailClient = novar(self.request.get('mailClient'))
            ciutat=''
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('SELECT cifClient FROM clients WHERE cifClient=%s',(cifClient,))
            cifs = cursor.fetchall()
            
            if cifs:
                db.commit()
                db.close()
                values = formulariInicio(usuari)
                path = os.path.join(os.path.dirname(__file__), 'clientDuplicat.html') 
                self.response.out.write(template.render(path, values,))
            else:
                cursor.execute('INSERT INTO clients (nomClient, direccio, ciutat, codiPostal, cifClient, telClient, contacte, nomRepres1, nifRepres1, nomRepres2, nifRepres2, mailClient) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nomClient, direccio, ciutat, codiPostal, cifClient, telClient, contacte, nomRepres1, nifRepres1, nomRepres2, nifRepres2, mailClient,))
                cursor.execute('SELECT idClient FROM clients ORDER BY idClient DESC LIMIT 0,1')
                lista = cursor.fetchall()
                idClient = lista[0][0]
                cursor.execute('UPDATE esquemes SET idClient=%s WHERE idEsquema=%s', (idClient, idEsquema,))          
                db.commit()
                db.close()

            idTarea = -1
            idHistoria = -1
            
            #obtenim valors per al html
            values = esquema(usuari, idEsquema, idTarea, idHistoria)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
            self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaClientTots(cursor):   
    cursor.execute('SELECT idClient, nomClient, direccio, ciutat, codiPostal, cifClient, telClient, contacte, nomRepres1, nifRepres1, nomRepres2, nifRepres2, mailClient FROM clients ORDER BY nomClient')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Client(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

def tablaClientEsquema(cursor):   
    cursor.execute('SELECT c.*, e.idEsquema FROM clients as c JOIN esquemes as e ON e.idClient= c.idClient ORDER BY c.nomClient')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = ClientEsquema(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

class ClientEsquema():
    def __init__(self, idClient=0, nomClient='', direccio='', ciutat='', codiPostal=0, cifClient='', telClient='', contacte='', nomRepres1='', nifRepres1='', nomRepres2='', nifRepres2='', mailClient='', idEsquema=0):
        self.idClient = idClient
        self.nomClient = nomClient
        self.direccio = direccio
        self.ciutat = ciutat
        self.codiPostal = codiPostal
        self.cifClient = cifClient
        self.telClient = telClient
        self.contacte = contacte
        self.nomRepres1 = nomRepres1
        self.nifRepres1 = nifRepres1
        self.nomRepres2 = nomRepres2
        self.nifRepres2 = nifRepres2
        self.mailClient = mailClient
        self.idEsquema = idEsquema


def tablaClientSelect(cursor, idClient):
    cursor.execute('SELECT idClient, nomClient, direccio, ciutat, codiPostal, cifClient, telClient, contacte, nomRepres1, nifRepres1, nomRepres2, nifRepres2, mailClient FROM clients WHERE idClient=%s',(idClient,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista = Client(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12]) #Modificar si anyadim columna 
    return lista 


class Client:
    def __init__(self, idClient=0, nomClient='', direccio='', ciutat='', codiPostal=0, cifClient='', telClient='', contacte='', nomRepres1='', nifRepres1='', nomRepres2='', nifRepres2='', mailClient=''):
        self.idClient = idClient
        self.nomClient = nomClient
        self.direccio = direccio
        self.ciutat = ciutat
        self.codiPostal = codiPostal
        self.cifClient = cifClient
        self.telClient = telClient
        self.contacte = contacte
        self.nomRepres1 = nomRepres1
        self.nifRepres1 = nifRepres1
        self.nomRepres2 = nomRepres2
        self.nifRepres2 = nifRepres2
        self.mailClient = mailClient
        
        
###########################################################################################################################################################
# TAREA              TAREA              TAREA              TAREA              TAREA              TAREA              TAREA              TAREA              TAREA          
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariTarea (usuari, idEsquema, idTarea, idGrafica):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
    
    if idTarea== -1: 
        tareaSelect = ''
        
        
    else: # select
        tareaSelect = tablaTareaSelect(cursor,idTarea)
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    treballadorAct= tablaTreballadorAct(cursor)
    treballadorTots= tablaTreballadorTots(cursor)
    esquemaSelect = tablaEsquemaSelect(cursor, idEsquema)
    color = tablaColor(cursor)
    estat = tablaEstat(cursor)
    
    #dataHui
    ara = datetime.datetime.today()
    dataHui = ara.strftime('%Y-%m-%d')

    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'tareaSelect': tareaSelect,
             'treballadorAct': treballadorAct,
             'treballadorTots': treballadorTots,
             'idEsquema': idEsquema,
             'idTarea': idTarea,
             'idGrafica': idGrafica,
             'dataHui': dataHui,
             'esquemaSelect': esquemaSelect,
             'color': color,
             'estat': estat,
              }
    return values   

# ACCIONS DEL FORMULARI
####################################

                
class TareaNou (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idEsquema = novar(self.request.get('idEsquema'))
                idTarea = -1
                idGrafica = 2
            
                #obtenim valors per al html
                values = formulariTarea(usuari, idEsquema, idTarea, idGrafica)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'tarea.html') 
                self.response.out.write(template.render(path, values,))

                
            
class TareaSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTarea= novar(self.request.get('idTarea'))
            idEsquema = novar(self.request.get('idEsquema'))
            
            #parametres
            idGrafica = 2
            

            #obtenim valors per al html
            values = formulariTarea(usuari, idEsquema, idTarea, idGrafica)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'tarea.html') 
            self.response.out.write(template.render(path, values,))

class TareaSelectCal (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTarea= novar(self.request.get('idTarea'))
            idEsquema = novar(self.request.get('idEsquema'))
            
            #parametres
            idHistoria = -1

            #obtenim valors per al html
            values = esquema(usuari, idEsquema, idTarea, idHistoria)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
            self.response.out.write(template.render(path, values,))

class TareaSelectTemps (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTarea= novar(self.request.get('idTarea'))
            idEsquema = novar(self.request.get('idEsquema'))
            idGrafica = novar(self.request.get('idGrafica'))


            #obtenim valors per al html
            values = formulariTarea(usuari, idEsquema, idTarea, idGrafica)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'tarea.html') 
            self.response.out.write(template.render(path, values,))



            

class TareaEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTarea= novar(self.request.get('idTarea'))
            idEsquema= novar(self.request.get('idEsquema'))
            idTreballador = novar(self.request.get('idTreballador'))
            comentari = novar(self.request.get('comentari'))
            dataTarea = novar(self.request.get('dataTarea'))
            dataFin = novar(self.request.get('dataFin'))
            ok = novar(self.request.get('ok'))
            marca = novar(self.request.get('marca'))
            idCoordinador = novar(self.request.get('idCoordinador'))
            idEstat= novar(self.request.get('idEstat'))
            
            try:
                ok=int(ok)
            except:
                ok=0

            comentari = eliminaComes(comentari)
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('UPDATE tareas SET idTreballador=%s, comentari=%s, dataTarea=%s, ok=%s, marca=%s, dataFin=%s, idEstat=%s WHERE idTarea=%s', (idTreballador, comentari, dataTarea, ok, marca, dataFin, idEstat, idTarea,))          
            cursor.execute('UPDATE esquemes SET idTreballador=%s WHERE idEsquema=%s', (idCoordinador, idEsquema,))          
            db.commit()
            db.close()
            
            
            
            #parametres
            idHistoria = -1

            #obtenim valors per al html
            values = esquema(usuari, idEsquema, idTarea, idHistoria)


            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
            self.response.out.write(template.render(path, values,))

class TareaCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idEsquema= novar(self.request.get('idEsquema'))
            idTreballador = novar(self.request.get('idTreballador'))
            comentari = novar(self.request.get('comentari'))
            dataTarea = novar(self.request.get('dataTarea'))
            ok = novar(self.request.get('ok'))
            marca = novar(self.request.get('marca'))
            idEstat= novar(self.request.get('idEstat'))
            dataFin = dataTarea
            
            comentari = eliminaComes(comentari)
            
            try:
                ok=int(ok)
            except:
                ok=0
            
            idTipoTarea = 1
            cancel=0
            
            idTreballadorN = int(idTreballador)
            if idTreballadorN <>19:
                marca=0
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('SELECT tr.idTreball FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost=tr.idPressupost WHERE pr.idEsquema = %s ORDER BY idTreball LIMIT 0,1', (idEsquema,))
            lista = cursor.fetchall()
            idTreball = lista[0][0]
            cursor.execute('INSERT INTO tareas (idTreballador, idTipoTarea, idTreball, comentari, dataTarea, ok, cancel, marca, dataFin, idEstat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (idTreballador, idTipoTarea, idTreball, comentari, dataTarea, ok, cancel, marca, dataFin, idEstat,))
            cursor.execute('SELECT idTarea FROM tareas ORDER BY idTarea DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idTarea = lista[0][0]
            db.commit()
            db.close()

            
            #parametres
            idTarea=-1
            idHistoria = -1

            #obtenim valors per al html
            values = esquema(usuari, idEsquema, idTarea, idHistoria)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
            self.response.out.write(template.render(path, values,))


# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaTareaCurs(cursor, idEsquema):   
    cursor.execute('SELECT ta.idTarea, ta.idTreballador, ta.idTipoTarea, ta.idTreball, ta.comentari, ta.dataTarea, ta.ok, ta.cancel, ta.marca, ta.dataFin, ta.idEstat FROM esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball WHERE es.idEsquema=%s AND ta.ok=%s ORDER BY ta.idTarea DESC',(idEsquema, 0,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[5])
        dataFin=dataFormat(i[9])
        lista[indice] = Tarea(i[0],i[1],i[2],i[3],i[4],data,i[6],i[7], i[8],dataFin, i[10]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 


def tablaTareaSelect(cursor, idTarea):
    cursor.execute('SELECT idTarea, idTreballador, idTipoTarea, idTreball, comentari, dataTarea, ok, cancel, marca, dataFin, idEstat FROM tareas WHERE idTarea=%s',(idTarea,))
    tabla = cursor.fetchall()  
    for i in tabla: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[5])
        dataFin=dataFormat(i[9])
        lista = Tarea(i[0],i[1],i[2],i[3],i[4],data,i[6],i[7],i[8],dataFin, i[10]) #Modificar si anyadim columna 
    return lista 


class Tarea:
    def __init__(self, idTarea=0, idTreballador=0, idTipoTarea=0, idTreball=0, comentari='', dataTarea='', ok=0, cancel=0, marca=0, dataFin='', idEstat=0):
        self.idTarea = idTarea
        self.idTreballador = idTreballador
        self.idTipoTarea = idTipoTarea
        self.idTreball = idTreball
        self.comentari = comentari
        self.dataTarea = dataTarea
        self.ok = ok
        self.cancel = cancel
        self.marca = marca
        self.dataFin = dataFin
        self.idEstat = idEstat

def tablaColor(cursor):   
    cursor.execute('SELECT idColor, nom, rgb, color FROM color')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Color(i[0],i[1],i[2],i[3]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista

class Color:
    def __init__(self, idColor=0, nom=0, rgb=0, color=0):
        self.idColor = idColor
        self.nom = nom
        self.rgb = rgb
        self.color = color
        
def tablaEstat(cursor):   
    cursor.execute('SELECT idEstat, claveEstat, nomEstat, ordre FROM estat')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Estat(i[0],i[1],i[2],i[3]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista

class Estat:
    def __init__(self, idEstat=0, claveEstat=0, nomEstat=0, ordre=0):
        self.idEstat = idEstat
        self.claveEstat = claveEstat
        self.nomEstat = nomEstat
        self.ordre= ordre
        
###########################################################################################################################################################
# HISTORIA            HISTORIA             HISTORIA             HISTORIA             HISTORIA             HISTORIA             HISTORIA        
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariHistoria (usuari, idEsquema, idHistoria):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
    
    if idHistoria== -1: 
        historiaSelect = ''
        historiaCompleta = ''
    elif idHistoria== -2: #totes
        historiaSelect = ''
        historiaCompleta = tablaHistoriaEsq(cursor, idEsquema)
    else: # select
        historiaSelect = tablaHistoriaSelect(cursor,idHistoria)
        historiaCompleta = ''
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    treballadorAct= tablaTreballadorAct(cursor)
    treballadorTots= tablaTreballadorTots(cursor)
    esquemaSelect = tablaEsquemaSelect(cursor, idEsquema)
    incidenciaTots = tablaIncidenciaTots(cursor)
    incidenciaAct = tablaIncidenciaAct(cursor)
    
    #dataHui
    ara = datetime.datetime.today()
    dataHui = ara.strftime('%Y-%m-%d')

    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'historiaSelect': historiaSelect,
             'historiaCompleta': historiaCompleta,
             'treballadorAct': treballadorAct,
             'treballadorTots': treballadorTots,
             'idEsquema': idEsquema,
             'dataHui': dataHui,
             'esquemaSelect': esquemaSelect,
             'incidenciaTots': incidenciaTots,
             'incidenciaAct': incidenciaAct,
             'idHistoria': idHistoria,
              }
    return values


# ACCIONS DEL FORMULARI
####################################

class HistoriaNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idHistoria= -1
            idEsquema = novar(self.request.get('idEsquema'))
            
            #parametres

            #obtenim valors per al html
            values = formulariHistoria (usuari, idEsquema, idHistoria)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'historia.html') 
            self.response.out.write(template.render(path, values,))

class HistoriaCompleta (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idHistoria= -2
            idEsquema = novar(self.request.get('idEsquema'))
            
            #parametres

            #obtenim valors per al html
            values = formulariHistoria (usuari, idEsquema, idHistoria)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'historia.html') 
            self.response.out.write(template.render(path, values,))

                  
class HistoriaSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idHistoria= novar(self.request.get('idHistoria'))
            idEsquema = novar(self.request.get('idEsquema'))
            
            #parametres

            #obtenim valors per al html
            values = formulariHistoria (usuari, idEsquema, idHistoria)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'historia.html') 
            self.response.out.write(template.render(path, values,))

            

class HistoriaEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idHistoria= novar(self.request.get('idHistoria'))
            idEsquema= novar(self.request.get('idEsquema'))
            idTreballador = novar(self.request.get('idTreballador'))
            idIncidencia = novar(self.request.get('idIncidencia'))
            dataHist = novar(self.request.get('dataHist'))
            historia = novar(self.request.get('historia'))
            contingut = novar(self.request.get('contingut'))

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('UPDATE histories SET idTreballador=%s, idIncidencia=%s, dataHist=%s, historia=%s, contingut=%s WHERE idHistoria=%s', (idTreballador, idIncidencia, dataHist, historia, contingut, idHistoria,))          
            db.commit()
            db.close()
            
            
            #obtenim valors per al html
            values = formulariHistoria (usuari, idEsquema, idHistoria)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'historia.html') 
            self.response.out.write(template.render(path, values,))

class HistoriaCrea (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idEsquema= novar(self.request.get('idEsquema'))
            idTreballador = novar(self.request.get('idTreballador'))
            idIncidencia = novar(self.request.get('idIncidencia'))
            dataHist = novar(self.request.get('dataHist'))
            historia = novar(self.request.get('historia'))
            contingut = novar(self.request.get('contingut'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('INSERT INTO histories (idTreballador, idIncidencia, idEsquema, dataHist, historia, contingut) VALUES (%s, %s, %s, %s, %s, %s)', (idTreballador, idIncidencia, idEsquema, dataHist, historia, contingut,))
            cursor.execute('SELECT idHistoria FROM histories ORDER BY idHistoria DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idHistoria = lista[0][0]
            db.commit()
            db.close()
            
            #obtenim valors per al html
            values = formulariHistoria (usuari, idEsquema, idHistoria)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'historia.html') 
            self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaHistoriaEsq(cursor, idEsquema):   
    cursor.execute('SELECT idHistoria, idTreballador, idIncidencia, idEsquema, dataHist, historia, contingut FROM histories WHERE idEsquema=%s ORDER BY dataHist DESC, idHistoria DESC',(idEsquema,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[4])
        lista[indice] = Historia(i[0],i[1],i[2],i[3],data,i[5], i[6]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 


def tablaHistoriaSelect(cursor, idHistoria):
    cursor.execute('SELECT idHistoria, idTreballador, idIncidencia, idEsquema, dataHist, historia, contingut FROM histories WHERE idHistoria=%s',(idHistoria,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[4])
        lista = Historia(i[0],i[1],i[2],i[3],data,i[5], i[6]) #Modificar si anyadim columna 
    return lista 


class Historia:
    def __init__(self, idHistoria=0, idTreballador=0, idIncidencia=0, idEsquema=0, dataHist='', historia='', contingut=''):
        self.idHistoria = idHistoria
        self.idTreballador = idTreballador
        self.idIncidencia = idIncidencia
        self.idEsquema = idEsquema
        self.dataHist = dataHist
        self.historia = historia
        self.contingut = contingut

###########################################################################################################################################################
# INCIDENCIES          INCIDENCIES          INCIDENCIES          INCIDENCIES          INCIDENCIES          INCIDENCIES          INCIDENCIES            
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariIncidencia (usuari, idIncidencia, idEsquema):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    
    if idIncidencia == -1: 
        incidenciaSelect = ''
        incidenciaTots = tablaIncidenciaTots(cursor)  
    elif idIncidencia == -2: 
        incidenciaSelect = ''
        incidenciaTots =  ''    
    else: 
        incidenciaSelect = tablaIncidenciaSelect(cursor,idIncidencia)
        incidenciaTots = ''
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'idIncidencia': idIncidencia,
             'idEsquema': idEsquema,
             'incidenciaSelect': incidenciaSelect,
             'incidenciaTots': incidenciaTots,          
              }
    return values   

# ACCIONS DEL FORMULARI
####################################

class IncidenciaNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1): 
                #parametres
                idIncidencia = -2
                idEsquema = novar(self.request.get('idEsquema'))
            
                #obtenim valors per al html
                values = formulariIncidencia(usuari, idIncidencia, idEsquema)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'incidencia.html') 
                self.response.out.write(template.render(path, values,))

class IncidenciaTots (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1): 
                #parametres
                idIncidencia = -1
                idEsquema = novar(self.request.get('idEsquema'))
            
                #obtenim valors per al html
                values = formulariIncidencia(usuari, idIncidencia, idEsquema)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'incidencia.html') 
                self.response.out.write(template.render(path, values,))
                
            
class IncidenciaSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idIncidencia= novar(self.request.get('idIncidencia'))
            idEsquema = novar(self.request.get('idEsquema'))
            
            #parametres

            
            #obtenim valors per al html
            values = formulariIncidencia(usuari, idIncidencia, idEsquema)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'incidencia.html') 
            self.response.out.write(template.render(path, values,))
            
class IncidenciaEdita (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idIncidencia= novar(self.request.get('idIncidencia'))
            idEsquema= novar(self.request.get('idEsquema'))
            incidencia = novar(self.request.get('incidencia'))
            enActiu = novar(self.request.get('enActiu'))
          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
                       
            cursor.execute('UPDATE incidencies SET  incidencia=%s, enActiu=%s WHERE idIncidencia=%s', (incidencia, enActiu, idIncidencia,))
            
            db.commit()
            db.close()
            
            
            idIncidencia=-1
            
            #obtenim valors per al html
            values = formulariIncidencia(usuari, idIncidencia, idEsquema)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'incidencia.html') 
            self.response.out.write(template.render(path, values,))

class IncidenciaCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idEsquema= novar(self.request.get('idEsquema'))
            incidencia = novar(self.request.get('incidencia'))
            enActiu = novar(self.request.get('enActiu'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('INSERT INTO incidencies (incidencia, enActiu) VALUES (%s, %s)', (incidencia, enActiu,))
            
            db.commit()
            db.close()

            #parametres
            idIncidencia = -1
            
            #obtenim valors per al html
            values = formulariIncidencia(usuari, idIncidencia, idEsquema)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'incidencia.html') 
            self.response.out.write(template.render(path, values,))


# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaIncidenciaTots(cursor):   
    cursor.execute('SELECT idIncidencia, incidencia, enActiu FROM incidencies ORDER BY enActiu DESC, incidencia')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Incidencia(i[0],i[1],i[2]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

def tablaIncidenciaAct(cursor):   
    cursor.execute('SELECT idIncidencia, incidencia, enActiu FROM incidencies WHERE enActiu=%s ORDER BY incidencia',(1,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Incidencia(i[0],i[1],i[2]) #Modificar si anyadim columna 
        indice=indice+1    
    return lista 

def tablaIncidenciaSelect(cursor, idIncidencia):
    cursor.execute('SELECT idIncidencia, incidencia, enActiu FROM incidencies WHERE idIncidencia=%s',(idIncidencia,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista = Incidencia(i[0],i[1],i[2]) #Modificar si anyadim columna 
    return lista 


class Incidencia: 
    def __init__(self, idIncidencia=0, incidencia='', enActiu=0):
        self.idIncidencia = idIncidencia
        self.incidencia= incidencia
        self.enActiu = enActiu  

###########################################################################################################################################################
# PRESSUPOSTOS              PRESSUPOSTOS              PRESSUPOSTOS              PRESSUPOSTOS              PRESSUPOSTOS              PRESSUPOSTOS          
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariPressupost (usuari, idPressupost, idEsquema):
    
    #dataHui
    ara = datetime.datetime.today()
    dataHui = ara.strftime('%Y-%m-%d')

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    
    if idPressupost == -1: #nou
        #num pressup ultim
        cursor.execute('SELECT numPressupost FROM pressupostos ORDER BY numPressupost DESC LIMIT 0,1')
        lista = cursor.fetchall()
        numPressupostA = lista[0][0]
        numPressupost = pressupostSeguent(numPressupostA)
        cursor.execute('SELECT nomExpedient, idUbicacio FROM esquemes WHERE idEsquema=%s', (idEsquema,))
        lista = cursor.fetchall()
        nomPressupost = lista[0][0]
        idUbicacio = 3
        
        pressupostSelect = Pressupost(0,0,numPressupost,nomPressupost,dataHui,'','',0,0,0,0,0,0,1,idUbicacio,1,0)
        treballPressup = ''
        tipoTreballTots = ''
        ubicacioTots = tablaUbicacioTots(cursor)

        
    else: # select
        pressupostSelect = tablaPressupostSelect(cursor,idPressupost)
        treballPressup = tablaTreballPressup(cursor, idPressupost)
        tipoTreballTots = tablaTipoTreballTots(cursor)
        ubicacioTots = tablaUbicacioTots(cursor)


    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'idPressupost': idPressupost,
             'idEsquema': idEsquema,
             'pressupostSelect': pressupostSelect, 
             'treballPressup': treballPressup,
             'tipoTreballTots': tipoTreballTots, 
             'ubicacioTots': ubicacioTots,
             'dataHui': dataHui,
              }
    return values  

# ACCIONS DEL FORMULARI
####################################

                
class PressupostNou (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idEsquema = novar(self.request.get('idEsquema'))
                idPressupost = -1
            
                #obtenim valors per al html
                values = formulariPressupost(usuari, idPressupost, idEsquema)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'pressupost.html') 
                self.response.out.write(template.render(path, values,))

                
            
class PressupostSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idPressupost= novar(self.request.get('idPressupost'))
            idEsquema = novar(self.request.get('idEsquema'))

            #obtenim valors per al html
            values = formulariPressupost(usuari, idPressupost, idEsquema)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'pressupost.html') 
            self.response.out.write(template.render(path, values,))

            

class PressupostEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idPressupost= novar(self.request.get('idPressupost'))
            idEsquema= novar(self.request.get('idEsquema'))
            numPressupost = novar(self.request.get('numPressupost'))
            nomPressupost = novar(self.request.get('nomPressupost'))
            dataPressupost = novar(self.request.get('dataPressupost'))
            titol = novar(self.request.get('titol'))
            enActiu = novar(self.request.get('enActiu'))
            idUbicacio = novar(self.request.get('idUbicacio'))
            enPis = novar(self.request.get('enPis'))
            valeva = novar(self.request.get('valeva'))

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('UPDATE pressupostos SET numPressupost=%s, nomPressupost=%s, dataPressupost=%s, titol=%s, enActiu=%s, idUbicacio=%s, enPis=%s, valeva=%s WHERE idPressupost=%s', (numPressupost, nomPressupost, dataPressupost, titol, enActiu, idUbicacio, enPis, valeva, idPressupost,))          
            db.commit()
            db.close()

            #obtenim valors per al html
            values = formulariPressupost(usuari, idPressupost, idEsquema)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'pressupost.html') 
            self.response.out.write(template.render(path, values,))

class PressupostCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idPressupost= novar(self.request.get('idPressupost'))
            idEsquema= novar(self.request.get('idEsquema'))
            numPressupost = novar(self.request.get('numPressupost'))
            nomPressupost = novar(self.request.get('nomPressupost'))
            dataPressupost = novar(self.request.get('dataPressupost'))
            titol = novar(self.request.get('titol'))
            enActiu = novar(self.request.get('enActiu'))
            idUbicacio = novar(self.request.get('idUbicacio'))
            enPis = novar(self.request.get('enPis'))

            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('INSERT INTO pressupostos (idEsquema, numPressupost, nomPressupost, dataPressupost, titol, enActiu, idUbicacio, enPis) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (idEsquema, numPressupost, nomPressupost, dataPressupost, titol, enActiu, idUbicacio, enPis,))
            cursor.execute('SELECT idPressupost FROM pressupostos ORDER BY idPressupost DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idPressupost = lista[0][0]
            db.commit()
            db.close()

            #obtenim valors per al html
            values = formulariPressupost(usuari, idPressupost, idEsquema)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'pressupost.html') 
            self.response.out.write(template.render(path, values,))


# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaPressupostEsq(cursor, idEsquema):   
    cursor.execute('SELECT idPressupost, idEsquema, numPressupost, nomPressupost, dataPressupost, titol, comentaris, nota1, nota2, nota3, nota4, nota5, nota6, enActiu, idUbicacio, enPis, valeva FROM pressupostos WHERE idEsquema=%s ORDER BY idPressupost LIMIT 1,50',(idEsquema,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[4])
        lista[indice] = Pressupost(i[0],i[1],i[2],i[3],data,i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 


def tablaPressupostSelect(cursor, idPressupost):
    cursor.execute('SELECT idPressupost, idEsquema, numPressupost, nomPressupost, dataPressupost, titol, comentaris, nota1, nota2, nota3, nota4, nota5, nota6, enActiu, idUbicacio, enPis, valeva FROM pressupostos WHERE idPressupost=%s',(idPressupost,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[4])
        lista = Pressupost(i[0],i[1],i[2],i[3],data,i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16]) #Modificar si anyadim columna 
    return lista 


class Pressupost:
    def __init__(self, idPressupost=0, idEsquema=0, numPressupost='', nomPressupost='', dataPressupost='', titol='', comentaris='', nota1=0, nota2=0, nota3=0, nota4=0, nota5=0, nota6=0, enActiu=0, idUbicacio=0, enPis=0, valeva=0):
        self.idPressupost = idPressupost
        self.idEsquema = idEsquema
        self.numPressupost = numPressupost
        self.nomPressupost = nomPressupost
        self.dataPressupost = dataPressupost
        self.titol = titol
        self.comentaris = comentaris
        self.nota1 = nota1
        self.nota2 = nota2
        self.nota3 = nota3
        self.nota4 = nota4
        self.nota5 = nota5
        self.nota6 = nota6
        self.enActiu = enActiu
        self.idUbicacio = idUbicacio
        self.enPis = enPis
        self.valeva = valeva

def tablaPressupostPercent(cursor, idEsquema):
    cursor.execute('SELECT idPressupost FROM pressupostos WHERE idEsquema=%s AND numPressupost IS NOT NULL ORDER BY idPressupost DESC LIMIT 0,1',(idEsquema,))
    vector = cursor.fetchall()
    try:
        idPressupost = vector[0][0]      
        cursor.execute('SELECT SUM(tr.preu) AS preuT FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost = tr.idPressupost WHERE tr.idPressupost=%s AND tr.acceptat =%s AND pr.enActiu=%s GROUP BY tr.idPressupost',(idPressupost, 1,1,))
        tabla = cursor.fetchall()
        totalPressup = tabla[0][0]
        try:
                total=float(totalPressup)
                tot="%.2f" %total
                t20=total*0.2
                t20t="%.2f" %t20
                t30=total*0.3
                t30t="%.2f" %t30
                t40=total*0.4
                t40t="%.2f" %t40
                t50=total*0.5
                t50t="%.2f" %t50
                t60=total*0.6
                t60t="%.2f" %t60
                t70=total*0.7
                t70t="%.2f" %t70
                lista = PressupostPercent(idPressupost, total, tot, t20t,t30t,t40t,t50t,t60t,t70t) #Modificar si anyadim columna 
        except:
                lista=""
    except:
        lista=""
    return lista 

class PressupostPercent:
    def __init__(self, idPressupost, total, tot, t20t,t30t,t40t,t50t,t60t,t70t):
        self.idPressupost = idPressupost
        self.total = total
        self.tot = tot
        self.t20t = t20t
        self.t30t = t30t
        self.t40t = t40t
        self.t50t = t50t
        self.t60t = t60t
        self.t70t = t70t

def tablaTreballPressupost(cursor, idEsquema):
    cursor.execute('SELECT idPressupost FROM pressupostos WHERE idEsquema=%s AND numPressupost IS NOT NULL ORDER BY idPressupost DESC LIMIT 0,1',(idEsquema,))
    vector = cursor.fetchall()
    try:
        idPressupost = vector[0][0]      
        cursor.execute('SELECT tr.idTreball, tr.idTipoTreball, tt.treball, tr.idTreballador, tb.claveTreballador, tr.enActiu, tr.enTabla, tr.ordre, tr.preu, es.numExpedient,es.nomExpedient, es.idEsquema, tr.enTop FROM esquemes es INNER JOIN (pressupostos pr INNER JOIN (treballadors tb INNER JOIN (tipostreball tt INNER JOIN treballs tr ON tt.idTipoTreball=tr.idTipoTreball) ON tb.idTreballador = tr.idTreballador) ON pr.idPressupost = tr.idPressupost) ON es.idEsquema = pr.idEsquema WHERE pr.idPressupost=%s',(idPressupost,))
        tabla = cursor.fetchall()
        conta=0
        indice=0
        for i in tabla: #conta el numero de files de la tabla
            conta=conta+1
        lista=[0]*conta #creem lista   
        for i in tabla: #cada fila es converteix en un objecte de lista
            idTreball=i[0]
            capMax=capsulaMaxTreball(cursor, idTreball)
            cap=capsulaTreball(cursor, idTreball)
            
            lista[indice] = TreballOrdre(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],capMax,cap) #Modificar si anyadim columna 
            indice=indice+1   
    except:
        lista=""
    return lista 

def capsulaMaxTreball(cursor, idTreball):
    cursor.execute('SELECT preu FROM treballs WHERE idTreball=%s',(idTreball,))
    vector = cursor.fetchall()
    preu = vector [0][0]
    cursor.execute('SELECT valorCap FROM constants WHERE idConstant=%s',(2,))
    vector2 = cursor.fetchall()
    valorCap = vector2 [0][0]
    capMax= int(preu/valorCap)
    return capMax

def capsulaTreball (cursor, idTreball):
    cursor.execute('SELECT  COUNT(idCapsula) FROM treballs tr INNER JOIN capsula ca ON tr.idTreball = ca.idTreball WHERE  ca.idTreball=%s',(idTreball,))
    vector = cursor.fetchall()
    ncap=vector[0][0]
    try:
        cap=int(ncap)
    except:
        cap=0
    return cap

class TreballOrdre:
    def __init__(self, idTreball, idTipoTreball, treball, idTreballador,claveTreballador,enActiu,enTabla,ordre,preu,numExpedient, nomExpedient, idEsquema,enTop,capMax,cap):
        self.idTreball = idTreball
        self.idTipoTreball = idTipoTreball
        self.treball = treball
        self.idTreballador = idTreballador
        self.claveTreballador = claveTreballador
        self.enActiu = enActiu
        self.enTabla = enTabla
        self.ordre = ordre
        self.preu = preu
        self.numExpedient = numExpedient
        self.nomExpedient = nomExpedient
        self.idEsquema = idEsquema
        self.enTop = enTop
        self.capMax = capMax
        self.cap = cap
        
###########################################################################################################################################################
# IMPRIMIR PRESSUP              IMPRIMIR PRESSUP              IMPRIMIR PRESSUP              IMPRIMIR PRESSUP              IMPRIMIR PRESSUP          
###########################################################################################################################################################


 

class ImpPressupost(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):           
            #captura camps del html
            idPressupost = novar(self.request.get('idPressupost'))
            detallT = novar(self.request.get('detall'))
            detall = int(detallT)

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('SELECT SUM(preu) AS preuT FROM treballs WHERE idPressupost=%s AND acceptat =%s GROUP BY idPressupost',(idPressupost, 1,))
            tabla = cursor.fetchall()
            totalPressup = tabla[0][0]
            cursor.execute('SELECT tipoIVA FROM constants WHERE idConstant=%s',(1,))
            tabla = cursor.fetchall()
            tipoIVA = tabla [0][0]
            iva = totalPressup*tipoIVA
            totalBruto = totalPressup*(1+tipoIVA)
            treballsPressupImp = tablaTreballPressupImp (cursor, idPressupost)
            pressupSelect = tablaPressupostSelect(cursor, idPressupost)
            tiposTreball = tablaTipoTreballTots (cursor)
            bancs = tablaBancs (cursor)
            
            total30=totalBruto*0.3
            #donar formato
            totalPressup = "%.2f" %totalPressup
            iva = "%.2f" %iva
            totalBruto = "%.2f" %totalBruto
            tipoIVA = tipoIVA*100
            total30 = "%.2f" %total30
            #tanca conexio
            db.commit()
            db.close()
        
        
        
        #pasem les llistes al arxiu html
        values = {
            'pressupSelect': pressupSelect,
            'treballsPressupImp': treballsPressupImp,
            'bancs': bancs,
            'tiposTreball': tiposTreball,
            'totalPressup': totalPressup,
            'iva': iva,
            'totalBruto': totalBruto,
            'tipoIVA': tipoIVA,
            'detall': detall,
            'total30': total30,
                  }
        
        #imprimim el arxiu html    
        path = os.path.join(os.path.dirname(__file__), 'impPressupIA.html')
        self.response.out.write(template.render(path, values,))
        
# FUNCIONS SECUNDARIES DEL FORMULARI
####################################

def tablaBancs(cursor):
    cursor.execute('SELECT idBanc, idUbicacio, claveBanc, nomBanc, numConter FROM bancs')
    bancs = cursor.fetchall()
    conta=0
    indice=0
    for i in bancs: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in bancs: #cada fila es converteix en un objecte de lista
        lista[indice] = Banc(i[0],i[1],i[2],i[3],i[4]) #Modificar si anyadim columna
        indice=indice+1   
    return lista

class Banc:
    def __init__(self, idBanc=0, idUbicacio=0, claveBanc='', nomBanc='', numConter=''):
        self.idBanc = idBanc
        self.idUbicacio = idUbicacio
        self.claveBanc = claveBanc
        self.nomBanc = nomBanc
        self.numConter = numConter
            
###########################################################################################################################################################
# TREBALLS        TREBALLS        TREBALLS        TREBALLS        TREBALLS        TREBALLS        TREBALLS        TREBALLS        TREBALLS        TREBALLS                 
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariTreball (usuari, idPressupost, idEsquema, idTreball):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    treballPressup = tablaTreballPressup(cursor, idPressupost)
    tipoTreballTots = tablaTipoTreballTots(cursor)
    
    if idTreball == -1: #nou
        tipoTreballAct = tablaTipoTreballAct(cursor)
        treballSelect = ''
        
    else: # select
        tipoTreballAct = tablaTipoTreballAct(cursor)
        treballSelect = tablaTreballPressupSelect(cursor, idTreball)
        
        
        


    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'idPressupost': idPressupost,
             'idEsquema': idEsquema,
             'idTreball': idTreball,
             'tipoTreballAct': tipoTreballAct,
             'tipoTreballTots': tipoTreballTots,
             'treballSelect': treballSelect,
             'treballPressup': treballPressup,
              }
    return values 

# ACCIONS DEL FORMULARI
####################################

                
class TreballNou (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            #parametres
            idEsquema = novar(self.request.get('idEsquema'))
            idPressupost = novar(self.request.get('idPressupost'))
            
            idTreball=-1
            #obtenim valors per al html
            values = formulariTreball(usuari, idPressupost, idEsquema, idTreball)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'treball.html') 
            self.response.out.write(template.render(path, values,))

                
            
class TreballSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #parametres
            idEsquema = novar(self.request.get('idEsquema'))
            idPressupost = novar(self.request.get('idPressupost'))
            idTreball= novar(self.request.get('idTreball'))
            
            #obtenim valors per al html
            values = formulariTreball(usuari, idPressupost, idEsquema, idTreball)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'treball.html') 
            self.response.out.write(template.render(path, values,))

            

class TreballEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTreball= novar(self.request.get('idTreball'))
            idEsquema= novar(self.request.get('idEsquema'))
            idTipoTreball = novar(self.request.get('idTipoTreball'))
            idPressupost = novar(self.request.get('idPressupost'))
            preu = novar(self.request.get('preu'))
            acceptat = novar(self.request.get('acceptat'))

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('UPDATE treballs SET idTipoTreball=%s, preu=%s, acceptat=%s WHERE idTreball=%s', (idTipoTreball, preu, acceptat, idTreball,))          
            db.commit()
            db.close()
            

            idTreball = -1
            
            #obtenim valors per al html
            values = formulariTreball(usuari, idPressupost, idEsquema, idTreball)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'treball.html') 
            self.response.out.write(template.render(path, values,))

class TreballAcceptatNo (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTreball= novar(self.request.get('idTreball'))
            idEsquema= novar(self.request.get('idEsquema'))
            idPressupost = novar(self.request.get('idPressupost'))
            acceptat = 0

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('UPDATE treballs SET acceptat=%s WHERE idTreball=%s', (acceptat, idTreball,))          
            db.commit()
            db.close()
            
            
            idTreball=-1
            
            #obtenim valors per al html
            values = formulariTreball(usuari, idPressupost, idEsquema, idTreball)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'treball.html') 
            self.response.out.write(template.render(path, values,))

class TreballAcceptatNoPre (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTreball= novar(self.request.get('idTreball'))
            idEsquema= novar(self.request.get('idEsquema'))
            idPressupost = novar(self.request.get('idPressupost'))
            acceptat = 0

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('UPDATE treballs SET acceptat=%s WHERE idTreball=%s', (acceptat, idTreball,))          
            db.commit()
            db.close()
            
            
            #obtenim valors per al html
            values = formulariPressupost(usuari, idPressupost, idEsquema)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'pressupost.html') 
            self.response.out.write(template.render(path, values,))
            
class TreballCrea (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idEsquema= novar(self.request.get('idEsquema'))
            idTipoTreball = novar(self.request.get('idTipoTreball'))
            idPressupost = novar(self.request.get('idPressupost'))
            preu = novar(self.request.get('preu'))
            acceptat = novar(self.request.get('acceptat'))
            treballNH = novar(self.request.get('treballNH'))
            claveTreball = "TNH"
            
            idTipoTreballN = int(idTipoTreball)
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            if idTipoTreballN == -1:
                cursor.execute('INSERT INTO tipostreball (claveTreball, treball, enActiu) VALUES (%s, %s, %s)', (claveTreball, treballNH, 0,))
                cursor.execute('SELECT idTipoTreball FROM tipostreball ORDER BY idTipoTreball DESC LIMIT 0,1')
                lista = cursor.fetchall()
                idTipoTreball = lista[0][0]        
            
            cursor.execute('INSERT INTO treballs (idTipoTreball, idPressupost, preu, acceptat) VALUES (%s, %s, %s, %s)', (idTipoTreball, idPressupost, preu, acceptat,))
            
            
            db.commit()
            db.close()

            idTreball = -1
            
            #obtenim valors per al html
            values = formulariTreball(usuari, idPressupost, idEsquema, idTreball)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'treball.html') 
            self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaTreballPressup(cursor, idPressupost):   
    cursor.execute('SELECT idTreball, idTipoTreball, idPressupost, dataTreball, preu, acceptat, patras, presentat, comentari, expAj, numVisado FROM treballs WHERE idPressupost=%s AND acceptat >=%s ORDER BY idTreball',(idPressupost, 1,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Treball(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

def tablaTreballPressupImp(cursor, idPressupost):   
    cursor.execute('SELECT idTreball, idTipoTreball, idPressupost, dataTreball, preu, acceptat, patras, presentat, comentari, expAj, numVisado FROM treballs WHERE idPressupost=%s AND acceptat =%s ORDER BY idTreball',(idPressupost, 1,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Treball(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

def tablaTreballPressupSelect(cursor, idTreball):
    cursor.execute('SELECT idTreball, idTipoTreball, idPressupost, dataTreball, preu, acceptat, patras, presentat, comentari, expAj, numVisado FROM treballs WHERE idTreball=%s',(idTreball,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista = Treball(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]) #Modificar si anyadim columna 
    return lista 


class Treball:
    def __init__(self, idTreball=0, idTipoTreball=0, idPressupost=0, dataTreball='', preu=0, acceptat=1, patras=0, presentat=0, comentari='', expAj='', numVisado=''):
        self.idTreball = idTreball
        self.idTipoTreball = idTipoTreball
        self.idPressupost = idPressupost
        self.dataTreball = dataTreball
        self.preu = preu
        self.acceptat = acceptat
        self.patras = patras
        self.presentat = presentat
        self.comentari = comentari
        self.expAj = expAj
        self.numVisado = numVisado
        
###########################################################################################################################################################
# TREBALL ORDRE           TREBALL ORDRE            TREBALL ORDRE           TREBALL ORDRE           TREBALL ORDRE           TREBALL ORDRE                                 
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariTreballOrdre (usuari, idTreball, idEsquema, tabla, idTreballador):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    treballadorTots=tablaTreballadorTots(cursor)
    treballadorAct=tablaTreballadorAct(cursor)
    esquemaSelect=tablaEsquemaSelect(cursor, idEsquema)
    
    if idTreballador == -1:
        treballTabla = tablaTreballTablaTots(cursor)
    else:
        treballTabla = tablaTreballTablaTreballador(cursor,idTreballador)

    
    if idTreball == -1: #tots
        idTreballadorNum=int(idTreballador)
        treballSelectOrdre = TreballOrdreS(-1,'',idTreballadorNum,'','','','','')
    else: # select
        treballSelectOrdre = tablaTreballSelectOrdre(cursor, idTreball)
        
    idTreballador=int(idTreballador)  
        
        


    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'treballTabla':treballTabla,
             'treballSelectOrdre': treballSelectOrdre,
             'idEsquema': idEsquema,
             'treballadorTots': treballadorTots,
             'treballadorAct': treballadorAct,
             'esquemaSelect': esquemaSelect,
             'tabla': tabla,
             'idTreballador': idTreballador,
             'idTreball': idTreball,
              }
    return values 

# ACCIONS DEL FORMULARI
####################################

                
class TreballTabla (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            #parametres
            idTreball=-1
            idEsquema=-1
            tabla=1
            idTreballador=-1

            #obtenim valors per al html
            values = formulariTreballOrdre(usuari,idTreball,idEsquema, tabla, idTreballador)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'treballOrdre.html') 
            self.response.out.write(template.render(path, values,))
            
class TreballadorTablaSelect (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            #parametres
            idTreball=-1
            idEsquema=-1
            tabla=1
            idTreballador= novar(self.request.get('idTreballador'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            renumerar(cursor, idTreballador)
            
            db.commit()
            db.close()
            

            #obtenim valors per al html
            values = formulariTreballOrdre(usuari,idTreball,idEsquema, tabla, idTreballador)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'treballOrdre.html') 
            self.response.out.write(template.render(path, values,))

                
            
class TreballSelectOrdre (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #parametres
            idTreball= novar(self.request.get('idTreball'))
            tabla=0
            idTreballador=-1
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('SELECT pr.idEsquema FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost=tr.idPressupost WHERE tr.idTreball=%s',(idTreball,))
            vector = cursor.fetchall()
            idEsquema = vector[0][0]
            db.commit()
            db.close()
            
            #obtenim valors per al html
            values = formulariTreballOrdre(usuari,idTreball, idEsquema, tabla, idTreballador)
            
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'treballOrdre.html') 
            self.response.out.write(template.render(path, values,))
            
class TreballSelectOrdreTabla (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #parametres
            idTreball= novar(self.request.get('idTreball'))
            tabla=1
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('SELECT pr.idEsquema, tr.idTreballador FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost=tr.idPressupost WHERE tr.idTreball=%s',(idTreball,))
            vector = cursor.fetchall()
            idEsquema = vector[0][0]
            idTreballador = vector[0][1]
            db.commit()
            db.close()
            
            #obtenim valors per al html
            values = formulariTreballOrdre(usuari,idTreball, idEsquema,tabla,idTreballador)
            
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'treballOrdre.html') 
            self.response.out.write(template.render(path, values,))

            

class TreballEditaOrdre (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTreball= novar(self.request.get('idTreball'))
            enActiu = novar(self.request.get('enActiu'))
            enTop = novar(self.request.get('enTop'))
            enTabla = novar(self.request.get('enTabla'))
            preu = novar(self.request.get('preu'))
            idTreballador = novar(self.request.get('idTreballador'))
            idEsquema= novar(self.request.get('idEsquema'))
            tabla=0
            
            enTopN=int(enTop)
            
            if enTopN==1:
                enActiu=1
                enTabla=1
            
            

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('UPDATE treballs SET preu=%s, enTabla=%s, enActiu=%s, idTreballador=%s, enTop=%s WHERE idTreball=%s', (preu, enTabla, enActiu, idTreballador, enTop, idTreball,))          
            db.commit()
            db.close()
            

            
            #obtenim valors per al html
            values = formulariTreballOrdre(usuari,idTreball,idEsquema,tabla,idTreballador)
            
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'treballOrdre.html') 
            self.response.out.write(template.render(path, values,))

class TreballValeva (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html

            idEsquema= novar(self.request.get('idEsquema'))
            idTreballador= 19
            


          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('UPDATE pressupostos SET valeva=%s WHERE idEsquema=%s', (1, idEsquema,))
            cursor.execute('SELECT idPressupost FROM pressupostos WHERE idEsquema=%s AND numPressupost IS NOT NULL ORDER BY idPressupost DESC LIMIT 0,1',(idEsquema,))
            vector = cursor.fetchall()
            idPressupost = vector[0][0]      
            cursor.execute('SELECT idTreball FROM treballs WHERE idPressupost=%s',(idPressupost,))
            tabla = cursor.fetchall() 
            for i in tabla: #cada fila es converteix en un objecte de lista
                idTreball=i[0]
                cursor.execute('UPDATE treballs SET enActiu=%s, enTabla=%s, idTreballador=%s WHERE idTreball=%s', (1,1, idTreballador, idTreball,))

                      
            db.commit()
            db.close()
            
            idTarea = -1
            idHistoria = -1
            #obtenim valors per al html
            values = esquema(usuari, idEsquema, idTarea, idHistoria)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
            self.response.out.write(template.render(path, values,))

class TreballEditaOrdreTabla (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTreball= novar(self.request.get('idTreball'))
            ordreNou= novar(self.request.get('ordre'))
            enTop = novar(self.request.get('enTop'))
            enActiu = novar(self.request.get('enActiu'))
            preu = novar(self.request.get('preu'))
            idTreballador = novar(self.request.get('idTreballador'))
            idTreballadorNou = novar(self.request.get('idTreballadorNou'))
            idEsquema= novar(self.request.get('idEsquema'))
            tabla=1

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            if idTreballador == idTreballadorNou:
                
                cursor.execute('UPDATE treballs SET preu=%s, enTop=%s, enActiu=%s, idTreballador=%s WHERE idTreball=%s', (preu, enTop, enActiu, idTreballadorNou, idTreball,))
                cursor.execute('SELECT ordre FROM treballs WHERE idTreball=%s',(idTreball,))
                vector = cursor.fetchall()
                ordreVell = vector[0][0]
                if ordreVell <> ordreNou:
                    ordre(cursor,idTreballadorNou,idTreball,ordreNou)
            else:
                ordreNou=1000  
                cursor.execute('UPDATE treballs SET preu=%s, enTop=%s, enActiu=%s, idTreballador=%s, ordre=%s WHERE idTreball=%s', (preu, enTop, enActiu, idTreballadorNou, ordreNou, idTreball,))
                renumerar(cursor, idTreballador)
            
            
            db.commit()
            db.close()
            
            idTreball=-1
            

            
            #obtenim valors per al html
            values = formulariTreballOrdre(usuari,idTreball,idEsquema,tabla, idTreballador)
            
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'treballOrdre.html') 
            self.response.out.write(template.render(path, values,))
            



class TreballenTablaNo (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTreball= novar(self.request.get('idTreball'))
            idEsquema= -1
            enTabla = 0
            tabla=1

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('UPDATE treballs SET enTabla=%s WHERE idTreball=%s', (enTabla, idTreball,))
            cursor.execute('SELECT idTreballador FROM treballs WHERE idTreball=%s',(idTreball,))
            vector = cursor.fetchall()
            idTreballador = vector[0][0]
            
            renumerar(cursor, idTreballador)   
                
            db.commit()
            db.close()
            
            idTreball=-1
            
            #obtenim valors per al html
            values = formulariTreballOrdre(usuari,idTreball,idEsquema,tabla,idTreballador)
            
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'treballOrdre.html') 
            self.response.out.write(template.render(path, values,))
            
class TreballenActiuNo (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTreball= novar(self.request.get('idTreball'))
            enActiu = 0

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('UPDATE treballs SET enActiu=%s WHERE idTreball=%s', (enActiu, idTreball,))  
                
            db.commit()
            db.close()
            
            idGrafica = 2
            idTreballador = usuari
            idEsquema = -1
            idTarea = -1
            idHistoria= -1
            idTareaCrea = -1
            
            #obtenim valors per al html
            values = formulariLiniatemps(usuari, idGrafica, idTreballador, idEsquema, idTarea, idHistoria, idTareaCrea)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'liniatemps.html') 
            self.response.out.write(template.render(path, values,))
            

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################

def tablaTreballTablaTots(cursor):   
     
    cursor.execute('SELECT tr.idTreball, tr.idTipoTreball, tt.treball, tr.idTreballador, tb.claveTreballador, tr.enActiu, tr.enTabla, tr.ordre, tr.preu, es.numExpedient,es.nomExpedient, es.idEsquema, tr.enTop FROM esquemes es INNER JOIN (pressupostos pr INNER JOIN (treballadors tb INNER JOIN (tipostreball tt INNER JOIN treballs tr ON tt.idTipoTreball=tr.idTipoTreball) ON tb.idTreballador = tr.idTreballador) ON pr.idPressupost = tr.idPressupost) ON es.idEsquema = pr.idEsquema WHERE tr.enTabla=%s ORDER BY tr.idTreballador, tr.ordre',(1,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        idTreball=i[0]
        capMax=capsulaMaxTreball(cursor, idTreball)
        cap=capsulaTreball(cursor, idTreball)
            
        lista[indice] = TreballOrdre(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],capMax,cap) #Modificar si anyadim columna 
        indice=indice+1   

    return lista 

def tablaTreballTablaTreballador(cursor, idTreballador):   
     
    cursor.execute('SELECT tr.idTreball, tr.idTipoTreball, tt.treball, tr.idTreballador, tb.claveTreballador, tr.enActiu, tr.enTabla, tr.ordre, tr.preu, es.numExpedient,es.nomExpedient, es.idEsquema, tr.enTop FROM esquemes es INNER JOIN (pressupostos pr INNER JOIN (treballadors tb INNER JOIN (tipostreball tt INNER JOIN treballs tr ON tt.idTipoTreball=tr.idTipoTreball) ON tb.idTreballador = tr.idTreballador) ON pr.idPressupost = tr.idPressupost) ON es.idEsquema = pr.idEsquema WHERE tr.enTabla=%s AND tr.idTreballador=%s ORDER BY tr.ordre',(1, idTreballador))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        idTreball=i[0]
        capMax=capsulaMaxTreball(cursor, idTreball)
        cap=capsulaTreball(cursor, idTreball)
            
        lista[indice] = TreballOrdre(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],capMax,cap) #Modificar si anyadim columna 
        indice=indice+1   
    
    renumerar(cursor, idTreballador)

    return lista 

def tablaTreballLiniaTemps(cursor, idTreballador):   
     
    cursor.execute('SELECT tr.idTreball, tr.idTipoTreball, tt.treball, tr.idTreballador, tb.claveTreballador, tr.enActiu, tr.enTabla, tr.ordre, tr.preu, es.numExpedient,es.nomExpedient, es.idEsquema, tr.enTop FROM esquemes es INNER JOIN (pressupostos pr INNER JOIN (treballadors tb INNER JOIN (tipostreball tt INNER JOIN treballs tr ON tt.idTipoTreball=tr.idTipoTreball) ON tb.idTreballador = tr.idTreballador) ON pr.idPressupost = tr.idPressupost) ON es.idEsquema = pr.idEsquema WHERE tr.enTabla=%s AND tr.idTreballador=%s AND tr.enActiu=%s ORDER BY tr.ordre LIMIT 0,10',(1, idTreballador, 1))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        idTreball=i[0]
        capMax=capsulaMaxTreball(cursor, idTreball)
        cap=capsulaTreball(cursor, idTreball)
            
        lista[indice] = TreballOrdre(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],capMax,cap) #Modificar si anyadim columna 
        indice=indice+1   
    
    return lista 

def tablaTreballLiniaTempsTop(cursor, idTreballador):   
     
    cursor.execute('SELECT tr.idTreball, tr.idTipoTreball, tt.treball, tr.idTreballador, tb.claveTreballador, tr.enActiu, tr.enTabla, tr.ordre, tr.preu, es.numExpedient,es.nomExpedient, es.idEsquema, tr.enTop FROM esquemes es INNER JOIN (pressupostos pr INNER JOIN (treballadors tb INNER JOIN (tipostreball tt INNER JOIN treballs tr ON tt.idTipoTreball=tr.idTipoTreball) ON tb.idTreballador = tr.idTreballador) ON pr.idPressupost = tr.idPressupost) ON es.idEsquema = pr.idEsquema WHERE tr.enTabla=%s AND tr.idTreballador=%s AND tr.enTop=%s AND tr.ordre>%s AND tr.enActiu=%s ORDER BY tr.ordre DESC',(1, idTreballador,1,3,1))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        idTreball=i[0]
        capMax=capsulaMaxTreball(cursor, idTreball)
        cap=capsulaTreball(cursor, idTreball)
            
        lista[indice] = TreballOrdre(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],capMax,cap) #Modificar si anyadim columna 
        indice=indice+1   
    
    return lista 


def tablaTreballSelectOrdre(cursor, idTreball):
     
    cursor.execute('SELECT tr.idTreball, tt.treball, tr.idTreballador, tr.enActiu, tr.enTabla, tr.ordre, tr.preu, tr.enTop FROM tipostreball tt INNER JOIN treballs tr ON tt.idTipoTreball=tr.idTipoTreball WHERE tr.idTreball=%s',(idTreball,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista = TreballOrdreS(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]) #Modificar si anyadim columna 
    return lista 

class TreballOrdreS:
    def __init__(self, idTreball, treball, idTreballador,enActiu,enTabla,ordre,preu,enTop):
        self.idTreball = idTreball
        self.treball = treball
        self.idTreballador = idTreballador
        self.enActiu = enActiu
        self.enTabla = enTabla
        self.ordre = ordre
        self.preu = preu
        self.enTop = enTop

def ordre(cursor, idTreballador, idTreball, ordre):
    #eliminem de la tabla la fila que modifiquem
    cursor.execute('UPDATE treballs SET enTabla=%s WHERE idTreball=%s', (0, idTreball,))
    
    cursor.execute('SELECT ordre FROM treballs WHERE idTreball=%s',(idTreball,))
    vector = cursor.fetchall()
    ordreIniS=int(vector[0][0])
    ordreObj = int(ordre)
    #tabla de elements excepte el modificat         
    cursor.execute('SELECT idTreball, ordre FROM treballs WHERE idTreballador=%s AND enTabla=%s ORDER BY ordre',(idTreballador,1))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        ordreIni=int(i[1])
        idTreballIni=i[0]
        
        if ordreIniS >= ordreObj: #ascenso
            if ordreIni >= ordreObj:
                ordreFin = ordreIni+1
            else:
                ordreFin = ordreIni
        else: #descenso
            if ordreIni>ordreObj:
                ordreFin = ordreIni+1
            else:
                ordreFin=ordreIni-1
  
        cursor.execute('UPDATE treballs SET ordre=%s WHERE idTreball=%s', (ordreFin, idTreballIni,))
    
    #insertem la fila modificada
    cursor.execute('UPDATE treballs SET ordre=%s, enTabla=%s WHERE idTreball=%s', (ordre, 1, idTreball,))
    renumerar(cursor,idTreballador)

def renumerar(cursor, idTreballador):
    cursor.execute('SELECT idTreball FROM treballs WHERE idTreballador=%s AND enTabla=%s ORDER BY ordre',(idTreballador,1,))
    tabla = cursor.fetchall()
    ordre=1
    for i in tabla: #cada fila es converteix en un objecte de lista
        idTreballIni=i[0]
        cursor.execute('UPDATE treballs SET ordre=%s WHERE idTreball=%s', (ordre, idTreballIni,))
        ordre=ordre+1

            
 
    
###########################################################################################################################################################
# TIPOS TREBALL        TIPOS TREBALL        TIPOS TREBALL         TIPOS TREBALL         TIPOS TREBALL         TIPOS TREBALL         TIPOS TREBALL            
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariTipoTreball (usuari, idTipoTreball, idEsquema, idPressupost):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    
    if idTipoTreball == -1: 
        tipoTreballSelect = ''
        tipoTreballTots = ''  
    elif idTipoTreball == -2: 
        tipoTreballSelect = ''
        tipoTreballTots = tablaTipoTreballTots(cursor)   
    else: 
        tipoTreballSelect = tablaTipoTreballSelect(cursor,idTipoTreball)
        tipoTreballTots = ''
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'idTipoTreball': idTipoTreball,
             'idEsquema': idEsquema,
             'idPressupost': idPressupost,
             'tipoTreballSelect': tipoTreballSelect,
             'tipoTreballTots': tipoTreballTots,          
              }
    return values   

# ACCIONS DEL FORMULARI
####################################

class TipoTreballNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1): 
                #parametres
                idTipoTreball = -1
                idEsquema = novar(self.request.get('idEsquema'))
                idPressupost = novar(self.request.get('idPressupost'))
            
                #obtenim valors per al html
                values = formulariTipoTreball(usuari, idTipoTreball, idEsquema, idPressupost)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'tipotreball.html') 
                self.response.out.write(template.render(path, values,))

class TipoTreballTots (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1): 
                #parametres
                idTipoTreball = -2
                idEsquema = novar(self.request.get('idEsquema'))
                idPressupost = novar(self.request.get('idPressupost'))
            
                #obtenim valors per al html
                values = formulariTipoTreball(usuari, idTipoTreball, idEsquema, idPressupost)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'tipotreball.html') 
                self.response.out.write(template.render(path, values,))
                
            
class TipoTreballSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
                #parametres
                idTipoTreball = novar(self.request.get('idTipoTreball'))
                idEsquema = novar(self.request.get('idEsquema'))
                idPressupost = novar(self.request.get('idPressupost'))
            
                #obtenim valors per al html
                values = formulariTipoTreball(usuari, idTipoTreball, idEsquema, idPressupost)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'tipotreball.html') 
                self.response.out.write(template.render(path, values,))
            
class TipoTreballEdita (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTipoTreball= novar(self.request.get('idTipoTreball'))
            idEsquema= novar(self.request.get('idEsquema'))
            idPressupost = novar(self.request.get('idPressupost'))
            claveTreball = novar(self.request.get('claveTreball'))
            treball = novar(self.request.get('treball'))
            enActiu = novar(self.request.get('enActiu'))
          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
                       
            cursor.execute('UPDATE tipostreball SET  claveTreball=%s, treball=%s, enActiu=%s WHERE idTipoTreball=%s', (claveTreball, treball, enActiu, idTipoTreball,))
            
            db.commit()
            db.close()
            
            
            idTipoTreball=-2
            
            #obtenim valors per al html
            values = formulariTipoTreball(usuari, idTipoTreball, idEsquema, idPressupost)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'tipotreball.html') 
            self.response.out.write(template.render(path, values,))

class TipoTreballCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idEsquema= novar(self.request.get('idEsquema'))
            idPressupost = novar(self.request.get('idPressupost'))
            claveTreball = novar(self.request.get('claveTreball'))
            treball = novar(self.request.get('treball'))
            enActiu = novar(self.request.get('enActiu'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('INSERT INTO tipostreball (claveTreball, treball, enActiu) VALUES (%s, %s, %s)', (claveTreball, treball, enActiu,))
            
            db.commit()
            db.close()

            #parametres
            idTipoTreball = -2
            
            #obtenim valors per al html
            values = formulariTipoTreball(usuari, idTipoTreball, idEsquema, idPressupost)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'tipotreball.html') 
            self.response.out.write(template.render(path, values,))


# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaTipoTreballTots(cursor):   
    cursor.execute('SELECT idTipoTreball, claveTreball, treball, enActiu FROM tipostreball ORDER BY enActiu DESC, claveTreball')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = TipoTreball(i[0],i[1],i[2],i[3]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

def tablaTipoTreballAct(cursor):   
    cursor.execute('SELECT idTipoTreball, claveTreball, treball, enActiu FROM tipostreball WHERE enActiu=%s ORDER BY claveTreball',(1,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = TipoTreball(i[0],i[1],i[2],i[3]) #Modificar si anyadim columna 
        indice=indice+1    
    return lista 

def tablaTipoTreballSelect(cursor, idTipoTreball):
    cursor.execute('SELECT idTipoTreball, claveTreball, treball, enActiu FROM tipostreball WHERE idTipoTreball=%s',(idTipoTreball,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista = TipoTreball(i[0],i[1],i[2],i[3]) #Modificar si anyadim columna 
    return lista 


class TipoTreball: 
    def __init__(self, idTipoTreball=0, claveTreball='', treball='', enActiu=0):
        self.idTipoTreball = idTipoTreball
        self.claveTreball= claveTreball
        self.treball = treball
        self.enActiu = enActiu  
   
   
###########################################################################################################################################################
# CALENDARI              CALENDARI                CALENDARI                CALENDARI                 CALENDARI                 CALENDARI          
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariCalendari (usuari, idTreballador, idUbicacio):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    treballadorTots=tablaTreballadorTots(cursor)
    treballadorAct=tablaTreballadorAct(cursor)
    intermediariTots=tablaIntermediariTots(cursor)
    ubicacioTots=tablaUbicacioTots(cursor)
      
    tareaPassat= tablaTareaPassat(cursor, idTreballador, idUbicacio)
    tareaHui= tablaTareaHui(cursor, idTreballador, idUbicacio)
    tareaDema= tablaTareaDema(cursor, idTreballador, idUbicacio)
    tareaFutur= tablaTareaFutur(cursor, idTreballador, idUbicacio)
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'treballadorTots': treballadorTots,
             'treballadorAct': treballadorAct,
             'intermediariTots': intermediariTots,
             'tareaPassat': tareaPassat,
             'tareaHui': tareaHui,
             'tareaDema': tareaDema,
             'tareaFutur': tareaFutur, 
             'ubicacioTots': ubicacioTots,
             'idTreballador': idTreballador,        
              }
    return values   

# ACCIONS DEL FORMULARI
####################################

class CalendariInicial (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1): 
                #parametres
                idUbicacio = -1
                
                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
                cursor.execute('SELECT idTreballador FROM treballadors WHERE enActiu=%s',(1,))
                tabla = cursor.fetchall()
                conta=0
                indice=0
                for i in tabla: #conta el numero de files de la tabla
                    conta=conta+1
                lista=[0]*conta #creem lista
                for i in tabla: #cada fila es converteix en un objecte de lista
                    lista[indice] = i[0] #Modificar si anyadim columna
                    indice=indice+1   
                #desconectar de la bd
                db.commit()
                db.close()
                
                j=0
                idTreballador=-1
                
                while(j!=len(lista) and idTreballador==-1):                        
                    if(lista[j]==usuari):
                        idTreballador=usuari
                    j+=1
                
                
                    
                        

            
                #obtenim valors per al html
                values = formulariCalendari(usuari, idTreballador, idUbicacio)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'calendari.html') 
                self.response.out.write(template.render(path, values,))

class CalendariFiltro (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1): 
                #parametres
                idUbicacio= novar(self.request.get('idUbicacio'))
                idTreballador = novar(self.request.get('idTreballador'))
                            
                #obtenim valors per al html
                values = formulariCalendari(usuari, idTreballador, idUbicacio)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'calendari.html') 
                self.response.out.write(template.render(path, values,))

                
#--PASSA TAREA A DEMA
class TareaDema (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):       
                #parametres
                idTarea= novar(self.request.get('idTarea'))
                idTreballador= novar(self.request.get('idTreballador'))
                idUbicacio= -1
   
                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
                
                #obtenir data tarea seleccionada
                cursor.execute('SELECT dataTarea FROM tareas WHERE idTarea=%s', (idTarea,))
                dataTarea = cursor.fetchall()
                dataTarea = dataTarea [0][0]
        
                #obtenir dema
                aradema = datetime.datetime.today() + datetime.timedelta(days=1)
                dema = aradema.strftime('%Y-%m-%d')
                
                #edita fila en tabla
                cursor.execute('UPDATE tareas SET dataTarea=%s WHERE idTarea=%s', (dema, idTarea,))
                
                #desconectar de la bd
                db.commit()
                db.close()
                         
                #obtenim valors per al html
                values = formulariCalendari(usuari, idTreballador, idUbicacio)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'calendari.html') 
                self.response.out.write(template.render(path, values,))

#--PASSA TAREA A DEMA
class TareaDemaTarea (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):       
                #parametres
                idTarea= novar(self.request.get('idTarea'))
                idEsquema= novar(self.request.get('idEsquema'))
   
                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
                
                #obtenir data tarea seleccionada
                cursor.execute('SELECT dataTarea FROM tareas WHERE idTarea=%s', (idTarea,))
                dataTarea = cursor.fetchall()
                dataTarea = dataTarea [0][0]
        
                #obtenir dema
                aradema = datetime.datetime.today() + datetime.timedelta(days=1)
                dema = aradema.strftime('%Y-%m-%d')
                
                #edita fila en tabla
                cursor.execute('UPDATE tareas SET dataTarea=%s WHERE idTarea=%s', (dema, idTarea,))
                
                #desconectar de la bd
                db.commit()
                db.close()
                         
                #parametres
                idGrafica = 2
                
                
                #obtenim valors per al html
                values = formulariTarea(usuari, idEsquema, idTarea, idGrafica)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'tarea.html') 
                self.response.out.write(template.render(path, values,))

#--PASSA TAREA A HUI
class TareaHui (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):       
                #parametres
                idTarea= novar(self.request.get('idTarea'))
                idTreballador= novar(self.request.get('idTreballador'))
                idUbicacio= -1
   
                #conectar a la bd
                db= get_db()
                cursor = db.cursor()

                #obtenir hui
                ara = datetime.datetime.today()
                hui = ara.strftime('%Y-%m-%d')
                
                #edita fila en tabla
                cursor.execute('UPDATE tareas SET dataTarea=%s WHERE idTarea=%s', (hui, idTarea,))
        
                #desconectar de la bd
                db.commit()
                db.close()
        
                #obtenim valors per al html
                values = formulariCalendari(usuari, idTreballador, idUbicacio)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'calendari.html') 
                self.response.out.write(template.render(path, values,))
        
#--PASSA TAREA A DILLUNS
class TareaDilluns (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):       
                #parametres
                idTarea= novar(self.request.get('idTarea'))
                idTreballador= novar(self.request.get('idTreballador'))
                idUbicacio= -1
   
                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
        
                #obtenir data tarea seleccionada
                cursor.execute('SELECT dataTarea FROM tareas WHERE idTarea=%s', (idTarea,))
                dataTarea = cursor.fetchall()
                dataTarea = dataTarea [0][0]

                #obtenir 
                ara = datetime.datetime.today()
                
                dilluns = proxDia(ara, 0) # 0 = Monday, 1=Tuesday, 2=Wednesday...
                
                dilluns = dilluns.strftime('%Y-%m-%d')
                
                #edita fila en tabla
                cursor.execute('UPDATE tareas SET dataTarea=%s WHERE idTarea=%s', (dilluns, idTarea,))
        
                #desconectar de la bd
                db.commit()
                db.close()
        
                #obtenim valors per al html
                values = formulariCalendari(usuari, idTreballador, idUbicacio)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'calendari.html') 
                self.response.out.write(template.render(path, values,))
            



# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaTareaPassat(cursor, idTreballador, idUbicacio):
    #dataHui
    ara = datetime.datetime.today()
    hui = ara.strftime('%Y-%m-%d')
    idUbicacio=int(idUbicacio)
    idTreballador=int(idTreballador)
  
    if idUbicacio == -1:
        if idTreballador == -1:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea<%s AND ta.ok=%s AND ta.cancel=%s AND ta.dataTarea>%s ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (hui,0,0,'1900-01-01',))
        else:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea<%s AND ta.ok=%s AND ta.cancel=%s AND ta.dataTarea>%s AND ta.idTreballador=%s ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (hui,0,0,'1900-01-01', idTreballador,))
    else:
        if idTreballador == -1:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea<%s AND ta.ok=%s AND ta.cancel=%s AND ta.dataTarea>%s AND es.idUbicacio=%s ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (hui,0,0,'1900-01-01', idUbicacio,))
        else:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea<%s AND ta.ok=%s AND ta.cancel=%s AND ta.dataTarea>%s AND es.idUbicacio=%s AND ta.idTreballador=%s ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (hui,0,0,'1900-01-01', idUbicacio, idTreballador,))

    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        tel=telFormat(i[7])
        lista[indice] = TareaCalendari(i[0],i[1],i[2],i[3],i[4],i[5],i[6],tel,i[8],i[9],i[10]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista

def tablaTareaHui(cursor, idTreballador, idUbicacio):
    #dataHui
    ara = datetime.datetime.today()
    hui = ara.strftime('%Y-%m-%d')
    idUbicacio=int(idUbicacio)
    idTreballador=int(idTreballador)
  
    if idUbicacio == -1:
        if idTreballador == -1:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea=%s AND ta.ok=%s AND ta.cancel=%s  ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (hui,0,0,))
        else:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea=%s AND ta.ok=%s AND ta.cancel=%s AND ta.idTreballador=%s ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (hui,0,0, idTreballador,))
    else:
        if idTreballador == -1:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea=%s AND ta.ok=%s AND ta.cancel=%s AND es.idUbicacio=%s ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (hui,0,0, idUbicacio,))
        else:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea=%s AND ta.ok=%s AND ta.cancel=%s AND es.idUbicacio=%s AND ta.idTreballador=%s ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (hui,0,0, idUbicacio, idTreballador,))

    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        tel=telFormat(i[7])
        lista[indice] = TareaCalendari(i[0],i[1],i[2],i[3],i[4],i[5],i[6],tel,i[8],i[9],i[10]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

def tablaTareaDema(cursor, idTreballador, idUbicacio):
    #dataHui
    ara = datetime.datetime.today()
    aradema = ara + datetime.timedelta(days=1)
    dema = aradema.strftime('%Y-%m-%d')
    idUbicacio=int(idUbicacio)
    idTreballador=int(idTreballador)
    
    if idUbicacio == -1:
        if idTreballador == -1:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea=%s AND ta.ok=%s AND ta.cancel=%s  ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (dema,0,0,))
        else:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea=%s AND ta.ok=%s AND ta.cancel=%s AND ta.idTreballador=%s ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (dema,0,0, idTreballador,))
    else:
        if idTreballador == -1:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea=%s AND ta.ok=%s AND ta.cancel=%s AND es.idUbicacio=%s ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (dema,0,0, idUbicacio,))
        else:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea=%s AND ta.ok=%s AND ta.cancel=%s AND es.idUbicacio=%s AND ta.idTreballador=%s ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (dema,0,0, idUbicacio, idTreballador,))

    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        tel=telFormat(i[7])
        lista[indice] = TareaCalendari(i[0],i[1],i[2],i[3],i[4],i[5],i[6],tel,i[8],i[9],i[10]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

def tablaTareaFutur(cursor, idTreballador, idUbicacio):
    #dataHui
    ara = datetime.datetime.today()
    aradema = ara + datetime.timedelta(days=1)
    dema = aradema.strftime('%Y-%m-%d')
    idUbicacio=int(idUbicacio)
    idTreballador=int(idTreballador)
  
    if idUbicacio == -1:
        if idTreballador == -1:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea>%s AND ta.ok=%s AND ta.cancel=%s  ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (dema,0,0,))
        else:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea>%s AND ta.ok=%s AND ta.cancel=%s  AND ta.idTreballador=%s ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (dema,0,0, idTreballador,))
    else:
        if idTreballador == -1:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea>%s AND ta.ok=%s AND ta.cancel=%s  AND es.idUbicacio=%s ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (dema,0,0, idUbicacio,))
        else:
            cursor.execute('SELECT ta.idTarea, ta.idTreballador, es.idEsquema, es.idUbicacio, es.idIntermediari, es.nomExpedient, es.numExpedient, es.telClientPos, ta.comentari, ta.marca, es.idTreballador FROM clients cl INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost INNER JOIN tareas ta ON tr.idTreball = ta.idTreball) ON es.idClient = cl.idClient  WHERE ta.dataTarea>%s AND ta.ok=%s AND ta.cancel=%s  AND es.idUbicacio=%s AND ta.idTreballador=%s ORDER BY es.idUbicacio, ta.idTreballador, ta.idTarea', (dema,0,0, idUbicacio, idTreballador,))

    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        tel=telFormat(i[7])
        lista[indice] = TareaCalendari(i[0],i[1],i[2],i[3],i[4],i[5],i[6],tel,i[8],i[9],i[10]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista

class TareaCalendari: 
    def __init__(self, idTarea=0, idTreballador=0, idEsquema=0, idUbicacio=0, idIntermediari=0, nomExpedient='', numExpedient='', telClientPos='', comentari='', marca=0, idCoordinador=0):
        self.idTarea = idTarea
        self.idTreballador= idTreballador
        self.idEsquema = idEsquema
        self.idUbicacio = idUbicacio
        self.idIntermediari = idIntermediari
        self.nomExpedient = nomExpedient
        self.numExpedient = numExpedient
        self.telClientPos = telClientPos
        self.comentari = comentari
        self.marca = marca
        self.idCoordinador=idCoordinador
        

###########################################################################################################################################################
# PROFORMA              PROFORMA              PROFORMA               PROFORMA               PROFORMA               PROFORMA           
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariProforma (usuari, idFactura, idEsquema):

    #dataHui
    ara = datetime.datetime.today()
    dataHui = ara.strftime('%Y-%m-%d')
    
    idFactura=int(idFactura)

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    treballAcceptatEsquema= tablaTreballAcceptatEsquema(cursor, idEsquema)
    tipoTreballTots = tablaTipoTreballTots(cursor)
    clientTots = tablaClientTots(cursor)
    ubicacioTots = tablaUbicacioTots(cursor)
    cursor.execute('SELECT factura FROM factures ORDER BY factura DESC LIMIT 0,1')
    lista = cursor.fetchall()
    ultFact = lista[0][0]
    
    if idFactura == -1: #nou
        #num proforma ultim
        cursor.execute('SELECT proforma FROM factures ORDER BY proforma DESC LIMIT 0,1')
        lista = cursor.fetchall()
        proforma = lista[0][0]
        proforma = proformaSeguent(proforma)

        cursor.execute('SELECT idClient FROM esquemes WHERE idEsquema=%s',(idEsquema,))
        lista = cursor.fetchall()
        idClient = lista[0][0]
        
        proformaSelect = Proforma(idFactura,idEsquema,idClient,proforma,dataHui,'','','','','','','','','','','','')
        treballProforma = ''
        treballsLF = ''
        treballsLFF = ''
        treballsLSF = ''

        
    else: # select
        proformaSelect = tablaProformaSelect(cursor,idFactura)
        treballProforma = tablaTreballProforma(cursor, idFactura)
        treballsLF = tablaTreballsLF(cursor, idFactura)
        treballsLFF = tablaTreballsLFF(cursor, idFactura)
        treballsLSF = tablaTreballsLSF(cursor, idFactura)
        



    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'idFactura': idFactura,
             'idEsquema': idEsquema,
             'treballAcceptatEsquema': treballAcceptatEsquema,
             'tipoTreballTots': tipoTreballTots, 
             'proformaSelect': proformaSelect, 
             'treballProforma': treballProforma,
             'clientTots': clientTots,
             'ultFact': ultFact,
             'treballsLF': treballsLF,
             'treballsLFF': treballsLFF,
             'treballsLSF': treballsLSF,
             'ubicacioTots': ubicacioTots,

              }
    return values  

# ACCIONS DEL FORMULARI
####################################

                
class ProformaNou (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idEsquema = novar(self.request.get('idEsquema'))
                idFactura = -1
            
                #obtenim valors per al html
                values = formulariProforma(usuari, idFactura, idEsquema)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'proforma.html') 
                self.response.out.write(template.render(path, values,))
                
class ProformaCreaPercent (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idEsquema = novar(self.request.get('idEsquema'))
                idPressupost = novar(self.request.get('idPressupost'))
                numPressupost = novar(self.request.get('numPressupost'))
                percentU= novar(self.request.get('percent'))
                percent = float(percentU)
                percentT=str(int(percent*100,))
                

                #dataHui
                ara = datetime.datetime.today()
                dataHui = ara.strftime('%Y-%m-%d')
                dataProforma=dataHui
                
            
                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
                    
                #operar en bd 

                #num proforma ultim
                cursor.execute('SELECT proforma FROM factures ORDER BY proforma DESC LIMIT 0,1')
                lista = cursor.fetchall()
                proforma = lista[0][0]
                proforma = proformaSeguent(proforma)
            
                cursor.execute('SELECT idClient FROM esquemes WHERE idEsquema=%s',(idEsquema,))
                lista = cursor.fetchall()
                idClient = lista[0][0]
                
                factura = ""
                dataFactura = ""
                titolFactura = "Honorarios correspondientes al "+percentT+"% del presupuesto: "+numPressupost
                enPis = 1
                idUbicacio = 3
                
                #inserta fila en factures
                cursor.execute('INSERT INTO factures (idEsquema, idClient, proforma, dataProforma, factura, dataFactura, titolFactura, idUbicacio, enPis) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (idEsquema, idClient, proforma, dataProforma, factura, dataFactura, titolFactura, idUbicacio, enPis,))
                #obtenir el idFactura de la fila que hem insertat
                cursor.execute('SELECT idFactura FROM factures ORDER BY idFactura DESC LIMIT 0,1')
                vector = cursor.fetchall()
                idFactura=vector[0][0]
                
                idTipoTreball = 33
                acceptat = 0
                
                cursor.execute('SELECT SUM(preu) AS preuT FROM treballs WHERE idPressupost=%s AND acceptat =%s GROUP BY idPressupost',(idPressupost, 1,))
                tabla = cursor.fetchall()
                totalPressup = tabla[0][0]
                totalP = float(totalPressup)
                
                preu = percent*totalP
                
                cursor.execute('INSERT INTO treballs (idTipoTreball, idPressupost, preu, acceptat) VALUES (%s, %s, %s, %s)', (idTipoTreball, idPressupost, preu, acceptat,))
                
                cursor.execute('SELECT idTreball FROM treballs ORDER BY idTreball DESC LIMIT 0,1')
                vector = cursor.fetchall()
                idTreball=vector[0][0]
                
                cursor.execute('INSERT INTO liniesfactura (idFactura, idTreball) VALUES (%s,%s)',(idFactura, idTreball,))
                
                
                #desconectar de la bd
                db.commit()
                db.close()
            
                #obtenim valors per al html
                values = formulariProforma(usuari, idFactura, idEsquema)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'proforma.html') 
                self.response.out.write(template.render(path, values,))

                
            
class ProformaSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idFactura= novar(self.request.get('idFactura'))

            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('SELECT idEsquema FROM factures WHERE idFactura=%s', (idFactura,))
            vector = cursor.fetchall()
            idEsquema=vector[0][0]
            db.commit()
            db.close()

            #obtenim valors per al html
            values = formulariProforma(usuari, idFactura, idEsquema)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'proforma.html') 
            self.response.out.write(template.render(path, values,))

            

class ProformaEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idFactura= novar(self.request.get('idFactura'))
            idEsquema= novar(self.request.get('idEsquema'))
            idClient = novar(self.request.get('idClient'))
            proforma = novar(self.request.get('proforma'))
            dataProforma = novar(self.request.get('dataProforma'))
            factura = novar(self.request.get('factura'))
            dataFactura = novar(self.request.get('dataFactura'))
            titolFactura = novar(self.request.get('titolFactura'))
            idUbicacio = novar(self.request.get('idUbicacio'))
            enPis = novar(self.request.get('enPis'))
            dataCobro = novar(self.request.get('dataCobro'))
            
            #dataHui
            ara = datetime.datetime.today()
            hui = ara.strftime('%Y-%m-%d')

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('UPDATE factures SET idClient=%s, proforma=%s, dataProforma=%s, factura=%s, dataFactura=%s, titolFactura=%s, idUbicacio=%s, enPis=%s, dataCobro=%s WHERE idFactura=%s', (idClient, proforma, dataProforma, factura, dataFactura, titolFactura, idUbicacio, enPis, dataCobro, idFactura,))          
            
            cursor.execute('SELECT SUM(quantitat) AS q FROM moviments GROUP BY idFactura HAVING idFactura=%s',(idFactura,))
            vector = cursor.fetchall()
            try:
                cobrat = vector [0] [0]
            except:
                cobrat = 0
                
            cursor.execute('SELECT SUM(tr.preu) AS preuLF FROM treballs tr INNER JOIN liniesfactura lf ON tr.idTreball=lf.idTreball GROUP BY lf.idFactura HAVING lf.idFactura=%s',(idFactura,))
            tSumPreuLF = cursor.fetchall()
            try:
                tProforma = tSumPreuLF[0][0]
            except:
                tProforma = 0
                
            if cobrat <> 0 and cobrat >= tProforma:
                dataCobro = hui
                cursor.execute('UPDATE factures SET dataCobro=%s WHERE idFactura=%s', (dataCobro, idFactura,))               
              
            db.commit()
            db.close()

            #obtenim valors per al html
            values = formulariProforma(usuari, idFactura, idEsquema)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'proforma.html') 
            self.response.out.write(template.render(path, values,))

class ProformaCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idClient  = novar(self.request.get('idClient'))
            titolFactura  = novar(self.request.get('titolFactura'))
            proforma  = novar(self.request.get('proforma'))
            dataProforma  = novar(self.request.get('dataProforma'))
            factura  = novar(self.request.get('factura'))
            dataFactura  = novar(self.request.get('dataFactura'))
            idEsquema =  novar(self.request.get('idEsquema'))
            idUbicacio =  novar(self.request.get('idUbicacio'))
            enPis =  novar(self.request.get('enPis'))

            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            #comprova que la proforma no existeix ja
            cursor.execute('SELECT proforma FROM factures WHERE proforma=%s',(proforma,))
            proformaE = cursor.fetchall()
            if proformaE: #si proforma ja existia
                self.response.out.write('el numero de proforma ja existeix, has fet dos clicks massa rapid i anaves a duplicar proforma')
                
                db.commit()
                db.close()
            else:
                #inserta fila en factures
                cursor.execute('INSERT INTO factures (idEsquema, idClient, proforma, dataProforma, factura, dataFactura, titolFactura, idUbicacio, enPis) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (idEsquema, idClient, proforma, dataProforma, factura, dataFactura, titolFactura, idUbicacio, enPis,))
                #obtenir el idFactura de la fila que hem insertat
                cursor.execute('SELECT idFactura FROM factures ORDER BY idFactura DESC LIMIT 0,1')
                vector = cursor.fetchall()
                idFactura=vector[0][0]
                          
                db.commit()
                db.close()

                #obtenim valors per al html
                values = formulariProforma(usuari, idFactura, idEsquema)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'proforma.html') 
                self.response.out.write(template.render(path, values,))

class ProformaElimina (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idFactura = novar(self.request.get('idFactura'))
                idEsquema = novar(self.request.get('idEsquema'))

                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
                
                cursor.execute('DELETE FROM factures WHERE idFactura=%s',(idFactura,))

                db.commit()
                db.close()

                #parametres
                idTarea=-1
                idHistoria = -1
    
                #obtenim valors per al html
                values = esquema(usuari, idEsquema, idTarea, idHistoria)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
                self.response.out.write(template.render(path, values,))


# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaProformaEsq(cursor, idEsquema):   
    cursor.execute('SELECT idFactura, idEsquema, idClient, proforma, dataProforma, factura, dataFactura, dataCobro, eurComis, facComisSol, comisPagada, titolFactura, factEntregada, sobre, incobrable, idUbicacio, enPis FROM factures WHERE idEsquema=%s ORDER BY idFactura',(idEsquema,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
            dataProforma=dataFormat(i[4])
            dataFactura=dataFormat(i[6])
            dataCobro=dataFormat(i[7])
            idClient = int(i[2])
            cursor.execute('SELECT nomClient FROM clients WHERE idClient=%s', (idClient,))
            vector = cursor.fetchall()
            nomClient = vector[0][0]
            
            idFactura2=i[0]
            #obtenir total linies factura
            cursor.execute('SELECT SUM(tr.preu) AS preuLF FROM treballs tr INNER JOIN liniesfactura lf ON tr.idTreball=lf.idTreball GROUP BY lf.idFactura HAVING lf.idFactura=%s',(idFactura2,))
            tSumPreuLF = cursor.fetchall()
            try:
                tProforma = tSumPreuLF[0][0]
            except:
                tProforma = 0
            
            #obtenir total linies suplidos
            cursor.execute('SELECT SUM(preuSuplido) AS preuLS FROM liniessuplidos GROUP BY idFactura HAVING idFactura=%s',(idFactura2,))
            tSumPreuLS = cursor.fetchall()
            try:
                tSuplido = tSumPreuLS[0] [0]
            except:
                tSuplido = 0
                
            #obtenir iva
            cursor.execute('SELECT factura FROM factures WHERE idFactura=%s',(idFactura2,))
            vector = cursor.fetchall()
            try:
                factura = vector [0] [0]
            except:
                factura = 0
            
            if factura > 'a':
                cursor.execute('SELECT tipoIVA FROM constants WHERE idConstant=%s',(1,))
                tabla = cursor.fetchall()
                tipoIVA = tabla [0][0]
                try:
                    iva = tProforma*tipoIVA
                except:
                    iva = 0
                
            else:
                iva=0
            
            #cobrat
            cursor.execute('SELECT SUM(quantitat) AS q FROM moviments GROUP BY idFactura HAVING idFactura=%s',(idFactura2,))
            vector = cursor.fetchall()
            try:
                cobrat = vector [0] [0]
            except:
                cobrat = 0
            
            try:
                #total = tProforma+tSuplido+iva
                total = tProforma
            except:
                total=0
                
            cobrat = cobrat-iva-tSuplido
            
            try:
                pendent = total - cobrat
            except:
                pendent =0
                
            try:
                total = "%.2f" %total
            except:
                total=""
            
            if pendent > 0:
                pendent = "%.2f" %pendent
            else:
                pendent = 'pagat'
                
            cobrat = "%.2f" %cobrat
            lista[indice] = Proforma(i[0],i[1],nomClient,i[3],dataProforma,i[5],dataFactura,dataCobro,i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16], total, pendent, cobrat) #Modificar si anyadim columna 
            indice=indice+1   
    return lista 
def tablaProformaEsqTot(cursor, idEsquema):   
    cursor.execute('SELECT idFactura, idEsquema, idClient, proforma, dataProforma, factura, dataFactura, dataCobro, eurComis, facComisSol, comisPagada, titolFactura, factEntregada, sobre, incobrable, idUbicacio, enPis FROM factures WHERE idEsquema=%s ORDER BY idFactura',(idEsquema,))
    tabla = cursor.fetchall()
    conta=0
    totalP = 0
    cobratP = 0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    for i in tabla: #cada fila es converteix en un objecte de lista       
            idFactura2=i[0]
            #obtenir total linies factura
            cursor.execute('SELECT SUM(tr.preu) AS preuLF FROM treballs tr INNER JOIN liniesfactura lf ON tr.idTreball=lf.idTreball GROUP BY lf.idFactura HAVING lf.idFactura=%s',(idFactura2,))
            tSumPreuLF = cursor.fetchall()
            try:
                tProforma = tSumPreuLF[0][0]
            except:
                tProforma = 0
            
            #obtenir total linies suplidos
            cursor.execute('SELECT SUM(preuSuplido) AS preuLS FROM liniessuplidos GROUP BY idFactura HAVING idFactura=%s',(idFactura2,))
            tSumPreuLS = cursor.fetchall()
            try:
                tSuplido = tSumPreuLS[0] [0]
            except:
                tSuplido = 0
                
            #obtenir iva
            cursor.execute('SELECT factura FROM factures WHERE idFactura=%s',(idFactura2,))
            vector = cursor.fetchall()
            try:
                factura = vector [0] [0]
            except:
                factura = 0
            
            if factura > 'a':
                cursor.execute('SELECT tipoIVA FROM constants WHERE idConstant=%s',(1,))
                tabla = cursor.fetchall()
                tipoIVA = tabla [0][0]
                try:
                    iva = tProforma*tipoIVA
                except:
                    iva = 0
                
            else:
                iva=0
            
            #cobrat
            cursor.execute('SELECT SUM(quantitat) AS q FROM moviments GROUP BY idFactura HAVING idFactura=%s',(idFactura2,))
            vector = cursor.fetchall()
            try:
                cobrat = vector [0] [0]
            except:
                cobrat = 0
            
            try:
                #total = tProforma+tSuplido+iva
                total = tProforma
            except:
                total=0
                
            cobrat = cobrat-iva-tSuplido
            
            try:
                totalP = totalP+total
            except:
                totalP=0.0
            cobratP = cobratP + cobrat
    
    pendentP = totalP-cobratP
            
    totalP = "%.2f" %totalP
    if pendentP >0:
        pendentP = "%.2f" %pendentP
    else:
        pendentP = "pagat"
    cobratP = "%.2f" %cobratP
    lista= ProformaT(totalP, cobratP, pendentP) #Modificar si anyadim columna  
    return lista 

class ProformaT:
    def __init__(self, totalP, cobratP, pendentP):
        self.totalP = totalP
        self.cobratP = cobratP
        self.pendentP = pendentP
        
        
def tablaTreballAcceptatEsquema(cursor, idEsquema):   
    cursor.execute('SELECT tr.idTreball, tr.idTipoTreball, tr.idPressupost, tr.dataTreball, tr.preu, tr.acceptat, tr.patras, tr.presentat, tr.comentari, tr.expAj, tr.numVisado FROM esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN  treballs tr ON pr.idPressupost = tr.idPressupost WHERE es.idEsquema=%s AND pr.enActiu=%s AND tr.acceptat=%s ORDER BY pr.idPressupost LIMIT 1,200', (idEsquema,1,1,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        cursor.execute('SELECT claveTreball FROM tipostreball WHERE idTipoTreball=%s', (i[1],))
        vector = cursor.fetchall()
        claveTreball= vector[0][0]
        cursor.execute('SELECT numPressupost FROM pressupostos WHERE idPressupost=%s', (i[2],))
        vector = cursor.fetchall()
        numPressupost= vector[0][0]
        lista[indice] = TreballProforma(i[0],claveTreball,numPressupost, i[4]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 




def tablaProformaSelect(cursor, idFactura):
    
    #si no se ha passat idFactura prepara per a nou, amb data hui i num prof seguent
    if idFactura > 0:
        cursor.execute('SELECT idFactura, idEsquema, idClient, proforma, dataProforma, factura, dataFactura, dataCobro, eurComis, facComisSol, comisPagada, titolFactura, factEntregada, sobre, incobrable, idUbicacio, enPis FROM factures WHERE idFactura=%s',(idFactura,))
        facturaSelect = cursor.fetchall()

        for i in facturaSelect: #cada fila es converteix en un objecte de lista
            dataP=dataFormat(i[4])
            dataF=dataFormat(i[6])
            dataC=dataFormat(i[7])
            proformaSelect = Proforma(i[0],i[1],i[2],i[3],dataP,i[5],dataF,dataC,i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16]) #Modificar si anyadim columna
    else:
        #dataHui
        ara = datetime.datetime.today()
        hui = ara.strftime('%Y-%m-%d')
        #ultima proforma
        cursor.execute('SELECT proforma FROM factures ORDER BY proforma DESC LIMIT 0,1')
        proforma = cursor.fetchall()
        proforma = proforma[0][0]
        #proforma seguent
        proforma = proformaSeguent(proforma)
        idFactura=-1
        #preparat per a proforma nova
        proformaSelect = Proforma(idFactura,'','',proforma,hui,'','','','','','','',3,'','','','')
    
    return proformaSelect



def tablaTreballsLF(cursor,idFactura):
    #obtenir idEsquema de la factura
    cursor.execute('SELECT idEsquema FROM factures WHERE idFactura=%s',(idFactura,))
    idEsquema = cursor.fetchall()
    #obtenir tots els treballs acceptats i no patras del esquema
    cursor.execute('SELECT tr.idTreball, tt.treball, pr.numPressupost, tr.preu FROM tipostreball tt INNER JOIN (esquemes es INNER JOIN (pressupostos pr INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost) ON pr.idEsquema = es.idEsquema)ON tt.idTipoTreball = tr.idTipoTreball WHERE es.idEsquema=%s ORDER BY tr.idTreball LIMIT 1,200',(idEsquema,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = TreballLF(i[0],i[1],i[2],i[3]) #Modificar si anyadim columna
        indice=indice+1   
    return lista

def tablaTreballsLFF(cursor,idFactura):

    cursor.execute('SELECT lf.idLiniaFactura, lf.idTreball, lf.idFactura FROM factures fa INNER JOIN liniesfactura lf ON  fa.idFactura=lf.idFactura WHERE fa.idFactura=%s',(idFactura,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = TreballLFF(i[0],i[1],i[2]) #Modificar si anyadim columna
        indice=indice+1   
    return lista


def tablaTreballsLSF(cursor,idFactura):

    cursor.execute('SELECT ls.idLiniaSuplidos, ls.suplido, ls.preuSuplido FROM factures fa INNER JOIN liniessuplidos ls ON  fa.idFactura=ls.idFactura WHERE fa.idFactura=%s',(idFactura,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = TreballLSF(i[0],i[1],i[2]) #Modificar si anyadim columna
        indice=indice+1   
    return lista

def tablaTreballProforma(cursor, idFactura):   
    cursor.execute('SELECT tr.idTreball, tr.idTipoTreball, tr.idPressupost, tr.dataTreball, tr.preu, tr.acceptat, tr.patras, tr.presentat, tr.comentari, tr.expAj, tr.numVisado FROM treballs tr INNER JOIN liniesfactura lf ON tr.idTreball = lf.idTreball WHERE lf.idFactura=%s',(idFactura,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Treball(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 


class Proforma:
    def __init__(self, idFactura=0, idEsquema=0, idClient=0, proforma='', dataProforma='', factura='', dataFactura='', dataCobro='', eurComis='', facComisSol=0, comisPagada=0, titolFactura='', factEntregada=0, sobre=0, incobrable=0, idUbicacio=0, enPis=0, total=0, pendent=0, cobrat=0):
        self.idFactura = idFactura
        self.idEsquema = idEsquema
        self.idClient = idClient
        self.proforma = proforma
        self.dataProforma = dataProforma
        self.factura = factura
        self.dataFactura = dataFactura
        self.dataCobro = dataCobro
        self.eurComis = eurComis
        self.facComisSol = facComisSol
        self.comisPagada = comisPagada
        self.titolFactura = titolFactura
        self.factEntregada = factEntregada
        self.sobre = sobre
        self.incobrable = incobrable
        self.idUbicacio = idUbicacio
        self.enPis = enPis
        self.total = total
        self.pendent = pendent
        self.cobrat = cobrat
        

class TreballLF:
    def __init__(self, idTreball=0, treball='', numPressupost='', preu=''):
        self.idTreball = idTreball
        self.treball = treball
        self.numPressupost = numPressupost
        self.preu = preu
        
class TreballLSF:
    def __init__(self, idLiniaSuplidos=0, suplido=0, preuSuplido=0):
        self.idLiniaSuplidos = idLiniaSuplidos
        self.suplido = suplido
        self.preuSuplido = preuSuplido

class TreballLFF:
    def __init__(self, idLiniaFactura=0, idTreball=0, idFactura=0):
        self.idLiniaFactura = idLiniaFactura
        self.idTreball = idTreball
        self.idFactura = idFactura

class TreballProforma:
    def __init__(self, idTreball=0, claveTreball='', numPressupost='', preu=''):
        self.idTreball = idTreball
        self.claveTreball = claveTreball
        self.numPressupost = numPressupost
        self.preu = preu

###########################################################################################################################################################
# TREBALL FAC                TREBALL FAC                TREBALL FAC                TREBALL FAC                TREBALL FAC                TREBALL FAC
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariTreballFac (usuari, idLiniaFactura, idFactura):

    #dataHui
    
    idLiniaFactura=int(idLiniaFactura)

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    treballsLF = tablaTreballsLF(cursor, idFactura)
    treballsLFF = tablaTreballsLFF(cursor, idFactura)
    treballsLSF = tablaTreballsLSF(cursor, idFactura)
    liniaFacturaSelect = ''
    
    preu=""
    treball=""
    
    if idLiniaFactura != -1: #select
        liniaFacturaSelect = tablaLiniaFacturaSelect(cursor,idLiniaFactura)
        
        cursor.execute('SELECT idTreball FROM liniesfactura WHERE idLiniaFactura=%s',(idLiniaFactura,))
        lista = cursor.fetchall()
        idTreball = lista[0][0]
                
        cursor.execute('SELECT idTipoTreball, preu FROM treballs WHERE idTreball=%s',(idTreball,))
        lista = cursor.fetchall()
        idTipoTreball = lista[0][0]
        preu = lista[0][1]
                
        cursor.execute('SELECT treball FROM tipostreball WHERE idTipoTreball=%s',(idTipoTreball,))
        lista = cursor.fetchall()
        treball = lista[0][0]        
        
    cursor.execute('SELECT idEsquema FROM factures WHERE idFactura=%s', (idFactura,))
    vector = cursor.fetchall()
    idEsquema=vector[0][0]
    
    treballAcceptatEsquema=tablaTreballAcceptatEsquema(cursor, idEsquema)
  
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'idLiniaFactura': idLiniaFactura,
             'idFactura': idFactura,
             'treballsLF': treballsLF,
             'treballsLFF': treballsLFF,
             'treballsLSF': treballsLSF,
             'liniaFacturaSelect': liniaFacturaSelect,
             'treballAcceptatEsquema': treballAcceptatEsquema,
             'preu': preu,
             'treball': treball,
              }
    return values  

# ACCIONS DEL FORMULARI
####################################

class TreballFacSelect (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idLiniaFactura = novar(self.request.get('idLiniaFactura'))
                idFactura = novar(self.request.get('idFactura'))

                

                

            
                #obtenim valors per al html
                values = formulariTreballFac(usuari, idLiniaFactura, idFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'treballFac.html') 
                self.response.out.write(template.render(path, values,))

class TreballFacNou (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idLiniaFactura = -1
                idFactura = novar(self.request.get('idFactura'))
                
                
            
                #obtenim valors per al html
                values = formulariTreballFac(usuari, idLiniaFactura, idFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'treballFac.html') 
                self.response.out.write(template.render(path, values,))

class TreballFacElimina (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idLiniaFactura = novar(self.request.get('idLiniaFactura'))
                idFactura = novar(self.request.get('idFactura'))

                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
                
                cursor.execute('DELETE FROM liniesfactura WHERE idLiniaFactura=%s',(idLiniaFactura,))

                cursor.execute('SELECT idEsquema FROM factures WHERE idFactura=%s', (idFactura,))
                vector = cursor.fetchall()
                idEsquema=vector[0][0]
                db.commit()
                db.close()

                #obtenim valors per al html
                values = formulariProforma(usuari, idFactura, idEsquema)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'proforma.html') 
                self.response.out.write(template.render(path, values,))
                
class LiniaFacturaCrea (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idFactura = novar(self.request.get('idFactura'))
                treballNH = novar(self.request.get('treballNH'))
                preu = novar(self.request.get('preu'))
                idLiniaFactura = -1


                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
                
                cursor.execute('INSERT INTO tipostreball (claveTreball, treball, enActiu) VALUES (%s, %s, %s)', ("TNH", treballNH, 0,))
                cursor.execute('SELECT idTipoTreball FROM tipostreball ORDER BY idTipoTreball DESC LIMIT 0,1')
                lista = cursor.fetchall()
                idTipoTreball = lista[0][0]
                cursor.execute('SELECT idEsquema FROM factures WHERE idFactura=%s',(idFactura,))
                lista2 = cursor.fetchall()
                idEsquema = lista2[0][0]
                cursor.execute('INSERT INTO pressupostos (idEsquema, enActiu, idUbicacio, enPis) VALUES (%s, %s, %s, %s)', (idEsquema, 0, 3, 0,))
                cursor.execute('SELECT idPressupost FROM pressupostos ORDER BY idPressupost DESC LIMIT 0,1')
                lista3 = cursor.fetchall()
                idPressupost = lista3[0][0]                   
                cursor.execute('INSERT INTO treballs (idTipoTreball, idPressupost, preu, acceptat) VALUES (%s, %s, %s, %s)', (idTipoTreball, idPressupost, preu, 0,))
                cursor.execute('SELECT idTreball FROM treballs ORDER BY idTreball DESC LIMIT 0,1')
                lista4 = cursor.fetchall()
                idTreball = lista4[0][0] 
                cursor.execute('INSERT INTO liniesfactura (idFactura, idTreball) VALUES (%s,%s)',(idFactura, idTreball,))

                db.commit()
                db.close()
                
            
                #obtenim valors per al html
                values = formulariTreballFac(usuari, idLiniaFactura, idFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'treballFac.html') 
                self.response.out.write(template.render(path, values,))
                
class LiniaFacturaEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                treballNH = novar(self.request.get('treballNH'))
                preu = novar(self.request.get('preu'))
                idLiniaFactura = novar(self.request.get('idLiniaFactura'))
                idFactura = novar(self.request.get('idFactura'))

                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
                
                cursor.execute('SELECT idTreball FROM liniesfactura WHERE idLiniaFactura=%s',(idLiniaFactura,))
                lista = cursor.fetchall()
                idTreball = lista[0][0]
                
                cursor.execute('SELECT idTipoTreball FROM treballs WHERE idTreball=%s',(idTreball,))
                lista = cursor.fetchall()
                idTipoTreball = lista[0][0]
                
                cursor.execute('UPDATE tipostreball SET treball=%s WHERE idTipoTreball=%s', (treballNH, idTipoTreball,)) 
                cursor.execute('UPDATE treballs SET preu=%s WHERE idTreball=%s', (preu, idTreball,))          
           
                
                cursor.execute('UPDATE liniesfactura SET idTreball=%s WHERE idLiniaFactura=%s',(idTreball, idLiniaFactura,))

                db.commit()
                db.close()
                
            
                #obtenim valors per al html
                values = formulariTreballFac(usuari, idLiniaFactura, idFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'treballFac.html') 
                self.response.out.write(template.render(path, values,))
              


# FUNCIONS SECUNDARIES DEL FORMULARI
####################################

def tablaLiniaFacturaSelect(cursor, idLiniaFactura):
    cursor.execute('SELECT idLiniaFactura,idTreball, idFactura FROM liniesfactura WHERE idLiniaFactura=%s',(idLiniaFactura,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista = TreballLFF(i[0],i[1],i[2]) #Modificar si anyadim columna 
    return lista 


###########################################################################################################################################################
# SUPLIDO FAC                SUPLIDO FAC                SUPLIDO FAC                SUPLIDO FAC                SUPLIDO FAC                SUPLIDO FAC 
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariSuplidoFac (usuari, idLiniaSuplidos, idFactura):

    #dataHui
    
    idLiniaSuplido=int(idLiniaSuplidos)

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    treballsLF = tablaTreballsLF(cursor, idFactura)
    treballsLFF = tablaTreballsLFF(cursor, idFactura)
    treballsLSF = tablaTreballsLSF(cursor, idFactura)
    liniaSuplidoSelect = ''
    
    if idLiniaSuplido != -1: #nou
        liniaSuplidoSelect = tablaLiniaSuplidoSelect(cursor,idLiniaSuplidos)
  
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'idLiniaSuplidos': idLiniaSuplidos,
             'idFactura': idFactura,
             'treballsLF': treballsLF,
             'treballsLFF': treballsLFF,
             'treballsLSF': treballsLSF,
             'liniaSuplidoSelect': liniaSuplidoSelect,
              }
    return values  

# ACCIONS DEL FORMULARI
####################################

class SuplidoFacSelect (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idLiniaSuplidos = novar(self.request.get('idLiniaSuplidos'))
                idFactura = novar(self.request.get('idFactura'))
            
                #obtenim valors per al html
                values = formulariSuplidoFac(usuari, idLiniaSuplidos, idFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'suplidoFac.html') 
                self.response.out.write(template.render(path, values,))

class SuplidoFacNou (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idLiniaSuplidos = -1
                idFactura = novar(self.request.get('idFactura'))
            
                #obtenim valors per al html
                values = formulariSuplidoFac(usuari, idLiniaSuplidos, idFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'suplidoFac.html') 
                self.response.out.write(template.render(path, values,))

class SuplidoFacElimina (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idLiniaSuplidos = novar(self.request.get('idLiniaSuplidos'))
                idFactura = novar(self.request.get('idFactura'))

                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
                
                cursor.execute('DELETE FROM liniessuplidos WHERE idLiniaSuplidos=%s',(idLiniaSuplidos,))

                cursor.execute('SELECT idEsquema FROM factures WHERE idFactura=%s', (idFactura,))
                vector = cursor.fetchall()
                idEsquema=vector[0][0]
                db.commit()
                db.close()

                #obtenim valors per al html
                values = formulariProforma(usuari, idFactura, idEsquema)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'proforma.html') 
                self.response.out.write(template.render(path, values,))
                
class LiniaSuplidoCrea (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idFactura = novar(self.request.get('idFactura'))
                suplido = novar(self.request.get('suplido'))
                preuSuplido = novar(self.request.get('preuSuplido'))
                idLiniaSuplidos = -1

                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
                
                cursor.execute('INSERT INTO liniessuplidos (idFactura, suplido, preuSuplido) VALUES (%s,%s,%s)',(idFactura, suplido, preuSuplido,))

                db.commit()
                db.close()
                
            
                #obtenim valors per al html
                values = formulariSuplidoFac(usuari, idLiniaSuplidos, idFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'suplidoFac.html') 
                self.response.out.write(template.render(path, values,))
                
class LiniaSuplidoEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idFactura = novar(self.request.get('idFactura'))
                suplido = novar(self.request.get('suplido'))
                preuSuplido = novar(self.request.get('preuSuplido'))
                idLiniaSuplidos = novar(self.request.get('idLiniaSuplidos'))

                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
                
                cursor.execute('UPDATE liniessuplidos SET suplido=%s, preuSuplido=%s WHERE idLiniaSuplidos=%s',(suplido, preuSuplido, idLiniaSuplidos,))

                db.commit()
                db.close()
                
            
                #obtenim valors per al html
                values = formulariSuplidoFac(usuari, idLiniaSuplidos, idFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'suplidoFac.html') 
                self.response.out.write(template.render(path, values,))
              


# FUNCIONS SECUNDARIES DEL FORMULARI
####################################

def tablaLiniaSuplidoSelect(cursor, idLiniaSuplidos):
    cursor.execute('SELECT idLiniaSuplidos,suplido, preuSuplido FROM liniessuplidos WHERE idLiniaSuplidos=%s',(idLiniaSuplidos,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista = TreballLSF(i[0],i[1],i[2]) #Modificar si anyadim columna 
    return lista 
###########################################################################################################################################################
# FACTURA IMP        FACTURA IMP        FACTURA IMP        FACTURA IMP        FACTURA IMP        FACTURA IMP        FACTURA IMP        FACTURA IMP
###########################################################################################################################################################

        
#--IMPRIMEIX FACTURA O PROFORMA
class ImpFactura(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):           
            #captura camps del html
            esFactura = novar(self.request.get('esFactura'))
            idFactura = novar(self.request.get('idFactura'))
                    
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            #obtenir total linies factura
            cursor.execute('SELECT SUM(tr.preu) AS preuLF FROM treballs tr INNER JOIN liniesfactura lf ON tr.idTreball=lf.idTreball GROUP BY lf.idFactura HAVING lf.idFactura=%s',(idFactura,))
            tSumPreuLF = cursor.fetchall()
            sumPreuLF = tSumPreuLF[0] [0]
            
            #obtenir total linies suplidos
            cursor.execute('SELECT SUM(preuSuplido) AS preuLS FROM liniessuplidos GROUP BY idFactura HAVING idFactura=%s',(idFactura,))
            tSumPreuLS = cursor.fetchall()
            if tSumPreuLS:
                sumPreuLS = tSumPreuLS[0] [0]
            else:
                sumPreuLS = 0
            
            #obtenir tipo IVA
            cursor.execute('SELECT tipoIVA FROM constants WHERE idConstant=%s',(1,))
            tTipoIVA = cursor.fetchall()
            tipoIVA = tTipoIVA [0] [0]
            
            #obtenir IVA
            iva = sumPreuLF*tipoIVA
            
            #obtenir total Bruto
            totalBruto = sumPreuLF*(1+tipoIVA)
            
            #obtenir total Factura
            totalFactura = sumPreuLF*(1+tipoIVA)+ sumPreuLS
            
            #tables factura
            liniesFactura = tablaLFFactura(cursor, idFactura)
            liniesSuplidos = tablaLSFactura(cursor, idFactura)
            facturaSelect = tablaProformaSelect(cursor, idFactura)
            tiposTreball = tablaTipoTreballTots(cursor)
            bancs = tablaBancs (cursor)
            clients = tablaClientTots (cursor)
            
            #donar formato
            sumPreuLF = "%.2f" %sumPreuLF
            sumPreuLS = "%.2f" %sumPreuLS
            totalFactura = "%.2f" %totalFactura
            iva = "%.2f" %iva
            totalBruto = "%.2f" %totalBruto
            tipoIVA = tipoIVA*100
            esFactura = int(esFactura)
            
            db.commit()
            db.close()
    
            #pasem les llistes al arxiu html
            values = {
                'esFactura': esFactura,
                'facturaSelect': facturaSelect,
                'liniesFactura': liniesFactura,
                'liniesSuplidos': liniesSuplidos,
                'bancs': bancs,
                'tiposTreball': tiposTreball,
                'clients': clients,
                'sumPreuLF': sumPreuLF,
                'sumPreuLS': sumPreuLS,
                'iva': iva,
                'totalBruto': totalBruto,
                'totalFactura': totalFactura,
                'tipoIVA': tipoIVA
                      }
            
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'facturaImp.html') 
            self.response.out.write(template.render(path, values,))         


class ImprimirFactura(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):           
            #captura camps del html
            esFactura = novar(self.request.get('esFactura'))
            idFactura = novar(self.request.get('idFactura'))
                    
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            #obtenir total linies factura
            cursor.execute('SELECT SUM(tr.preu) AS preuLF FROM treballs tr INNER JOIN liniesfactura lf ON tr.idTreball=lf.idTreball GROUP BY lf.idFactura HAVING lf.idFactura=%s',(idFactura,))
            tSumPreuLF = cursor.fetchall()
            sumPreuLF = tSumPreuLF[0] [0]
            
            #obtenir total linies suplidos
            cursor.execute('SELECT SUM(preuSuplido) AS preuLS FROM liniessuplidos GROUP BY idFactura HAVING idFactura=%s',(idFactura,))
            tSumPreuLS = cursor.fetchall()
            if tSumPreuLS:
                sumPreuLS = tSumPreuLS[0] [0]
            else:
                sumPreuLS = 0
            
            #obtenir tipo IVA
            cursor.execute('SELECT tipoIVA FROM constants WHERE idConstant=%s',(1,))
            tTipoIVA = cursor.fetchall()
            tipoIVA = tTipoIVA [0] [0]
            
            #obtenir IVA
            iva = sumPreuLF*tipoIVA
            
            #obtenir total Bruto
            totalBruto = sumPreuLF*(1+tipoIVA)
            
            #obtenir total Factura
            totalFactura = sumPreuLF*(1+tipoIVA)+ sumPreuLS
            
            #tables factura
            liniesFactura = tablaLFFactura(cursor, idFactura)
            liniesSuplidos = tablaLSFactura(cursor, idFactura)
            facturaSelect = tablaProformaSelect(cursor, idFactura)
            tiposTreball = tablaTipoTreballTots(cursor)
            bancs = tablaBancs (cursor)
            clients = tablaClientTots (cursor)
            
            #donar formato
            sumPreuLF = "%.2f" %sumPreuLF
            sumPreuLS = "%.2f" %sumPreuLS
            totalFactura = "%.2f" %totalFactura
            iva = "%.2f" %iva
            totalBruto = "%.2f" %totalBruto
            tipoIVA = tipoIVA*100
            esFactura = int(esFactura)
            
            db.commit()
            db.close()
    
            #pasem les llistes al arxiu html
            values = {
                'esFactura': esFactura,
                'facturaSelect': facturaSelect,
                'liniesFactura': liniesFactura,
                'liniesSuplidos': liniesSuplidos,
                'bancs': bancs,
                'tiposTreball': tiposTreball,
                'clients': clients,
                'sumPreuLF': sumPreuLF,
                'sumPreuLS': sumPreuLS,
                'iva': iva,
                'totalBruto': totalBruto,
                'totalFactura': totalFactura,
                'tipoIVA': tipoIVA
                      }
            
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'imprimirFactura.html') 
            self.response.out.write(template.render(path, values,))         



class ImprimirPresupuesto(webapp2.RequestHandler):
    
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):           
            #captura camps del html
            idPressupost = novar(self.request.get('idPressupost'))

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('SELECT SUM(preu) AS preuT FROM treballs WHERE idPressupost=%s GROUP BY idPressupost',(idPressupost,))
            tabla = cursor.fetchall()
            totalPressup = tabla[0][0]
            cursor.execute('SELECT tipoIVA FROM constants WHERE idConstant=%s',(1,))
            tabla = cursor.fetchall()
            tipoIVA = tabla [0][0]
            iva = totalPressup*tipoIVA
            totalBruto = totalPressup*(1+tipoIVA)
            treballsPressup = tablaTreballPressup (cursor, idPressupost)
            pressupSelect = tablaPressupostSelect(cursor, idPressupost)
            tiposTreball = tablaTipoTreballTots (cursor)
            bancs = tablaBancs (cursor)
            clients = tablaClientEsquema(cursor)

            #donar formato
            totalPressup = "%.2f" %totalPressup
            iva = "%.2f" %iva
            totalBruto = "%.2f" %totalBruto
            tipoIVA = tipoIVA*100
            #tanca conexio
            db.commit()
            db.close()
        
        
        
        #pasem les llistes al arxiu html
        values = {
            'pressupSelect': pressupSelect,
            'treballsPressup': treballsPressup,
            'bancs': bancs,
            'tiposTreball': tiposTreball,
            'totalPressup': totalPressup,
            'iva': iva,
            'totalBruto': totalBruto,
            'tipoIVA': tipoIVA,
            'clients':clients
                }
        
        #imprimim el arxiu html    
        path = os.path.join(os.path.dirname(__file__), 'presupuesto.html')
        self.response.out.write(template.render(path, values,))
     

#--FUNCIO TABLA LINIES FACTURA DE LA FACTURA
#--Entrades: Resultat de la conexio amb la BD, idFactura
#--Resultat: Lista de objectes
def tablaLFFactura(cursor, idFactura):
    cursor.execute('SELECT lf.idLiniaFactura, lf.idTreball, lf.idFactura, tr.idTipoTreball, tr.preu FROM treballs tr INNER JOIN liniesfactura lf ON lf.idTreball = tr.idTreball WHERE lf.idFactura=%s ORDER BY lf.idLiniaFactura LIMIT 0,500', (idFactura,))
    liniesFactura = cursor.fetchall()
    conta=0
    indice=0
    for i in liniesFactura: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in liniesFactura: #cada fila es converteix en un objecte de lista
        p = "%.2f" %i[4]
        lista[indice] = LiniesFactura(i[0],i[1],i[2],i[3],p) #Modificar si anyadim columna
        indice=indice+1   
    return lista

#--FUNCIO TABLA LINIES SUPLIDOS DE LA FACTURA
#--Entrades: Resultat de la conexio amb la BD, idFactura
#--Resultat: Lista de objectes
def tablaLSFactura(cursor, idFactura):
    cursor.execute('SELECT idLiniaSuplidos, idFactura, suplido, preuSuplido FROM liniessuplidos WHERE idFactura=%s ORDER BY idLiniaSuplidos LIMIT 0,500', (idFactura,))
    liniesSuplidos = cursor.fetchall()
    conta=0
    indice=0
    for i in liniesSuplidos: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in liniesSuplidos: #cada fila es converteix en un objecte de lista
        p = "%.2f" %i[3]
        lista[indice] = LiniesSuplidos(i[0],i[1],i[2],p) #Modificar si anyadim columna
        indice=indice+1   
    return lista   

class LiniesFactura: 
    def __init__(self, idLiniaFactura=0, idTreball=0, idFactura=0, idTipoTreball=0, preu=''):
        self.idLiniaFactura = idLiniaFactura
        self.idTreball = idTreball
        self.idFactura = idFactura
        self.idTipoTreball = idTipoTreball
        self.preu = preu

class LiniesSuplidos: 
    def __init__(self, idLiniaSuplidos=0, idFactura=0, suplido='', preuSuplido=0):
        self.idLiniaSuplidos = idLiniaSuplidos
        self.idFactura = idFactura
        self.suplido = suplido
        self.preuSuplido = preuSuplido 
        
###########################################################################################################################################################
# MOVIMENTS          MOVIMENTS          MOVIMENTS          MOVIMENTS          MOVIMENTS          MOVIMENTS          MOVIMENTS          MOVIMENTS
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariMoviment (usuari, idMoviment, idFactura):

    #dataHui
    ara = datetime.datetime.today()
    dataHui = ara.strftime('%Y-%m-%d')

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    treballadorTots = tablaTreballadorTots(cursor)
    bancs = tablaBancs(cursor)
    treballadorAct = tablaTreballadorAct(cursor)
    movimentUltims = ''
    movimentSelect = ''
    quadraBancUltim = ''
    saldoBanc = ''
    dataCobro=''
    total=''
    cobrat=''
    pendent=''

    
    if idMoviment == -1: #nou
        movimentUltims = tablaMovimentsUltims(cursor)
        saldoBanc = tablaSaldoBancs(cursor)
        quadraBancUltim = tablaQuadraBancUltim(cursor) 
        
    elif idMoviment < -1:
        dataHui = dataHui
        
    else: # select
        movimentSelect = tablaMovimentSelect(cursor, idMoviment)
        cursor.execute('SELECT idFactura FROM moviments WHERE idMoviment=%s', (idMoviment,))
        vector= cursor.fetchall()
        idFactura2 = vector[0][0] 
        try:
            idFactura2=int(idFactura2)            
        except:
            idFactura2=-1   
        if idFactura2>0: 
            cursor.execute('SELECT dataCobro FROM factures WHERE idFactura=%s', (idFactura2,))
            vector= cursor.fetchall()
            dataCobro = vector[0][0]
            dataCobro = dataFormat(dataCobro)
            #obtenir total linies factura
            cursor.execute('SELECT SUM(tr.preu) AS preuLF FROM treballs tr INNER JOIN liniesfactura lf ON tr.idTreball=lf.idTreball GROUP BY lf.idFactura HAVING lf.idFactura=%s',(idFactura2,))
            tSumPreuLF = cursor.fetchall()
            try:
                tProforma = tSumPreuLF[0] [0]
            except:
                tProforma = 0
            
            #obtenir total linies suplidos
            cursor.execute('SELECT SUM(preuSuplido) AS preuLS FROM liniessuplidos GROUP BY idFactura HAVING idFactura=%s',(idFactura2,))
            tSumPreuLS = cursor.fetchall()
            try:
                tSuplido = tSumPreuLS[0] [0]
            except:
                tSuplido = 0
                
            #obtenir iva
            cursor.execute('SELECT factura FROM factures WHERE idFactura=%s',(idFactura2,))
            vector = cursor.fetchall()
            try:
                factura = vector [0] [0]
            except:
                factura = 0
            
            if factura != 0:
                cursor.execute('SELECT tipoIVA FROM constants WHERE idConstant=%s',(1,))
                tabla = cursor.fetchall()
                tipoIVA = tabla [0][0]
                iva = tProforma*tipoIVA
            else:
                iva=0
            
            #cobrat
            cursor.execute('SELECT SUM(quantitat) AS q FROM moviments GROUP BY idFactura HAVING idFactura=%s',(idFactura2,))
            vector = cursor.fetchall()
            try:
                cobrat = vector [0] [0]
            except:
                cobrat = 0
            
            total = tProforma+tSuplido+iva
            pendent = total - cobrat
            
            total = "%.2f" %total
            pendent = "%.2f" %pendent
            cobrat = "%.2f" %cobrat

    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'treballadorTots': treballadorTots,
             'treballadorAct': treballadorAct,
             'idMoviment': idMoviment,
             'movimentUltims': movimentUltims,
             'dataHui': dataHui,
             'movimentSelect': movimentSelect,
             'bancs': bancs,
             'quadraBancUltim': quadraBancUltim,
             'saldoBanc': saldoBanc,
             'idFactura': idFactura,
             'dataCobro': dataCobro,
             'total': total,
             'pendent': pendent,
             'cobrat': cobrat
             
              }
    return values  

# ACCIONS DEL FORMULARI
####################################

                
class MovimentInicial (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idMoviment = -1
                idFactura = -1
            
                #obtenim valors per al html
                values = formulariMoviment(usuari, idMoviment, idFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'moviment.html') 
                self.response.out.write(template.render(path, values,))

class MovimentNouIngres (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idMoviment = -2
                idFactura = -1
            
                #obtenim valors per al html
                values = formulariMoviment(usuari, idMoviment, idFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'moviment.html') 
                self.response.out.write(template.render(path, values,))

class MovimentNouGasto (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idMoviment = -3
                idFactura = -1
                #obtenim valors per al html
                values = formulariMoviment(usuari, idMoviment, idFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'moviment.html') 
                self.response.out.write(template.render(path, values,))
                
class MovimentNouIngresProf (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idMoviment = -4
                idFactura = novar(self.request.get('idFactura'))            
            
                #obtenim valors per al html
                values = formulariMoviment(usuari, idMoviment, idFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'moviment.html') 
                self.response.out.write(template.render(path, values,))

class MovimentNouTraspas (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idMoviment = -5
                idFactura = -1           
            
                #obtenim valors per al html
                values = formulariMoviment(usuari, idMoviment, idFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'moviment.html') 
                self.response.out.write(template.render(path, values,))

class MovimentSelect (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idMoviment = novar(self.request.get('idMoviment'))
                idFactura = novar(self.request.get('idFactura'))
                if idFactura == "":
                    idFactura=-1  
            
                #obtenim valors per al html
                values = formulariMoviment(usuari, idMoviment, idFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'moviment.html') 
                self.response.out.write(template.render(path, values,))


class MovimentCreaIngres (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            dataMov  = novar(self.request.get('dataMov'))
            idTreballador  = novar(self.request.get('idTreballador'))
            quantitat  = novar(self.request.get('quantitat'))
            descripcio = novar(self.request.get('descripcio'))
            idTipoMov= 6
            idBanc = 2 #banc
            idBanc2 = 1 #caixa

            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('INSERT INTO moviments (idTipoMov, idTreballador, idBanc, idBanc2, dataMov, quantitat, descripcio) VALUES (%s, %s, %s, %s, %s, %s, %s)', (idTipoMov, idTreballador, idBanc, idBanc2, dataMov, quantitat, descripcio,))
            
            db.commit()
            db.close()

            idMoviment = -1
            idFactura = -1
            
            #obtenim valors per al html
            values = formulariMoviment(usuari, idMoviment, idFactura)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'moviment.html') 
            self.response.out.write(template.render(path, values,))
            
class MovimentCreaGasto (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            dataMov  = novar(self.request.get('dataMov'))
            idTreballador  = novar(self.request.get('idTreballador'))
            quantitat  = novar(self.request.get('quantitat'))
            descripcio = novar(self.request.get('descripcio'))
            tipoGasto = novar(self.request.get('tipoGasto'))
            tipoGasto = int(tipoGasto)
            idBanc = 1

            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            if tipoGasto == 5: #cartereta
                idTipoMov = 2
                idGasto = 5 
                cursor.execute('INSERT INTO moviments (idTipoMov, idTreballador, idBanc, idGasto, dataMov, quantitat, descripcio) VALUES (%s, %s, %s, %s, %s, %s, %s)', (idTipoMov, idTreballador, idBanc, idGasto, dataMov, quantitat, descripcio,))
            elif tipoGasto ==1: #altres
                idTipoMov = 2
                idGasto = 1
                cursor.execute('INSERT INTO moviments (idTipoMov, idTreballador, idBanc, idGasto, dataMov, quantitat, descripcio) VALUES (%s, %s, %s, %s, %s, %s, %s)', (idTipoMov, idTreballador, idBanc, idGasto, dataMov, quantitat, descripcio,))
            elif tipoGasto ==3: #banc
                idTipoMov = 6
                idBanc2 = 2
                cursor.execute('INSERT INTO moviments (idTipoMov, idTreballador, idBanc, idBanc2, dataMov, quantitat, descripcio) VALUES (%s, %s, %s, %s, %s, %s, %s)', (idTipoMov, idTreballador, idBanc, idBanc2, dataMov, quantitat, descripcio,))
            else:   #complement
                idTipoMov = 2
                idGasto = 21
                cursor.execute('INSERT INTO moviments (idTipoMov, idTreballador, idBanc, idGasto, dataMov, quantitat, descripcio) VALUES (%s, %s, %s, %s, %s, %s, %s)', (idTipoMov, idTreballador, idBanc, idGasto, dataMov, quantitat, descripcio,))
            
            db.commit()
            db.close()

            idMoviment = -1
            idFactura = -1
            
            #obtenim valors per al html
            values = formulariMoviment(usuari, idMoviment, idFactura)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'moviment.html') 
            self.response.out.write(template.render(path, values,))
            
    


class MovimentEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idMoviment= novar(self.request.get('idMoviment'))
            idTreballador= novar(self.request.get('idTreballador'))
            dataMov = novar(self.request.get('dataMov'))
            quantitat = novar(self.request.get('quantitat'))
            descripcio = novar(self.request.get('descripcio'))
            idBanc2 = novar(self.request.get('idBanc2'))
            idFactura = novar(self.request.get('idFactura'))
            try:
                idFactura=int(idFactura)            
            except:
                idFactura=-1  
                
          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('UPDATE moviments SET idTreballador=%s, dataMov=%s, quantitat=%s, descripcio=%s WHERE idMoviment=%s', (idTreballador, dataMov, quantitat, descripcio, idMoviment,))          
           
            db.commit()
            db.close()  
            if idFactura != -1:
                
                db= get_db()
                cursor = db.cursor()
                
                cursor.execute('SELECT SUM(quantitat) AS q FROM moviments GROUP BY idFactura HAVING idFactura=%s',(idFactura,))
                vector = cursor.fetchall()
                try:
                    cobrat = vector [0] [0]
                except:
                    cobrat = 0
                
                cursor.execute('SELECT SUM(tr.preu) AS preuLF FROM treballs tr INNER JOIN liniesfactura lf ON tr.idTreball=lf.idTreball GROUP BY lf.idFactura HAVING lf.idFactura=%s',(idFactura,))
                tSumPreuLF = cursor.fetchall()
                try:
                    tProforma = tSumPreuLF[0][0]
                except:
                    tProforma = 0
                
                if cobrat <> 0 and cobrat >= tProforma:
                    dataCobro = dataMov
                else:
                    dataCobro = ""
                
                cursor.execute('UPDATE moviments SET idBanc2=%s WHERE idMoviment=%s', (idBanc2, idMoviment,))
                cursor.execute('UPDATE factures SET dataCobro=%s WHERE idFactura=%s', (dataCobro, idFactura,))      
                cursor.execute('SELECT fa.idEsquema FROM factures fa INNER JOIN moviments mo ON fa.idFactura=mo.idFactura WHERE idMoviment=%s',(idMoviment,))
                vector=cursor.fetchall()
                idEsquema=vector[0][0]
                
                db.commit()
                db.close()     
                
                idTarea = -1
                idHistoria = -1
                
                #obtenim valors per al html
                values = esquema(usuari, idEsquema, idTarea, idHistoria)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
                self.response.out.write(template.render(path, values,))
            else:
             
                idMoviment = -1
                idFactura = -1
                #obtenim valors per al html
                values = formulariMoviment(usuari, idMoviment, idFactura)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'moviment.html') 
                self.response.out.write(template.render(path, values,))



class MovimentElimina (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idMoviment= novar(self.request.get('idMoviment'))
          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('DELETE FROM moviments WHERE idMoviment=%s', (idMoviment,))          
            db.commit()
            db.close()
            
            idMoviment = -1
            idFactura = -1

            #obtenim valors per al html
            values = formulariMoviment(usuari, idMoviment, idFactura)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'moviment.html') 
            self.response.out.write(template.render(path, values,))

class QuadraCaixa (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            #dataHui
            ara = datetime.datetime.today()
            hui = ara.strftime('%Y-%m-%d')
            
            #captura del html
            dataQuadraBanc  = hui
            idTreballador  = novar(self.request.get('idTreballador'))
            idBanc = 1 #caixa

            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('INSERT INTO quadrabancs (idTreballador, idBanc, dataQuadraBanc) VALUES (%s, %s, %s)', (idTreballador, idBanc, dataQuadraBanc,))
            
            db.commit()
            db.close()

            idMoviment = -1
            idFactura = -1
            
            #obtenim valors per al html
            values = formulariMoviment(usuari, idMoviment, idFactura)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'moviment.html') 
            self.response.out.write(template.render(path, values,))
            

class CreaIngresProf (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            dataMov  = novar(self.request.get('dataMov'))
            idTreballador  = novar(self.request.get('idTreballador'))
            quantitat  = novar(self.request.get('quantitat'))
            descripcio = novar(self.request.get('descripcio'))
            idFactura  = novar(self.request.get('idFactura'))
            idBanc2  = novar(self.request.get('idBanc2'))
            idTipoMov= 1
            
            if idBanc2 == 0: # si obliden seleccionar desti que torne a carregar formulari per a crear ingres
                #parametres
                idMoviment = -4
            
                #obtenim valors per al html
                values = formulariMoviment(usuari, idMoviment, idFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'moviment.html') 
                self.response.out.write(template.render(path, values,))
            else:

                #accions sobre bd
                db= get_db()
                cursor = db.cursor()
                
                cursor.execute('INSERT INTO moviments (idTipoMov, idTreballador, idFactura, idBanc2, dataMov, quantitat, descripcio) VALUES (%s, %s, %s, %s, %s, %s, %s)', (idTipoMov, idTreballador, idFactura, idBanc2, dataMov, quantitat, descripcio,))
                
                cursor.execute('SELECT idEsquema FROM factures WHERE idFactura=%s', (idFactura,))
                vector= cursor.fetchall()
                idEsquema = vector[0][0]
                
                cursor.execute('SELECT SUM(quantitat) AS q FROM moviments GROUP BY idFactura HAVING idFactura=%s',(idFactura,))
                vector = cursor.fetchall()
                try:
                    cobrat = vector [0] [0]
                except:
                    cobrat = 0
                
                cursor.execute('SELECT SUM(tr.preu) AS preuLF FROM treballs tr INNER JOIN liniesfactura lf ON tr.idTreball=lf.idTreball GROUP BY lf.idFactura HAVING lf.idFactura=%s',(idFactura,))
                tSumPreuLF = cursor.fetchall()
                try:
                    tProforma = tSumPreuLF[0][0]
                except:
                    tProforma = 0
                
                if cobrat <> 0 and cobrat >= tProforma:
                    dataCobro = dataMov
                else:
                    dataCobro = ""                
                
                cursor.execute('UPDATE factures SET dataCobro=%s WHERE idFactura=%s', (dataCobro, idFactura,))          
           
                db.commit()
                db.close()
    
                idTarea = -1
                idHistoria = -1
                #obtenim valors per al html
                values = esquema(usuari, idEsquema, idTarea, idHistoria)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
                self.response.out.write(template.render(path, values,))


# FUNCIONS SECUNDARIES DEL FORMULARI
####################################




def tablaMovimentsUltims(cursor):
    cursor.execute('SELECT idMoviment, idTreballador, idTipoMov, dataMov, idBanc, idBanc2, idGasto, idFactura, quantitat, descripcio FROM moviments WHERE (idBanc=%s AND idTipoMov != %s AND idTipoMov != %s AND idTipoMov != %s) OR (idBanc2=%s AND idTipoMov != %s AND idTipoMov != %s AND idTipoMov != %s) ORDER BY dataMov DESC, idMoviment DESC LIMIT 0,500', (1,3,4,5,1,3,4,5,))
    tabla = cursor.fetchall()  
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[3])
        if i[1]:
            idTreballador=i[1]
        else:
            idTreballador=8
            
        if i[2]==1:
                idFactura=i[7]
                idBanc2=int(i[5])
                cursor.execute('SELECT cl.nomClient FROM clients cl INNER JOIN factures fa ON fa.idClient = cl.idClient WHERE fa.idFactura=%s',(idFactura,))
                vector=cursor.fetchall()
                origen = vector[0][0]
                desti = "caixa"
                quantitat = i[8]
                descripcio = i[9]
                
        elif i[2]==2:
                origen="caixa"
                idGasto=int(i[6])
                cursor.execute('SELECT gasto FROM gastos WHERE idGasto=%s',(idGasto,))
                vector=cursor.fetchall()
                desti = vector[0][0]
                quantitat = i[8]
                descripcio = i[9]
                               
        elif i[2]==6:
                idBanc=i[4]
                idBanc2=i[5]
                cursor.execute('SELECT claveBanc FROM bancs WHERE idBanc=%s',(idBanc,))
                vector=cursor.fetchall()
                origen = vector[0][0]
                cursor.execute('SELECT claveBanc FROM bancs WHERE idBanc=%s',(idBanc2,))
                vector=cursor.fetchall()
                desti = vector[0][0]
                quantitat = i[8]
                descripcio = i[9]
        else:
            origen = ""
            desti = ""
            quantitat = 0 
            descripcio = ""
          
        lista[indice] = Mov(i[0],idTreballador,i[2],data,origen,desti,quantitat,descripcio,i[7],i[5]) #Modificar si anyadim columna
        indice=indice+1   
    return lista



  
def tablaMovimentsEsquema(cursor, idEsquema):
    cursor.execute('SELECT mo.idMoviment, mo.idFactura, mo.dataMov, mo.dataFact, mo.descripcio, mo.quantitat, mo.iva, mo.declarat, mo.provisional, fa.proforma, fa.factura FROM factures fa INNER JOIN moviments mo ON mo.idFactura = fa.idFactura WHERE fa.idEsquema=%s ORDER BY dataMov DESC', (idEsquema,))
    movs = cursor.fetchall()
    conta=0
    indice=0
    for i in movs: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in movs: #cada fila es converteix en un objecte de lista
        dataM=dataFormat(i[2])
        dataF=dataFormat(i[3])
        lista[indice] = MovimentsFac2(i[0],i[1],dataM,dataF,i[4],i[5],i[6],i[7],i[8],i[9],i[10]) #Modificar si anyadim columna
        indice=indice+1   
    return lista

def tablaMovimentSelect(cursor, idMoviment):
    cursor.execute('SELECT idMoviment, idTreballador, idTipoMov, dataMov, idBanc, idBanc2, idGasto, idFactura, quantitat, descripcio FROM moviments WHERE idMoviment=%s',(idMoviment,))
    tabla = cursor.fetchall()  
    for i in tabla: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[3])
        if i[2]==1:
            origen=i[7]
            desti=i[5]
        elif i[2]==2:
            origen=i[4]
            desti=i[6]
        else:
            origen=i[4]
            desti=i[5]
            
        lista = Mov(i[0],i[1],i[2],data,origen,desti,i[8],i[9],i[7],i[5]) #Modificar si anyadim columna 
    return lista 

def tablaQuadraBancUltim(cursor):
    cursor.execute('SELECT idQuadraBanc, idTreballador, idBanc, dataQuadraBanc FROM quadrabancs ORDER BY idQuadraBanc DESC LIMIT 0,1')
    tabla = cursor.fetchall()  
    for i in tabla: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[3])   
        lista = QuadraBanc(i[0],i[1],i[2],data) #Modificar si anyadim columna 
    return lista 


def tablaSaldoBancs(cursor):

        #dataHui
        ara = datetime.datetime.today()
        hui = ara.strftime('%Y-%m-%d')

        
        inicial = 18772.43 #caixa
        idBanc=1 #caixa
        
        cursor.execute('SELECT SUM(quantitat) AS tquantitat FROM moviments WHERE dataMov<=%s GROUP BY idBanc2 HAVING idBanc2=%s',(hui, idBanc,))
        entrades = cursor.fetchall()
        for i in entrades: 
            tquantitate = i[0]
        try:
            entradaT = tquantitate
        except:
            entradaT = 0
        
        cursor.execute('SELECT SUM(quantitat) AS tquantitat FROM moviments WHERE dataMov<=%s GROUP BY idBanc HAVING idBanc=%s',(hui, idBanc,))
        eixides = cursor.fetchall()
        for i in eixides: 
            tquantitatx = i[0]

        try: 
            eixidaT = tquantitatx
        except:
            eixidaT = 0
        
        saldoBanc = entradaT-eixidaT+inicial
        saldoBanc = "%.2f" %saldoBanc        

        lista = saldoBanc

        return lista

class QuadraBanc:
    def __init__(self, idQuadraBanc=0, idTreballador=0, idBanc=0, dataQuadraBanc=''):
        self.idQuadraBanc = idQuadraBanc
        self.idTreballador= idTreballador
        self.idBanc = idBanc
        self.dataQuadraBanc = dataQuadraBanc 



class Mov:
    def __init__(self, idMoviment=0, idTreballador=0, idTipoMov=0, dataMov='', origen='', desti='', quantitat='', descripcio='', idFactura=-1, idBanc2=0):
        self.idMoviment = idMoviment
        self.idTreballador = idTreballador
        self.idTipoMov = idTipoMov
        self.dataMov = dataMov
        self.origen = origen
        self.desti = desti
        self.quantitat = quantitat
        self.descripcio = descripcio  
        self.idFactura=idFactura
        self.idBanc2=idBanc2

        
class MovimentsFac2:
    def __init__(self, idMoviment=0, idFactura=0, dataMov='', dataFact='', descripcio='', quantitat=0, iva=0, declarat=0, provisional=0, proforma=0, factura=0):
        self.idMoviment = idMoviment
        self.idFactura = idFactura
        self.dataMov = dataMov
        self.dataFact = dataFact
        self.descripcio = descripcio
        self.quantitat = quantitat
        self.iva = iva
        self.declarat = declarat
        self.provisional = provisional  
        self.proforma = proforma
        self.factura = factura  
        

###########################################################################################################################################################
# PISSARRA         PISSARRA         PISSARRA         PISSARRA         PISSARRA         PISSARRA         PISSARRA         PISSARRA         PISSARRA 
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariPissarra (usuari, tipo):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    pissarraFacAR=''
    pissarraCobroAR = ''
    totalFacAR=''
    totalEmpresaFac=''
    totalEmpresaCob=''
    totalPendAR=''
    totalPendCobAR=''
    totalCobAR=''
    pissarraMes=''

    
    if tipo == -1: #elegir
        pissarraMes=tablaPissarraMes(cursor)

        
    elif tipo == -2: #facturacio
        pissarraFacAR=tablaPissarraFacArmonic(cursor)
        totalFacAR=totalPissarraFacArmonic(cursor)
        totalFacAR = "%.2f" %totalFacAR
        totalEmpresaFac=tablaTotalEmpresaFac(cursor)
        totalEmpresaFac = "%.2f" %totalEmpresaFac
        totalPendAR=totalPendentFacArmonic(cursor)
        totalPendAR = "%.2f" %totalPendAR
        
    elif tipo== -3: # cobros         
        pissarraCobroAR = tablaPissarraCobroArmonic(cursor) 
        lenCobroAR = len(pissarraCobroAR)-1
        if lenCobroAR >= 0:
            totalCobroAR = pissarraCobroAR[lenCobroAR]
            tcobratAR= totalCobroAR.tcobrat
            totalCobAR = "%.2f" %tcobratAR
            tpendentAR = totalCobroAR.tpendent
            totalPendCobAR = "%.2f" %tpendentAR
        else:
            tcobratAR =0   
            
        #totalEmpresaCob=tcobratAR+tcobratIA+tcobratLAO
        totalEmpresaCob=tcobratAR
        totalEmpresaCob = "%.2f" %totalEmpresaCob



    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'tipo': tipo,           
             'pissarraFacAR': pissarraFacAR,
             'pissarraCobroAR': pissarraCobroAR,
             'totalFacAR': totalFacAR,
             'totalCobAR': totalCobAR,
             'totalEmpresaFac': totalEmpresaFac,
             'totalEmpresaCob': totalEmpresaCob, 
             'totalPendAR': totalPendAR,
             'totalPendCobAR': totalPendCobAR,
             'pissarraMes': pissarraMes
              }
    return values  

# ACCIONS DEL FORMULARI
####################################

                
class PissarraInicial (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                tipo = -1
            
                #obtenim valors per al html
                values = formulariPissarra(usuari, tipo)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'pissarra.html') 
                self.response.out.write(template.render(path, values,))

class PissarraFacturacio (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                tipo = -2
            
                #obtenim valors per al html
                values = formulariPissarra(usuari, tipo)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'pissarra.html') 
                self.response.out.write(template.render(path, values,))

class PissarraCobro (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                tipo = -3
            
                #obtenim valors per al html
                values = formulariPissarra(usuari, tipo)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'pissarra.html') 
                self.response.out.write(template.render(path, values,))

class SelectNoPisFact (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                tipo = -2
                enPis = 0
                idPressupost  = novar(self.request.get('idPressupost'))
                
                #accions sobre bd
                db= get_db()
                cursor = db.cursor()
                cursor.execute('UPDATE pressupostos SET enPis=%s WHERE idPressupost=%s', (enPis, idPressupost,))          
                db.commit()
                db.close()
            
                #obtenim valors per al html
                values = formulariPissarra(usuari, tipo)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'pissarra.html') 
                self.response.out.write(template.render(path, values,))

class SelectNoPisCob (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                tipo = -3
                enPis = 0
                idFactura  = novar(self.request.get('idFactura'))
                
                #accions sobre bd
                db= get_db()
                cursor = db.cursor()
                cursor.execute('UPDATE factures SET enPis=%s WHERE idFactura=%s', (enPis, idFactura,))          
                db.commit()
                db.close()
            
                #obtenim valors per al html
                values = formulariPissarra(usuari, tipo)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'pissarra.html') 
                self.response.out.write(template.render(path, values,))

class PissarraCobroMes (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                dataMes  = novar(self.request.get('dataMes'))
                tipo = -3
                dataFin=datetime.datetime.strptime(dataMes,'%Y-%m-%d')    
                an=dataFin.year
                mes=dataFin.month
        
                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
                    
                #operar en bd 
                treballadorSelect=tablaTreballadorSelect(cursor,usuari)
                iniciCapsula = tablaCapsulaUltima(cursor, usuari)
                capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
                fitxa=estatFitxa(cursor,usuari)
                
                pissarraCobroAR = tablaPissarraCobroMes(cursor, dataMes) 
                lenCobroAR = len(pissarraCobroAR)-1
                if lenCobroAR >= 0:
                    totalCobroAR = pissarraCobroAR[lenCobroAR]
                    tcobratAR= totalCobroAR.tcobrat
                    totalCobAR = "%.2f" %tcobratAR
                else:
                    tcobratAR =0 
                    totalCobAR =0
                    
                pissarraCobroAR = tablaPissarraCobroMesArmonic(cursor, dataMes)
                lenCobroAR = len(pissarraCobroAR)-1
                if lenCobroAR >= 0:
                    totalCobroAR = pissarraCobroAR[lenCobroAR]
                    tcobratAR= totalCobroAR.tcobrat
                    totalCobAR = "%.2f" %tcobratAR
                else:
                    tcobratAR =0 
                    totalCobAR =0
                     
                #totalEmpresaCob=tcobratAR+tcobratIA+tcobratLAO
                totalEmpresaCob=tcobratAR
                totalEmpresaCob = "%.2f" %totalEmpresaCob
        
                #desconectar de la bd
                db.commit()
                db.close()
            
                #pasem les llistes al arxiu html
                values = {
                         'treballadorSelect': treballadorSelect,
                         'iniciCapsula': iniciCapsula,
                         'capsula': capsula,
                         'fitxa': fitxa,
                         'tipo': tipo,
                         
                         'pissarraCobroAR': pissarraCobroAR,
                     
                         'totalCobAR': totalCobAR,
                         'totalEmpresaCob': totalEmpresaCob,
                         'an': an,
                         'mes':mes,
                          }

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'pissarra.html') 
                self.response.out.write(template.render(path, values,))
                
class PissarraFacMes (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                dataMes  = novar(self.request.get('dataMes'))
                tipo = -4
                dataFin=datetime.datetime.strptime(dataMes,'%Y-%m-%d')    
                an=dataFin.year
                mes=dataFin.month
        
                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
                    
                #operar en bd 
                treballadorSelect=tablaTreballadorSelect(cursor,usuari)
                iniciCapsula = tablaCapsulaUltima(cursor, usuari)
                capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
                fitxa=estatFitxa(cursor,usuari)
                    
                pissarraFacAR = tablaPissarraFacMes(cursor,dataMes)
                lenFacAR = len(pissarraFacAR)-1
                if lenFacAR >= 0:
                    totalAR = pissarraFacAR[lenFacAR]
                    totalNumAR= totalAR.total
                    totalFacAR = "%.2f" %totalNumAR
                else:
                    totalNumAR=0
                    totalFacAR=0
                    
                pissarraFacAR = tablaPissarraFacMesArmonic(cursor,dataMes)
                lenFacAR = len(pissarraFacAR)-1
                if lenFacAR >= 0:
                    totalAR = pissarraFacAR[lenFacAR]
                    totalNumAR= totalAR.total
                    totalFacAR = "%.2f" %totalNumAR
                else:
                    totalNumAR=0
                    totalFacAR=0
                     
                #totalEmpresaFac=totalNumLAO+totalNumIA+totalNumAR
                totalEmpresaFac=totalNumAR
                totalEmpresaFac = "%.2f" %totalEmpresaFac
        
                #desconectar de la bd
                db.commit()
                db.close()
            
                #pasem les llistes al arxiu html
                values = {
                         'treballadorSelect': treballadorSelect,
                         'iniciCapsula': iniciCapsula,
                         'capsula': capsula,
                         'fitxa': fitxa,
                         'tipo': tipo,
                         
                         'pissarraFacAR': pissarraFacAR,
                         
                         'totalFacAR': totalFacAR,
                         'totalEmpresaFac': totalEmpresaFac,
                         'an': an,
                         'mes':mes,
                          }

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'pissarra.html') 
                self.response.out.write(template.render(path, values,))

class PissarraFac (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                
                dataFin=datetime.datetime.today()
                dataFin='%d-%d-1'%(dataFin.year, dataFin.month)
                dataFin=datetime.datetime.strptime(dataFin,'%Y-%m-%d')
                tipo = -4  
                an=dataFin.year
                mes=dataFin.month
                dataMes=dataFin.strftime('%Y-%m-%d')
        
                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
                    
                #operar en bd 
                treballadorSelect=tablaTreballadorSelect(cursor,usuari)
                iniciCapsula = tablaCapsulaUltima(cursor, usuari)
                capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
                fitxa=estatFitxa(cursor,usuari)
                
                
                pissarraFacAR = tablaPissarraFacMes(cursor,dataMes)
                lenFacAR = len(pissarraFacAR)-1
                if lenFacAR >= 0:
                    totalAR = pissarraFacAR[lenFacAR]
                    totalNumAR= totalAR.total
                    totalFacAR = "%.2f" %totalNumAR
                else:
                    totalNumAR=0
                    totalFacAR=0
                   
                pissarraFacAR = tablaPissarraFacMesArmonic(cursor, dataMes)
                lenFacAR = len(pissarraFacAR)-1
                if lenFacAR >= 0:
                    totalAR = pissarraFacAR[lenFacAR]
                    totalNumAR= totalAR.total
                    totalFacAR = "%.2f" %totalNumAR
                else:
                    totalNumAR=0
                    totalFacAR=0
                     
                totalEmpresaFac=totalNumAR
                totalEmpresaFac = "%.2f" %totalEmpresaFac
        
                #desconectar de la bd
                db.commit()
                db.close()
            
                #pasem les llistes al arxiu html
                values = {
                         'treballadorSelect': treballadorSelect,
                         'iniciCapsula': iniciCapsula,
                         'capsula': capsula,
                         'fitxa': fitxa,
                         'tipo': tipo,
                         'pissarraFacAR': pissarraFacAR,
                         'totalFacAR': totalFacAR,
                         'totalEmpresaFac': totalEmpresaFac,
                         'an': an,
                         'mes':mes,
                          }

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'pissarra.html') 
                self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################

def tablaPissarraFac(cursor):
        
        #data inicial del passat
        dataIni=datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')
        
        #primer dia del mes actual
        dataFin=datetime.datetime.today()
        dataFin='%d-%d-1'%(dataFin.year, dataFin.month)
        dataFin=datetime.datetime.strptime(dataFin,'%Y-%m-%d')
        
        #hui
        ara = datetime.datetime.today()
        hui = ara.strftime('%Y-%m-%d')        
        
        cursor.execute('SELECT idPressupost, idEsquema, nomPressupost FROM pressupostos WHERE enActiu=%s AND enPis=%s', (1,1,))
        tabla = cursor.fetchall()

        conta=0
        indice=0
        for i in tabla: #conta el numero de files de la tabla
            conta=conta+1
        lista=[0]*conta #creem lista
        
        for i in tabla: #cada fila es converteix en un objecte de lista
            idPressupost = i[0]
            idEsquema = i[1]
            nom = i[2]
            #acceptat
            cursor.execute('SELECT SUM(tr.preu) AS acceptat FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost = tr.idPressupost WHERE pr.enActiu=%s AND pr.enPis=%s AND tr.acceptat=%s AND pr.idPressupost=%s',(1, 1, 1, idPressupost,))
            vector = cursor.fetchall()
            acceptat = vector[0][0]
            if acceptat:
                acceptat=int(acceptat)
            else:
                acceptat=0
            #facturat
            cursor.execute('SELECT sum(tr.preu) FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost=tr.idPressupost INNER JOIN (factures fa INNER JOIN liniesfactura lf ON fa.idFactura=lf.idFactura) ON tr.idTreball = lf.idTreball WHERE pr.idPressupost=%s AND fa.dataProforma<=%s AND fa.dataProforma>=%s AND pr.enPis=%s AND tr.acceptat=%s',(idPressupost,hui,dataFin,1,1,))
            vector = cursor.fetchall()
            facturat = vector[0][0]
            if facturat:
                facturat=int(facturat)
            else:
                facturat=0
            
            #pendent
            cursor.execute('SELECT sum(tr.preu) FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost=tr.idPressupost INNER JOIN (factures fa INNER JOIN liniesfactura lf ON fa.idFactura=lf.idFactura) ON tr.idTreball = lf.idTreball WHERE pr.idPressupost=%s AND fa.dataProforma<%s AND fa.dataProforma>%s AND pr.enPis=%s AND tr.acceptat=%s',(idPressupost,dataFin,dataIni,1,1,))
            vector = cursor.fetchall()
            anterior = vector[0][0]
            if anterior:
                anterior=int(anterior)
            else:
                anterior=0
            pendent = acceptat-facturat-anterior
            
            acceptat = "%.2f" %acceptat
            facturat = "%.2f" %facturat
            
            #color
            color = 1
   
            lista[indice] = PisFac(idPressupost, idEsquema, nom,acceptat,pendent, anterior ,facturat,color) #Modificar si anyadim columna 
            indice=indice+1  
        return lista 
    
def tablaPissarraFacArmonic(cursor):
        
        #data inicial del passat
        dataIni=datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')
        
        #primer dia del mes actual
        dataFin=datetime.datetime.today()
        dataFin='%d-%d-1'%(dataFin.year, dataFin.month)
        dataFin=datetime.datetime.strptime(dataFin,'%Y-%m-%d')
        
        #hui
        ara = datetime.datetime.today()
        hui = ara.strftime('%Y-%m-%d')        
        
        cursor.execute('SELECT idPressupost, idEsquema, nomPressupost FROM pressupostos WHERE enActiu=%s AND enPis=%s', (1,1,))
        tabla = cursor.fetchall()

        conta=0
        indice=0
        for i in tabla: #conta el numero de files de la tabla
            conta=conta+1
        lista=[0]*conta #creem lista
        
        for i in tabla: #cada fila es converteix en un objecte de lista
            idPressupost = i[0]
            idEsquema = i[1]
            nom = i[2]
            #acceptat
            cursor.execute('SELECT SUM(tr.preu) AS acceptat FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost = tr.idPressupost WHERE pr.enActiu=%s AND pr.enPis=%s AND tr.acceptat=%s AND pr.idPressupost=%s',(1, 1, 1, idPressupost,))
            vector = cursor.fetchall()
            acceptat = vector[0][0]
            if acceptat:
                acceptat=int(acceptat)
            else:
                acceptat=0
            #facturat
            cursor.execute('SELECT sum(tr.preu) FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost=tr.idPressupost INNER JOIN (factures fa INNER JOIN liniesfactura lf ON fa.idFactura=lf.idFactura) ON tr.idTreball = lf.idTreball WHERE pr.idPressupost=%s AND fa.dataProforma<=%s AND fa.dataProforma>=%s AND pr.enPis=%s AND tr.acceptat=%s',(idPressupost,hui,dataFin,1,1,))
            vector = cursor.fetchall()
            facturat = vector[0][0]
            if facturat:
                facturat=int(facturat)
            else:
                facturat=0
            
            #pendent
            cursor.execute('SELECT sum(tr.preu) FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost=tr.idPressupost INNER JOIN (factures fa INNER JOIN liniesfactura lf ON fa.idFactura=lf.idFactura) ON tr.idTreball = lf.idTreball WHERE pr.idPressupost=%s AND fa.dataProforma<%s AND fa.dataProforma>%s AND pr.enPis=%s AND tr.acceptat=%s',(idPressupost,dataFin,dataIni,1,1,))
            vector = cursor.fetchall()
            anterior = vector[0][0]
            if anterior:
                anterior=int(anterior)
            else:
                anterior=0
            pendent = acceptat-facturat-anterior
            
            acceptat = "%.2f" %acceptat
            facturat = "%.2f" %facturat
            
            #color
            color = 1
   
            lista[indice] = PisFac(idPressupost, idEsquema, nom,acceptat,pendent, anterior ,facturat,color) #Modificar si anyadim columna 
            indice=indice+1  
        return lista 
    
def totalPissarraFac(cursor):
                       
            #primer dia del mes actual
            dataFin=datetime.datetime.today()
            dataFin='%d-%d-1'%(dataFin.year, dataFin.month)
            dataFin=datetime.datetime.strptime(dataFin,'%Y-%m-%d')
            
            #hui
            ara = datetime.datetime.today()
            hui = ara.strftime('%Y-%m-%d') 
            
            cursor.execute('SELECT sum(tr.preu) FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost=tr.idPressupost INNER JOIN (factures fa INNER JOIN liniesfactura lf ON fa.idFactura=lf.idFactura) ON tr.idTreball = lf.idTreball WHERE fa.dataProforma<=%s AND fa.dataProforma>=%s AND pr.enPis=%s AND tr.acceptat=%s',(hui,dataFin,1,1,))
            vector = cursor.fetchall()
            facturat = vector[0][0]
            if facturat:
                facturat=int(facturat)
            else:
                facturat=0
            return facturat
        
        
#ARMONIC     
def totalPissarraFacArmonic(cursor):
                       
            #primer dia del mes actual
            dataFin=datetime.datetime.today()
            dataFin='%d-%d-1'%(dataFin.year, dataFin.month)
            dataFin=datetime.datetime.strptime(dataFin,'%Y-%m-%d')
            
            #hui
            ara = datetime.datetime.today()
            hui = ara.strftime('%Y-%m-%d') 
            
            cursor.execute('SELECT sum(tr.preu) FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost=tr.idPressupost INNER JOIN (factures fa INNER JOIN liniesfactura lf ON fa.idFactura=lf.idFactura) ON tr.idTreball = lf.idTreball WHERE fa.dataProforma<=%s AND fa.dataProforma>=%s AND pr.enPis=%s AND tr.acceptat=%s',(hui,dataFin,1,1,))
            vector = cursor.fetchall()
            facturat = vector[0][0]
            if facturat:
                facturat=int(facturat)
            else:
                facturat=0
            return facturat

def totalAcceptatFac(cursor):
                       
            #primer dia del mes actual
            dataFin=datetime.datetime.today()
            dataFin='%d-%d-1'%(dataFin.year, dataFin.month)
            dataFin=datetime.datetime.strptime(dataFin,'%Y-%m-%d')
            
            
            #acceptat
            cursor.execute('SELECT SUM(tr.preu) AS acceptat FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost = tr.idPressupost WHERE pr.enActiu=%s AND pr.enPis=%s AND tr.acceptat=%s',(1, 1, 1,))
            vector = cursor.fetchall()
            acceptat = vector[0][0]
            if acceptat:
                acceptat=int(acceptat)
            else:
                acceptat=0
            return acceptat

def totalAnteriorFac(cursor):
                       
            #data inicial del passat
            dataIni=datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')
            #primer dia del mes actual
            dataFin=datetime.datetime.today()
            dataFin='%d-%d-1'%(dataFin.year, dataFin.month)
            dataFin=datetime.datetime.strptime(dataFin,'%Y-%m-%d')

            cursor.execute('SELECT sum(tr.preu) FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost=tr.idPressupost INNER JOIN (factures fa INNER JOIN liniesfactura lf ON fa.idFactura=lf.idFactura) ON tr.idTreball = lf.idTreball WHERE fa.dataProforma<%s AND fa.dataProforma>%s AND pr.enPis=%s AND tr.acceptat=%s',(dataFin,dataIni,1,1,))
            vector = cursor.fetchall()
            anterior = vector[0][0]
            if anterior:
                anterior=int(anterior)
            else:
                anterior=0
            return anterior

def totalPendentFac(cursor):
            
            acceptat = totalAcceptatFac(cursor)
            facturat = totalPissarraFac(cursor)
            anterior = totalAnteriorFac(cursor)
                       
            pendent = acceptat-facturat-anterior
            return pendent

def totalPendentFacArmonic(cursor):
            
            acceptat = totalAcceptatFac(cursor)
            facturat = totalPissarraFac(cursor)
            anterior = totalAnteriorFac(cursor)
                       
            pendent = acceptat-facturat-anterior
            return pendent


# cobros
def tablaPissarraCobro(cursor):
        
        #data inicial del passat
        dataIni=datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')
        
        #primer dia del mes actual
        dataFin=datetime.datetime.today()
        dataFin='%d-%d-1'%(dataFin.year, dataFin.month)
        dataFin=datetime.datetime.strptime(dataFin,'%Y-%m-%d')
                
        
        cursor.execute('SELECT es.idEsquema, fa.idFactura, es.nomExpedient, fa.proforma, fa.dataCobro FROM esquemes es INNER JOIN factures fa ON es.idEsquema = fa.idEsquema WHERE fa.enPis=%s AND fa.dataCobro IS NULL OR fa.enPis=%s AND fa.dataCobro>=%s OR fa.enPis=%s AND fa.dataCobro<%s', (1,1,dataFin,1,'1900-01-01',))
        tabla = cursor.fetchall()

        conta=0
        indice=0
        tcobrat=0
        tpendent=0
        tanterior=0
        tsuplido=0
        
        for i in tabla: #conta el numero de files de la tabla
            conta=conta+1
        lista=[0]*conta #creem lista
        
        for i in tabla: #cada fila es converteix en un objecte de lista
            idFactura = i[1]
            idEsquema = i[0]
            nom = i[2]
            proforma= i[3]
            dataCobro=dataFormat(i[4])
            #facturat
            cursor.execute('SELECT SUM(tr.preu) FROM factures fa INNER JOIN (treballs tr INNER JOIN liniesfactura lf ON tr.idTreball = lf.idTreball) ON fa.idFactura=lf.idFactura WHERE (fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro IS NULL) OR (fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro>=%s) OR (fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro<%s)',(idFactura, 1, idFactura, 1,dataFin, idFactura, 1,'1900-01-01',))
            vector = cursor.fetchall()
            facturat = vector[0][0]
            if facturat:
                facturat=facturat
            else:
                facturat=0
                
            #suplido
            cursor.execute('SELECT SUM(ls.preuSuplido) FROM liniessuplidos ls LEFT JOIN (factures fa INNER JOIN (treballs tr INNER JOIN liniesfactura lf ON tr.idTreball = lf.idTreball) ON fa.idFactura=lf.idFactura) ON ls.idFactura=fa.idFactura WHERE ((fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro IS NULL) OR (fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro>=%s) OR (fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro<%s))',(idFactura, 1, idFactura, 1,dataFin, idFactura, 1,'1900-01-01'))
            vector = cursor.fetchall()
            suplido = vector[0][0]
            if suplido:
                suplido=suplido
            else:
                suplido=0
            
            #cobrat
            cursor.execute('SELECT sum(quantitat) FROM moviments WHERE idFactura=%s AND dataMov>=%s',(idFactura, dataFin,))
            vector = cursor.fetchall()
            cobrat  = vector[0][0]
            
            if cobrat:
                cobrat=int(cobrat)
                cursor.execute('SELECT dataFactura FROM factures WHERE idFactura=%s',(idFactura,))
                vector = cursor.fetchall()
                data  = vector[0][0]
                dataFactura=dataFormat(data)
                dataIni=dataFormat(dataIni)
                if dataFactura>dataIni:
                    factura=1
                else:
                    factura = 0
            else:
                cobrat=0
                factura=0
        
                
            if factura >0:
                #obtenir tipo IVA
                cursor.execute('SELECT tipoIVA FROM constants WHERE idConstant=%s',(1,))
                tTipoIVA = cursor.fetchall()
                try:
                    tipoIVA = tTipoIVA [0] [0]
                except:
                    tipoIVA = 0
                    
                if suplido == 0:
                    cobrat = cobrat/(1+tipoIVA)
                else:
                    cobrat = (cobrat-suplido)/(1+tipoIVA)

            #anterior
            cursor.execute('SELECT sum(quantitat) FROM moviments WHERE idFactura=%s AND dataMov<%s AND dataMov>%s',(idFactura, dataFin, dataIni,))
            vector = cursor.fetchall()
            anterior = vector[0][0]
            if anterior:
                anterior=anterior
            else:
                anterior=0
                
            

            pendent = facturat-cobrat-anterior
 

                

            #totals
            tcobrat = tcobrat+cobrat
            tanterior = tanterior+anterior
            tpendent = tpendent+pendent
            tsuplido = tsuplido+suplido
            if pendent < 1: #redondeja a pagat si la diferencia son centims
                pendent=0
                
            npendent=pendent
            
            cobrat = "%.2f" %cobrat
            facturat = "%.2f" %facturat
            pendent = "%.2f" %pendent
            anterior = "%.2f" %anterior
            suplido = "%.2f" %suplido


            lista[indice] = PisCob(idFactura, idEsquema, nom, proforma, facturat, cobrat, pendent, anterior, suplido, dataCobro, tcobrat, tpendent, tanterior, tsuplido, npendent) #Modificar si anyadim columna 
            indice=indice+1  
            
        return lista 

def tablaPissarraCobroArmonic(cursor):
        
        #data inicial del passat
        dataIni=datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')
        
        #primer dia del mes actual
        dataFin=datetime.datetime.today()
        dataFin='%d-%d-1'%(dataFin.year, dataFin.month)
        dataFin=datetime.datetime.strptime(dataFin,'%Y-%m-%d')
                
        
        cursor.execute('SELECT es.idEsquema, fa.idFactura, es.nomExpedient, fa.proforma, fa.dataCobro FROM esquemes es INNER JOIN factures fa ON es.idEsquema = fa.idEsquema WHERE fa.enPis=%s AND fa.dataCobro IS NULL  OR fa.enPis=%s AND fa.dataCobro>=%s  OR fa.enPis=%s AND fa.dataCobro<%s', (1,1,dataFin,1,'1900-01-01'))
        tabla = cursor.fetchall()

        conta=0
        indice=0
        tcobrat=0
        tpendent=0
        tanterior=0
        tsuplido=0
        
        for i in tabla: #conta el numero de files de la tabla
            conta=conta+1
        lista=[0]*conta #creem lista
        
        for i in tabla: #cada fila es converteix en un objecte de lista
            idFactura = i[1]
            idEsquema = i[0]
            nom = i[2]
            proforma= i[3]
            dataCobro=dataFormat(i[4])
            #facturat
            cursor.execute('SELECT SUM(tr.preu) AS preuLF FROM treballs tr INNER JOIN liniesfactura lf ON tr.idTreball=lf.idTreball GROUP BY lf.idFactura HAVING lf.idFactura=%s',(idFactura,))
            vector = cursor.fetchall()
            try:
                facturat = vector[0][0]
            except:
                facturat=0
                
            #suplido
            cursor.execute('SELECT SUM(preuSuplido) AS preuLS FROM liniessuplidos GROUP BY idFactura HAVING idFactura=%s',(idFactura,))
            vector = cursor.fetchall()
            try:
                suplido = vector[0][0]
            except:
                suplido=0
            
            #cobrat
            cursor.execute('SELECT sum(quantitat) FROM moviments WHERE idFactura=%s AND dataMov>=%s',(idFactura, dataFin))
            vector = cursor.fetchall()
            cobrat  = vector[0][0]
            
            if cobrat:
                cobrat=int(cobrat)
                cursor.execute('SELECT dataFactura FROM factures WHERE idFactura=%s',(idFactura,))
                vector = cursor.fetchall()
                data  = vector[0][0]
                dataFactura=dataFormat(data)
                dataIni=dataFormat(dataIni)
                if dataFactura>dataIni:
                    factura=1
                else:
                    factura = 0
            else:
                cobrat=0
                factura=0
        
                
            if factura >0:
                #obtenir tipo IVA
                cursor.execute('SELECT tipoIVA FROM constants WHERE idConstant=%s',(1,))
                tTipoIVA = cursor.fetchall()
                try:
                    tipoIVA = tTipoIVA [0] [0]
                except:
                    tipoIVA = 0
                    
                if suplido == 0:
                    cobrat = cobrat/(1+tipoIVA)
                else:
                    cobrat = (cobrat-suplido)/(1+tipoIVA)

            #anterior
            cursor.execute('SELECT sum(quantitat) FROM moviments WHERE idFactura=%s AND dataMov<%s AND dataMov>%s',(idFactura, dataFin, dataIni))
            vector = cursor.fetchall()
            anterior = vector[0][0]
            if anterior:
                anterior=anterior
            else:
                anterior=0
                
            

            pendent = facturat-cobrat-anterior
 

                

            #totals
            tcobrat = tcobrat+cobrat
            tanterior = tanterior+anterior
            tpendent = tpendent+pendent
            tsuplido = tsuplido+suplido
            if pendent < 1: #redondeja a pagat si la diferencia son centims
                pendent=0
                
            npendent=pendent
            
            cobrat = "%.2f" %cobrat
            facturat = "%.2f" %facturat
            pendent = "%.2f" %pendent
            anterior = "%.2f" %anterior
            suplido = "%.2f" %suplido


            lista[indice] = PisCob(idFactura, idEsquema, nom, proforma, facturat, cobrat, pendent, anterior, suplido, dataCobro, tcobrat, tpendent, tanterior, tsuplido, npendent) #Modificar si anyadim columna 
            indice=indice+1  
            
        return lista 


def tablaTotalEmpresaFac(cursor):
    tlaofi=totalPissarraFac(cursor,1)
    tantrom=totalPissarraFac(cursor,2)
    tarmonic=totalPissarraFac(cursor,3)
    totalFac=tlaofi+tantrom+tarmonic
    return totalFac

        
class PisFac:
    def __init__(self, idPressupost=0, idEsquema=0, nom=0, acceptat=0, pendent=0, anterior=0, facturat=0, color=0):
        self.idPressupost = idPressupost
        self.idEsquema= idEsquema
        self.nom = nom
        self.acceptat = acceptat
        self.pendent = pendent
        self.anterior = anterior
        self.facturat = facturat
        self.color = color
class PisCob:
    def __init__(self, idFactura=0, idEsquema=0, nom=0, proforma=0, facturat=0, cobrat=0, pendent=0, anterior=0, suplido=0, dataCobro=0, tcobrat=0, tpendent=0, tanterior=0, tsuplido=0, npendent=0):
        self.idFactura = idFactura
        self.idEsquema= idEsquema
        self.nom = nom
        self.proforma = proforma
        self.facturat = facturat
        self.cobrat = cobrat
        self.pendent = pendent
        self.anterior = anterior
        self.suplido = suplido
        self.dataCobro = dataCobro
        self.tcobrat = tcobrat
        self.tpendent = tpendent
        self.tanterior = tanterior
        self.tsuplido = tsuplido
        self.npendent = npendent
        

def tablaPissarraMes(cursor):
    data=datetime.datetime.strptime('2017-12-01', '%Y-%m-%d') #data inicial
    dataFin=datetime.datetime.today()
    dataFin='%d-%d-1'%(dataFin.year, dataFin.month)
    dataFin=datetime.datetime.strptime(dataFin,'%Y-%m-%d') #primer dia del mes actual
    conta=0
    while data<dataFin: #conta numero de files de la tabla, (numero de mesos)
        data=data+datetime.timedelta(days=32)
        data='%d-%d-1'%(data.year, data.month)
        data=datetime.datetime.strptime(data,'%Y-%m-%d')
        conta=conta+1
    lista=[0]*conta
    data=datetime.datetime.strptime('2017-12-01', '%Y-%m-%d') #data inicial
    indice=0

    #decrementa dataFin un mes
    dataFin=dataFin-datetime.timedelta(days=27)
    dataFin='%d-%d-1'%(dataFin.year, dataFin.month)
    dataFin=datetime.datetime.strptime(dataFin,'%Y-%m-%d')    

    while dataFin>=data:
        an=dataFin.year
        mes=dataFin.month
        dataMes='%d-%d-1'%(dataFin.year, dataFin.month)
        
        #cobrat
        
        pissarraCobroARMes=tablaPissarraCobroMes(cursor,dataMes)
        lenCobroAR = len(pissarraCobroARMes)-1
        if lenCobroAR >= 0:
            totalCobroAR = pissarraCobroARMes[lenCobroAR]
            tcobratAR= totalCobroAR.tcobrat
        else:
            tcobratAR=0
            
        
        pissarraCobroARMes=tablaPissarraCobroMesArmonic(cursor, dataMes)
        lenCobroAR = len(pissarraCobroARMes)-1
        if lenCobroAR >= 0:
            totalCobroAR = pissarraCobroARMes[lenCobroAR]
            tcobratAR= totalCobroAR.tcobrat
        else:
            tcobratAR=0  
            
        cobroARMes=tcobratAR
        #cobroARMes=tcobratAR+tcobratIA
        
        
        cobroMes = cobroARMes
        
        #facturat
        
        
        pissarraFacARMes=tablaPissarraFacMesArmonic(cursor, dataMes)
        lenFacAR = len(pissarraFacARMes)-1
        if lenFacAR >= 0:
            totalFacAR = pissarraFacARMes[lenFacAR]
            tfacAR= totalFacAR.total
        else:
            tfacAR=0

        facARMes=tfacAR 
        
        facMes = facARMes
        
        #decrementa dataFin un mes
        dataFin=dataFin-datetime.timedelta(days=27)
        dataFin='%d-%d-1'%(dataFin.year, dataFin.month)
        dataFin=datetime.datetime.strptime(dataFin,'%Y-%m-%d')    
        
        #pasa a tabla
        cobroMes = "%.2f" %cobroMes
        cobroARMes = "%.2f" %cobroARMes
        facMes = "%.2f" %facMes
        facARMes = "%.2f" %facARMes

        lista[indice]= PissarraMes(dataMes,an,mes,cobroARMes, cobroMes, facARMes, facMes)
        indice = indice+1
    return lista 

class PissarraMes:
    def __init__(self, dataMes=0, an=0, mes=0, cobroARMes=0, cobroMes=0, facARMes=0, facMes=0):
        self.dataMes = dataMes
        self.an= an
        self.mes = mes
        self.cobroARMes = cobroARMes
        self.cobroMes = cobroMes
        self.facARMes = facARMes
        self.facMes = facMes

#meses anteriores 
def tablaPissarraCobroMes(cursor, dataMes):
        
        #data inicial del passat
        dataIni=datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')
        
        #dataMes: primer dia del mes a calcular
        dataMes=datetime.datetime.strptime(dataMes,'%Y-%m-%d')   
        
        #incrementa dataMes un mes
        
        dataSeg=dataMes+datetime.timedelta(days=32)
        dataSeg='%d-%d-1'%(dataSeg.year, dataSeg.month)
        dataSeg=datetime.datetime.strptime(dataSeg,'%Y-%m-%d')   
                
        
        cursor.execute('SELECT es.idEsquema, fa.idFactura, es.nomExpedient, fa.proforma, fa.dataCobro FROM esquemes es INNER JOIN factures fa ON es.idEsquema = fa.idEsquema INNER JOIN moviments mo ON mo.idFactura=fa.idFactura WHERE fa.enPis=%s AND mo.dataMov>=%s AND mo.dataMov<%s', (1, dataMes, dataSeg,))
        tabla = cursor.fetchall()

        conta=0
        indice=0
        tcobrat=0
        tpendent=0
        tanterior=0
        tsuplido=0
        
        for i in tabla: #conta el numero de files de la tabla
            conta=conta+1
        lista=[0]*conta #creem lista
        
        for i in tabla: #cada fila es converteix en un objecte de lista
            idFactura = i[1]
            idEsquema = i[0]
            nom = i[2]
            proforma= i[3]
            dataCobro=dataFormat(i[4])
            #facturat
            cursor.execute('SELECT SUM(tr.preu) FROM factures fa INNER JOIN (treballs tr INNER JOIN liniesfactura lf ON tr.idTreball = lf.idTreball) ON fa.idFactura=lf.idFactura WHERE fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro>=%s AND fa.dataCobro<%s',(idFactura, 1, dataMes, dataSeg,))
            vector = cursor.fetchall()
            facturat = vector[0][0]
            if facturat:
                facturat=facturat
            else:
                facturat=0
                
            #suplido
            cursor.execute('SELECT SUM(ls.preuSuplido) FROM liniessuplidos ls LEFT JOIN factures fa ON ls.idFactura=fa.idFactura WHERE fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro>=%s AND fa.dataCobro<%s',(idFactura, 1,dataMes,dataSeg,))
            vector = cursor.fetchall()
            suplido = vector[0][0]
            if suplido:
                suplido=suplido
            else:
                suplido=0
            
            #cobrat
            cursor.execute('SELECT sum(quantitat) FROM moviments WHERE idFactura=%s AND dataMov>=%s AND dataMov<%s',(idFactura, dataMes, dataSeg,))
            vector = cursor.fetchall()
            cobrat  = vector[0][0]
            
            if cobrat:
                cobrat=int(cobrat)
                cursor.execute('SELECT dataFactura FROM factures WHERE idFactura=%s',(idFactura,))
                vector = cursor.fetchall()
                data  = vector[0][0]
                dataFactura=dataFormat(data)
                dataIni=dataFormat(dataIni)
                if dataFactura>dataIni:
                    factura=1
                else:
                    factura = 0
            else:
                cobrat=0
                factura=0
        
                
            if factura >0:
                #obtenir tipo IVA
                cursor.execute('SELECT tipoIVA FROM constants WHERE idConstant=%s',(1,))
                tTipoIVA = cursor.fetchall()
                try:
                    tipoIVA = tTipoIVA [0] [0]
                except:
                    tipoIVA = 0
                    
                if suplido == 0:
                    cobrat = cobrat/(1+tipoIVA)
                else:
                    cobrat = (cobrat-suplido)/(1+tipoIVA)

            #anterior
            cursor.execute('SELECT sum(quantitat) FROM moviments WHERE idFactura=%s AND dataMov<=%s AND dataMov>%s',(idFactura, dataMes, dataIni,))
            vector = cursor.fetchall()
            anterior = vector[0][0]
            if anterior:
                anterior=anterior
            else:
                anterior=0
                
            

            pendent = facturat-cobrat-anterior
 

                

            #totals
            tcobrat = tcobrat+cobrat
            tanterior = tanterior+anterior
            tpendent = tpendent+pendent
            tsuplido = tsuplido+suplido
            if pendent < 1: #redondeja a pagat si la diferencia son centims
                pendent=0
                
            npendent=-1
            
            cobrat = "%.2f" %cobrat
            facturat = "%.2f" %facturat
            pendent = "%.2f" %pendent
            anterior = "%.2f" %anterior
            suplido = "%.2f" %suplido


            lista[indice] = PisCob(idFactura, idEsquema, nom, proforma, facturat, cobrat, pendent, anterior, suplido, dataCobro, tcobrat, tpendent, tanterior, tsuplido, npendent) #Modificar si anyadim columna 
            indice=indice+1  
            
        return lista 
    
    
def tablaPissarraCobroMesArmonic(cursor, dataMes):
        
        #data inicial del passat
        dataIni=datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')
        
        #dataMes: primer dia del mes a calcular
        dataMes=datetime.datetime.strptime(dataMes,'%Y-%m-%d')   
        
        #incrementa dataMes un mes
        
        dataSeg=dataMes+datetime.timedelta(days=32)
        dataSeg='%d-%d-1'%(dataSeg.year, dataSeg.month)
        dataSeg=datetime.datetime.strptime(dataSeg,'%Y-%m-%d')   
                
        
        cursor.execute('SELECT es.idEsquema, fa.idFactura, es.nomExpedient, fa.proforma, fa.dataCobro FROM esquemes es INNER JOIN factures fa ON es.idEsquema = fa.idEsquema INNER JOIN moviments mo ON mo.idFactura=fa.idFactura WHERE fa.enPis=%s AND mo.dataMov>=%s AND mo.dataMov<%s', (1, dataMes, dataSeg,))
        tabla = cursor.fetchall()

        conta=0
        indice=0
        tcobrat=0
        tpendent=0
        tanterior=0
        tsuplido=0
        
        for i in tabla: #conta el numero de files de la tabla
            conta=conta+1
        lista=[0]*conta #creem lista
        
        for i in tabla: #cada fila es converteix en un objecte de lista
            idFactura = i[1]
            idEsquema = i[0]
            nom = i[2]
            proforma= i[3]
            dataCobro=dataFormat(i[4])
            #facturat
            cursor.execute('SELECT SUM(tr.preu) FROM factures fa INNER JOIN (treballs tr INNER JOIN liniesfactura lf ON tr.idTreball = lf.idTreball) ON fa.idFactura=lf.idFactura WHERE fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro>=%s AND fa.dataCobro<%s',(idFactura, 1, dataMes, dataSeg,))
            vector = cursor.fetchall()
            facturat = vector[0][0]
            if facturat:
                facturat=facturat
            else:
                facturat=0
                
            #suplido
            cursor.execute('SELECT SUM(ls.preuSuplido) FROM liniessuplidos ls LEFT JOIN factures fa ON ls.idFactura=fa.idFactura WHERE fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro>=%s AND fa.dataCobro<%s ',(idFactura, 1,dataMes,dataSeg,))
            vector = cursor.fetchall()
            suplido = vector[0][0]
            if suplido:
                suplido=suplido
            else:
                suplido=0
            
            #cobrat
            cursor.execute('SELECT sum(quantitat) FROM moviments WHERE idFactura=%s AND dataMov>=%s AND dataMov<%s',(idFactura, dataMes, dataSeg,))
            vector = cursor.fetchall()
            cobrat  = vector[0][0]
            
            if cobrat:
                cobrat=int(cobrat)
                cursor.execute('SELECT dataFactura FROM factures WHERE idFactura=%s',(idFactura,))
                vector = cursor.fetchall()
                data  = vector[0][0]
                dataFactura=dataFormat(data)
                dataIni=dataFormat(dataIni)
                if dataFactura>dataIni:
                    factura=1
                else:
                    factura = 0
            else:
                cobrat=0
                factura=0
        
                
            if factura >0:
                #obtenir tipo IVA
                cursor.execute('SELECT tipoIVA FROM constants WHERE idConstant=%s',(1,))
                tTipoIVA = cursor.fetchall()
                try:
                    tipoIVA = tTipoIVA [0] [0]
                except:
                    tipoIVA = 0
                    
                if suplido == 0:
                    cobrat = cobrat/(1+tipoIVA)
                else:
                    cobrat = (cobrat-suplido)/(1+tipoIVA)

            #anterior
            cursor.execute('SELECT sum(quantitat) FROM moviments WHERE idFactura=%s AND dataMov<=%s AND dataMov>%s',(idFactura, dataMes, dataIni,))
            vector = cursor.fetchall()
            anterior = vector[0][0]
            if anterior:
                anterior=anterior
            else:
                anterior=0
                
            

            pendent = facturat-cobrat-anterior
 

                

            #totals
            tcobrat = tcobrat+cobrat
            tanterior = tanterior+anterior
            tpendent = tpendent+pendent
            tsuplido = tsuplido+suplido
            if pendent < 1: #redondeja a pagat si la diferencia son centims
                pendent=0
                
            npendent=-1
            
            cobrat = "%.2f" %cobrat
            facturat = "%.2f" %facturat
            pendent = "%.2f" %pendent
            anterior = "%.2f" %anterior
            suplido = "%.2f" %suplido


            lista[indice] = PisCob(idFactura, idEsquema, nom, proforma, facturat, cobrat, pendent, anterior, suplido, dataCobro, tcobrat, tpendent, tanterior, tsuplido, npendent) #Modificar si anyadim columna 
            indice=indice+1  
            
        return lista 

    
def tablaPissarraFacMes(cursor, dataMes):
        
        
        #dataMes: primer dia del mes a calcular
        dataMes=datetime.datetime.strptime(dataMes,'%Y-%m-%d')   
        
        #incrementa dataMes un mes
        
        dataSeg=dataMes+datetime.timedelta(days=32)
        dataSeg='%d-%d-1'%(dataSeg.year, dataSeg.month)
        dataSeg=datetime.datetime.strptime(dataSeg,'%Y-%m-%d')   
        
        
        cursor.execute('SELECT fa.idFactura, fa.proforma, fa.factura, fa.dataCobro, es.numExpedient, es.nomExpedient, sum(tr.preu) FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost=tr.idPressupost INNER JOIN (esquemes es INNER JOIN factures fa ON es.idEsquema=fa.idEsquema INNER JOIN liniesfactura lf ON lf.idFactura=fa.idFactura) ON tr.idTreball=lf.idTreball WHERE fa.dataProforma>=%s AND fa.dataProforma<%s AND pr.enActiu=%s AND fa.proforma>%s AND fa.enPis=%s group by fa.idFactura', (dataMes, dataSeg, 1, 0, 1,))
        tabla = cursor.fetchall()

        conta=0
        indice=0
        total=0
        for i in tabla: #conta el numero de files de la tabla
            conta=conta+1
        lista=[0]*conta #creem lista
        
        for i in tabla: #cada fila es converteix en un objecte de lista
            preu = i[6]
            dataCobro = dataFormat(i[3])
            total = total + preu
            cpreu = "%.2f" %preu
   
            lista[indice] = PisFacMes(i[0], i[1], i[2],dataCobro,i[4], i[5] ,i[6],total,cpreu) #Modificar si anyadim columna 
            indice=indice+1  
        return lista 
    

    
def tablaPissarraFacMesArmonic(cursor, dataMes):
        
        
        #dataMes: primer dia del mes a calcular
        dataMes=datetime.datetime.strptime(dataMes,'%Y-%m-%d')   
        
        #incrementa dataMes un mes
        
        dataSeg=dataMes+datetime.timedelta(days=32)
        dataSeg='%d-%d-1'%(dataSeg.year, dataSeg.month)
        dataSeg=datetime.datetime.strptime(dataSeg,'%Y-%m-%d')   
        
        
        cursor.execute('SELECT fa.idFactura, fa.proforma, fa.factura, fa.dataCobro, es.numExpedient, es.nomExpedient, sum(tr.preu) FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost=tr.idPressupost INNER JOIN (esquemes es INNER JOIN factures fa ON es.idEsquema=fa.idEsquema INNER JOIN liniesfactura lf ON lf.idFactura=fa.idFactura) ON tr.idTreball=lf.idTreball WHERE fa.dataProforma>=%s AND fa.dataProforma<%s AND pr.enActiu=%s AND fa.proforma>%s AND fa.enPis=%s group by fa.idFactura', (dataMes, dataSeg, 1, 0, 1,))
        tabla = cursor.fetchall()

        conta=0
        indice=0
        total=0
        for i in tabla: #conta el numero de files de la tabla
            conta=conta+1
        lista=[0]*conta #creem lista
        
        for i in tabla: #cada fila es converteix en un objecte de lista
            preu = i[6]
            dataCobro = dataFormat(i[3])
            total = total + preu
            cpreu = "%.2f" %preu
   
            lista[indice] = PisFacMes(i[0], i[1], i[2],dataCobro,i[4], i[5] ,i[6],total,cpreu) #Modificar si anyadim columna 
            indice=indice+1  
        return lista     
    
class PisFacMes:
    def __init__(self, idFactura=0, proforma=0, factura=0, dataCobro=0, numExpedient=0, nomExpedient=0, preu=0, total=0, cpreu=0):
        self.idFactura = idFactura
        self.proforma= proforma
        self.factura = factura
        self.dataCobro = dataCobro
        self.numExpedient = numExpedient
        self.nomExpedient = nomExpedient
        self.preu = preu
        self.total=total
        self.cpreu=cpreu


###########################################################################################################################################################
# COMISSIONS           COMISSIONS           COMISSIONS           COMISSIONS           COMISSIONS           COMISSIONS           COMISSIONS           COMISSIONS
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariComi (usuari, idIntermediari):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    intermediariComiSelect=''
  
    if idIntermediari == -1: #elegir
        intermediariComi=tablaIntermediariComi(cursor)


    else: # select
        intermediariComiSelect = tablaIntermediariComiSelect(cursor, idIntermediari)
        intermediariComi=tablaIntermediariComi(cursor)
        
 

    
    #desconectar de la bd
    db.commit()
    db.close()


    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'idIntermediari': idIntermediari,
             'intermediariComi': intermediariComi,
             'intermediariComiSelect': intermediariComiSelect,

              }
    return values  

# ACCIONS DEL FORMULARI
####################################

                
class ComiInicial (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idIntermediari = -1
            
                #obtenim valors per al html
                values = formulariComi(usuari, idIntermediari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'comi.html') 
                self.response.out.write(template.render(path, values,))
                
class IntermediariComiSelect (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idIntermediari  = novar(self.request.get('idIntermediari'))
            
                #obtenim valors per al html
                values = formulariComi(usuari, idIntermediari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'comi.html') 
                self.response.out.write(template.render(path, values,))

class IntermediariComiSol (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idIntermediari  = novar(self.request.get('idIntermediari'))
                idFactura  = novar(self.request.get('idFactura'))
                facComisSol = novar(self.request.get('facComisSol'))
                facComisSol = int(facComisSol)
                
                if facComisSol !=1:
                    #accions sobre bd
                    db= get_db()
                    cursor = db.cursor()
                    cursor.execute('UPDATE factures SET facComisSol=%s WHERE idFactura=%s', (1,idFactura,))          
                    db.commit()
                    db.close()
                else:
                    #accions sobre bd
                    db= get_db()
                    cursor = db.cursor()
                    cursor.execute('UPDATE factures SET facComisSol=%s WHERE idFactura=%s', (0,idFactura,))          
                    db.commit()
                    db.close()
                    
            
                #obtenim valors per al html
                values = formulariComi(usuari, idIntermediari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'comi.html') 
                self.response.out.write(template.render(path, values,))

class IntermediariComiPagada (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idIntermediari  = novar(self.request.get('idIntermediari'))
                idFactura  = novar(self.request.get('idFactura'))
                comisPagada = novar(self.request.get('comisPagada'))
                comisPagada = int(comisPagada)
                
                if comisPagada !=1:
                    #accions sobre bd
                    db= get_db()
                    cursor = db.cursor()
                    cursor.execute('UPDATE factures SET comisPagada=%s WHERE idFactura=%s', (1,idFactura,))          
                    db.commit()
                    db.close()
                else:
                    #accions sobre bd
                    db= get_db()
                    cursor = db.cursor()
                    cursor.execute('UPDATE factures SET comisPagada=%s WHERE idFactura=%s', (0,idFactura,))          
                    db.commit()
                    db.close()
                    
            
                #obtenim valors per al html
                values = formulariComi(usuari, idIntermediari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'comi.html') 
                self.response.out.write(template.render(path, values,))

class IntermediariComiElimina (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idIntermediari  = novar(self.request.get('idIntermediari'))
                idFactura  = novar(self.request.get('idFactura'))
                

                #accions sobre bd
                db= get_db()
                cursor = db.cursor()
                cursor.execute('UPDATE factures SET sobre=%s WHERE idFactura=%s', (1,idFactura,))          
                db.commit()
                db.close()
                    
            
                #obtenim valors per al html
                values = formulariComi(usuari, idIntermediari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'comi.html') 
                self.response.out.write(template.render(path, values,))
                

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################

def tablaIntermediariComi(cursor):
        
        #data inicial del passat
        dataIni=datetime.datetime.strptime('2017-01-01', '%Y-%m-%d')
             
        
        cursor.execute('SELECT it.idIntermediari, it.identificador FROM treballs tr INNER JOIN (intermediaris it INNER JOIN esquemes es ON it.idIntermediari=es.idIntermediari INNER JOIN  factures fa ON fa.idEsquema=es.idEsquema INNER JOIN liniesfactura lf ON fa.idFactura=lf.idFactura) ON tr.idTreball=lf.idTreball WHERE fa.dataCobro>%s AND it.comis=%s AND fa.comisPagada!=%s AND fa.sobre!=%s OR fa.dataCobro>%s AND it.comis=%s AND fa.comisPagada!=%s AND fa.sobre IS NULL GROUP BY it.identificador',(dataIni, 1,1,1,dataIni, 1,1,))
        tabla = cursor.fetchall()

        conta=0
        indice=0
        for i in tabla: #conta el numero de files de la tabla
            conta=conta+1
        lista=[0]*conta #creem lista
        
        for i in tabla: #cada fila es converteix en un objecte de lista
            idIntermediari = i[0]
            identificador = i[1]
            cursor.execute('SELECT it.idIntermediari,cl.nomClient, sum(tr.preu), fa.idFactura, fa.facComisSol, fa.comisPagada FROM clients cl INNER JOIN (treballs tr INNER JOIN (intermediaris it INNER JOIN esquemes es ON it.idIntermediari=es.idIntermediari INNER JOIN  factures fa ON fa.idEsquema=es.idEsquema INNER JOIN liniesfactura lf ON fa.idFactura=lf.idFactura) ON tr.idTreball=lf.idTreball) ON cl.idClient=fa.idClient WHERE fa.dataCobro>%s AND it.comis=%s AND it.idIntermediari=%s AND fa.sobre!=%s  AND fa.comisPagada!=%s OR fa.dataCobro>%s AND it.comis=%s AND it.idIntermediari=%s AND fa.sobre IS NULL AND fa.comisPagada!=%s GROUP BY cl.nomClient',(dataIni,1,idIntermediari,1,1,dataIni,1,idIntermediari,1,))
            vector = cursor.fetchall()

            baseComis=0
            
            for j in vector: #cada fila es converteix en un objecte de lista
                baseComisC = j[2]
                baseComis = baseComis + baseComisC
            
            
            comis=baseComis/10

            lista[indice] = IntermediariComi(idIntermediari, identificador, comis) #Modificar si anyadim columna 
            indice=indice+1  
            
        return lista 

def tablaIntermediariComiSelect(cursor,idIntermediari):
        
        #data inicial del passat
        dataIni=datetime.datetime.strptime('2017-01-01', '%Y-%m-%d')
             
        
        cursor.execute('SELECT it.idIntermediari,cl.nomClient, sum(tr.preu), fa.idFactura, fa.facComisSol, fa.comisPagada, fa.proforma, es.idEsquema FROM clients cl INNER JOIN (treballs tr INNER JOIN (intermediaris it INNER JOIN esquemes es ON it.idIntermediari=es.idIntermediari INNER JOIN  factures fa ON fa.idEsquema=es.idEsquema INNER JOIN liniesfactura lf ON fa.idFactura=lf.idFactura) ON tr.idTreball=lf.idTreball) ON cl.idClient=fa.idClient WHERE fa.dataCobro>%s AND it.comis=%s AND it.idIntermediari=%s AND fa.sobre!=%s OR fa.dataCobro>%s AND it.comis=%s AND it.idIntermediari=%s AND fa.sobre IS NULL GROUP BY fa.idFactura ORDER BY cl.nomClient',(dataIni,1,idIntermediari,1,dataIni,1,idIntermediari,))
        tabla = cursor.fetchall()

        conta=0
        indice=0
        for i in tabla: #conta el numero de files de la tabla
            conta=conta+1
        lista=[0]*conta #creem lista
        
        for i in tabla: #cada fila es converteix en un objecte de lista
            idIntermediari = i[0]
            nomClient = i[1]
            baseComis = i[2]
            comis=baseComis/10
            idFactura = i[3]
            facComisSol = i[4]
            comisPagada = i[5]
            proforma = i[6]
            idEsquema = i[7]

            lista[indice] = InterComiSelect(idIntermediari, nomClient, comis,idFactura,facComisSol, comisPagada, proforma, idEsquema) #Modificar si anyadim columna 
            indice=indice+1  
            
        return lista 
    
    
# CLASSES
####################################
class IntermediariComi:
    def __init__(self, idIntermediari=0, identificador=0, comis=0):
        self.idIntermediari = idIntermediari
        self.identificador= identificador
        self.comis = comis

class InterComiSelect:
    def __init__(self, idIntermediari=0, nomClient=0, comis=0, idFactura=0, facComisSol=0, comisPagada=0, proforma=0, idEsquema=0):
        self.idIntermediari = idIntermediari
        self.nomClient= nomClient
        self.comis = comis
        self.idFactura = idFactura
        self.facComisSol = facComisSol
        self.comisPagada = comisPagada
        self.proforma=proforma
        self.idEsquema=idEsquema

###########################################################################################################################################################
# PROFORMES      PROFORMES      PROFORMES      PROFORMES      PROFORMES      PROFORMES      PROFORMES      PROFORMES      PROFORMES      PROFORMES
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariProformaTots (usuari):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    proformes=tablaProformaTots(cursor)

    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'proformes': proformes,
              }
    return values  

# ACCIONS DEL FORMULARI
####################################

                
class ProformaTotsInicial (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres

                #obtenim valors per al html
                values = formulariProformaTots(usuari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'profTots.html') 
                self.response.out.write(template.render(path, values,))
                


# FUNCIONS SECUNDARIES DEL FORMULARI
####################################

def tablaProformaTots(cursor):
        
        cursor.execute('SELECT fa.idFactura, fa.idEsquema, es.numExpedient, es.nomExpedient, fa.proforma, fa.dataProforma, fa.factura, fa.dataFactura, fa.dataCobro FROM esquemes es INNER JOIN  factures fa ON fa.idEsquema=es.idEsquema WHERE fa.proforma IS NOT NULL ORDER BY fa.proforma DESC LIMIT 0,500')
        tabla = cursor.fetchall()

        conta=0
        indice=0
        for i in tabla: #conta el numero de files de la tabla
            conta=conta+1
        lista=[0]*conta #creem lista
        
        for i in tabla: #cada fila es converteix en un objecte de lista
            idFactura = i[0]
            #obtenir total linies factura
            cursor.execute('SELECT SUM(tr.preu) AS preuLF FROM treballs tr INNER JOIN liniesfactura lf ON tr.idTreball=lf.idTreball GROUP BY lf.idFactura HAVING lf.idFactura=%s',(idFactura,))
            tSumPreuLF = cursor.fetchall()
            try:
                tProforma = tSumPreuLF[0] [0]
                tProforma = "%.2f" %tProforma
            except:
                tProforma = ""
            
            #obtenir total linies suplidos
            cursor.execute('SELECT SUM(preuSuplido) AS preuLS FROM liniessuplidos GROUP BY idFactura HAVING idFactura=%s',(idFactura,))
            tSumPreuLS = cursor.fetchall()
            try:
                tSuplido = tSumPreuLS[0] [0]
                tSuplido = "%.2f" %tSuplido
            except:
                tSuplido = ""
                
            dataProforma = dataFormat(i[5])
            dataFactura = dataFormat(i[7])
            dataCobro = dataFormat(i[8])

            lista[indice] = ProformaTots(i[0], i[1], i[2], i[3], i[4], dataProforma, i[6], dataFactura, dataCobro, tProforma, tSuplido) #Modificar si anyadim columna 
            indice=indice+1  
            
        return lista 


    
# CLASSES
####################################

class ProformaTots:
    def __init__(self, idFactura=0, idEsquema=0, numExpedient=0, nomExpedient=0, proforma=0, dataProforma=0, factura=0, dataFactura=0, dataCobro=0, tProforma=0, tSuplido=0):
        self.idFactura = idFactura
        self.idEsquema= idEsquema
        self.numExpedient = numExpedient
        self.nomExpedient = nomExpedient
        self.proforma = proforma
        self.dataProforma = dataProforma
        self.factura = factura
        self.dataFactura = dataFactura
        self.dataCobro = dataCobro
        self.tProforma = tProforma
        self.tSuplido = tSuplido
        

                
                
        
        
###########################################################################################################################################################
# LINIATEMPS     LINIATEMPS     LINIATEMPS     LINIATEMPS     LINIATEMPS     LINIATEMPS     LINIATEMPS     LINIATEMPS     LINIATEMPS
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariLiniatemps (usuari, idGrafica, idTreballador, idEsquema, idTarea, idHistoria, idTareaCrea):
    
    idGrafica = int(idGrafica)
    idTarea = int(idTarea)
    try:
        idTreballador = int(idTreballador)
    except:
        idTreballador = -1
    try:
        idEsquema = int(idEsquema)
    except:
        idEsquema = -1

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd   
    if idGrafica<3:
        if idTreballador==-1:
            grafica = tablaTareaFin(cursor)
            treballsTreballador = ''
            treballsTop = ''
        else:
            grafica = tablaTareaTreballador(cursor,idTreballador)
            treballsTreballador = tablaTreballLiniaTemps(cursor, idTreballador)
            treballsTop = tablaTreballLiniaTempsTop(cursor, idTreballador)
    elif idGrafica==3:
        grafica = tablaTareaEsquema(cursor,idEsquema)
        
    if idTarea == -1:
        tareaSelect = ""
        esquemaSelect = ""
    else:
        tareaSelect = tablaTareaSelect(cursor, idTarea)
        esquemaSelect = tablaEsquemaSelect(cursor, idEsquema)
    
    
    liniatempsVec = grafica
    liniatemps = liniatempsVec[0]
    colorTreballador = liniatempsVec[1]
    linkTarea = liniatempsVec[2]
    
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    treballadorAct=tablaTreballadorAct(cursor)
    treballadorTots=tablaTreballadorTots(cursor)
    color = tablaColor(cursor)
    estat = tablaEstat(cursor)
    fitxaDia = tablaFitxaHuiTreballador(cursor, idTreballador)
    horesDia = tablaHoresDiaTreballador(cursor, idTreballador)
    
    ara = datetime.datetime.today()
    hui = ara
    dataHui = hui.strftime('%Y-%m-%d')
    huiAny = hui.strftime('%j')
    
    ahir = ara - datetime.timedelta(days=1)
    dataAhir = ahir.strftime('%Y-%m-%d')
    
    if idGrafica==2:
        idTreballador=usuari
    
    if idTarea <> -1:  #divisio per a fer mes rapida la edicio
        capsulaDataHui=""
        capsulaDataAhir=""
        capAhir=""
        capHui=""
        capMes=""
        controlCapHui=""
        controlCapHuiTot=""
        controlCapAhir=""
        controlCapAhirTot=""
        
    else:
        capsulaDataHui = tablaCapsulaData(cursor, dataHui, idTreballador)
        capsulaDataAhir = tablaCapsulaData(cursor, dataAhir, idTreballador)
        
        capAhir = capsulaTrebAhir(cursor, idTreballador)
        capHui = capsulaTrebHui(cursor, idTreballador)
        capMes = capsulaTrebMes(cursor, idTreballador)

        
        dataIni = dataHui
        dataFin = dataHui
    
        
        dataIni2 = dataAhir
        dataFin2 = dataAhir
        
        controlCapHui = tablaControlCapsula(cursor, idTreballador, dataIni, dataFin)
        controlCapHuiTot = tablaControlCapsulaTot(cursor, idTreballador, dataIni, dataFin)
        controlCapAhir = tablaControlCapsula(cursor, idTreballador, dataIni2, dataFin2)
        controlCapAhirTot = tablaControlCapsulaTot(cursor, idTreballador, dataIni2, dataFin2)
    
    
    #desconectar de la bd
    db.commit()
    db.close()
    
    ara = datetime.datetime.today()
    dillunsFinD = dillunsDeuSem(ara,6)
    #dillunsActD = dillunsActual(ara,0)
    
    dillunsFin = dataFormat(dillunsFinD)
    #dillunsAct = dataFormat(dillunsActD)
    
    zoomE = str(6000)
    
    eixTemps = zoomE+","+dillunsFin
    
    
    
        
    


    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'treballadorAct': treballadorAct,
             'treballadorTots': treballadorTots,
             'liniatemps': liniatemps,
             'colorTreballador': colorTreballador,
             'linkTarea': linkTarea,
             'idGrafica': idGrafica,
             'eixTemps': eixTemps,
             'idTreballador': idTreballador,
             'capsulaDataHui': capsulaDataHui,
             'capsulaDataAhir': capsulaDataAhir,
             'capAhir': capAhir,
             'capHui': capHui,
             'capMes': capMes,
             'huiAny': huiAny,
             'controlCapHui': controlCapHui,
             'controlCapHuiTot': controlCapHuiTot,
             'controlCapAhir': controlCapAhir,
             'controlCapAhirTot': controlCapAhirTot,
             'tareaSelect': tareaSelect,
             'esquemaSelect': esquemaSelect,
             'color': color,
             'idHistoria': idHistoria,
             'idTareaCrea': idTareaCrea,
             'dataHui': dataHui,
             'estat': estat,
             'treballsTreballador': treballsTreballador,
             'treballsTop': treballsTop,
             'fitxaDia': fitxaDia,
             'horesDia': horesDia,
             }
    return values  

# ACCIONS DEL FORMULARI
####################################

                
class LiniatempsInicial (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                
                idGrafica = novar(self.request.get('idGrafica'))
                idTreballador = novar(self.request.get('idTreballador'))
                idEsquema = novar(self.request.get('idEsquema'))
                idTarea = -1
                idHistoria = -1
                idTareaCrea = -1
            
                #obtenim valors per al html
                values = formulariLiniatemps(usuari, idGrafica, idTreballador, idEsquema, idTarea, idHistoria, idTareaCrea)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'liniatemps.html') 
                self.response.out.write(template.render(path, values,))
                
class LiniatempsTots (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                
                idGrafica = 2  #no interesa, millor sempre igual que liniatempsTreballador
                idTreballador = -1
                idEsquema = -1
                idTarea = -1
                idHistoria = -1
                idTareaCrea = -1
            
                #obtenim valors per al html
                values = formulariLiniatemps(usuari, idGrafica, idTreballador, idEsquema, idTarea, idHistoria, idTareaCrea)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'liniatemps.html') 
                self.response.out.write(template.render(path, values,))
                
class LiniatempsTreballador (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                
                idGrafica = 2
                idTreballador = usuari
                idEsquema = -1
                idTarea = -1
                idHistoria= -1
                idTareaCrea = -1
            
                #obtenim valors per al html
                values = formulariLiniatemps(usuari, idGrafica, idTreballador, idEsquema, idTarea, idHistoria, idTareaCrea)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'liniatemps.html') 
                self.response.out.write(template.render(path, values,))
                
class LiniatempsEsquema (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                
                idGrafica = 3
                idTreballador = -1
                idEsquema = novar(self.request.get('idEsquema'))
                idTarea = -1
                idHistoria = -1
                idTareaCrea = -1
            
                #obtenim valors per al html
                values = formulariLiniatemps(usuari, idGrafica, idTreballador, idEsquema, idTarea, idHistoria, idTareaCrea)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'liniatemps.html') 
                self.response.out.write(template.render(path, values,))
                
                

                
                
class LiniatempsTareaSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idGrafica = 2
            idTreballador = usuari
            idTarea= novar(self.request.get('idTarea'))
            idEsquema = novar(self.request.get('idEsquema'))
            idHistoria=-1
            idTareaCrea = -1

            #obtenim valors per al html
            values = formulariLiniatemps(usuari, idGrafica, idTreballador, idEsquema, idTarea, idHistoria, idTareaCrea)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'liniatemps.html') 
            self.response.out.write(template.render(path, values,))

     

class LiniatempsTareaEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTarea= novar(self.request.get('idTarea'))
            idTreballador= novar(self.request.get('idTreballador'))
            comentari = novar(self.request.get('comentari'))
            dataTarea = novar(self.request.get('dataTarea'))
            dataFin = novar(self.request.get('dataTarea'))
            ok = novar(self.request.get('ok'))
            marca = novar(self.request.get('marca'))
            idEsquema= novar(self.request.get('idEsquema'))
            idEstat= novar(self.request.get('idEstat'))
            idTreballadorEsq= novar(self.request.get('idTreballadorEsq'))
            idEsquema= novar(self.request.get('idEsquema'))
            

            comentari = eliminaComes(comentari)
            
            try:
                ok=int(ok)
            except:
                ok=0
            
        
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('UPDATE tareas SET comentari=%s, dataTarea=%s, ok=%s, marca=%s, dataFin=%s, idTreballador=%s, idEstat=%s WHERE idTarea=%s', (comentari, dataTarea, ok, marca, dataFin, idTreballador, idEstat, idTarea,))                  
            cursor.execute('UPDATE esquemes SET idTreballador=%s WHERE idEsquema=%s', (idTreballadorEsq, idEsquema,))                  
            db.commit()
            db.close()
            
            
            
            #parametres
            #idTarea = -1
            #idEsquema = -1
            idGrafica = 2
            idTreballador = usuari
            idHistoria=-1
            idTareaCrea = -1


            #obtenim valors per al html
            values = formulariLiniatemps(usuari, idGrafica, idTreballador, idEsquema, idTarea, idHistoria, idTareaCrea)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'liniatemps.html') 
            self.response.out.write(template.render(path, values,))
            
class LiniatempsHistoria (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idGrafica = 2
            idTreballador = usuari
            idTarea= novar(self.request.get('idTarea'))
            idEsquema = novar(self.request.get('idEsquema'))
            idHistoria=-2
            idTareaCrea = -1



            #obtenim valors per al html
            values = formulariLiniatemps(usuari, idGrafica, idTreballador, idEsquema, idTarea, idHistoria, idTareaCrea)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'liniatemps.html') 
            self.response.out.write(template.render(path, values,))

class LiniatempsHistoriaCrea (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #obtenir hui
            ara = datetime.datetime.today()
            hui = ara.strftime('%Y-%m-%d')
            
            #captura del html
            idTarea= novar(self.request.get('idTarea'))
            idEsquema = novar(self.request.get('idEsquema'))
            historia = novar(self.request.get('historia'))
            
            idTreballador = usuari
            idIncidencia = 2
            dataHist = hui
            contingut = ""
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('INSERT INTO histories (idTreballador, idIncidencia, idEsquema, dataHist, historia, contingut) VALUES (%s, %s, %s, %s, %s, %s)', (idTreballador, idIncidencia, idEsquema, dataHist, historia, contingut,))
            db.commit()
            db.close()
            
            #parametres
            idGrafica = 2   
            idHistoria=-1
            idTareaCrea = -1



            #obtenim valors per al html
            values = formulariLiniatemps(usuari, idGrafica, idTreballador, idEsquema, idTarea, idHistoria, idTareaCrea)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'liniatemps.html') 
            self.response.out.write(template.render(path, values,))

class LiniatempsTarea (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idGrafica = 2
            idTreballador = usuari
            idTarea= novar(self.request.get('idTarea'))
            idEsquema = novar(self.request.get('idEsquema'))
            idHistoria=-1
            idTareaCrea = -2



            #obtenim valors per al html
            values = formulariLiniatemps(usuari, idGrafica, idTreballador, idEsquema, idTarea, idHistoria, idTareaCrea)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'liniatemps.html') 
            self.response.out.write(template.render(path, values,))
            

class LiniatempsTareaCrea (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            
            #captura del html
            idTarea= novar(self.request.get('idTarea'))
            idEsquema= novar(self.request.get('idEsquema'))
            idTreballador = novar(self.request.get('idTreballador'))
            comentari = novar(self.request.get('comentari'))
            dataTarea = novar(self.request.get('dataTarea'))
            ok = novar(self.request.get('ok'))
            marca = novar(self.request.get('marca'))
            idEstat= novar(self.request.get('idEstat'))
            
            comentari = eliminaComes(comentari)
            
            try:
                ok=int(ok)
            except:
                ok=0
            
            idTipoTarea = 1
            cancel=0
            ok = 0
            dataFin = dataTarea
            
            idTreballadorN = int(idTreballador)
            if idTreballadorN <> 19:
                marca = 0
            

            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('SELECT tr.idTreball FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost=tr.idPressupost WHERE pr.idEsquema = %s ORDER BY idTreball LIMIT 0,1', (idEsquema,))
            lista = cursor.fetchall()
            idTreball = lista[0][0]
            cursor.execute('INSERT INTO tareas (idTreballador, idTipoTarea, idTreball, comentari, dataTarea, ok, cancel, marca, dataFin, idEstat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (idTreballador, idTipoTarea, idTreball, comentari, dataTarea, ok, cancel, marca, dataFin, idEstat,))
            cursor.execute('SELECT idTarea FROM tareas ORDER BY idTarea DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idTarea = lista[0][0]
            db.commit()
            db.close()
            
            #parametres
            idGrafica = 2   
            idHistoria=-1
            idTareaCrea = -1
            idTreballador = usuari



            #obtenim valors per al html
            values = formulariLiniatemps(usuari, idGrafica, idTreballador, idEsquema, idTarea, idHistoria, idTareaCrea)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'liniatemps.html') 
            self.response.out.write(template.render(path, values,))


# FUNCIONS SECUNDARIES DEL FORMULARI
####################################





def graficaTimeline (tabla, idGrafica, idTreballador, cursor):
    b=""     
    color = ""   
    link=""
       
    for i in tabla: #cada fila es converteix en un objecte de lista

        idTreballadorTa = i[0]
        idEsquema = str(i[5])
        idTarea = str(i[6])
        numExpedient = str(i[7])
        idGrafica = str(idGrafica)
        comentari = i[1]
        #comentari = comentari.encode('ascii', 'ignore').decode('ascii')
        dataIni=dataFormat(i[2])
        dataFin=dataFormat(i[3])
        marca = str(i[8])
        claveEstat = str(i[9])
        
        ara = datetime.datetime.today()
        hui = ara.strftime('%Y-%m-%d') 
                                         
        if idTreballadorTa <> 19 and idTreballadorTa <> -1:
            if dataIni < hui:
                cursor.execute('SELECT rgb2 FROM color WHERE idTreballador=%s',(idTreballadorTa,))
            else:
                cursor.execute('SELECT rgb FROM color WHERE idTreballador=%s',(idTreballadorTa,))
        else:
            if dataIni < hui:
                cursor.execute('SELECT rgb2 FROM color WHERE idColor=%s',(marca,))
            else:
                cursor.execute('SELECT rgb FROM color WHERE idColor=%s',(marca,))
        
        vector = cursor.fetchall()
        try:
            rgb= vector [0][0]
        except:
            rgb='#000000'
        
        ara = datetime.datetime.today()
        dillunsD = dillunsActual(ara, 0)
        dilluns = dillunsD.strftime('%Y-%m-%d')
        
        
        #dataIni minim dilluns
        #if dataIni<dilluns:
                #dataIni=dilluns
        dataIni=dilluns

         
            
        #dataIni i dataFin max 10 sem mes 
        dataIniMaxD = dillunsDeuSem(ara,5)
        dataIniMaxT = dataIniMaxD.strftime('%Y-%m-%d')
        dataFinMaxD = dillunsDeuSem(ara,6)
        dataFinMaxT = dataFinMaxD.strftime('%Y-%m-%d')

        
        if dataIni>dataIniMaxT:
            dataIni=dataIniMaxT
        if dataFin>dataFinMaxT:
            dataFin = dataFinMaxT
                          
        #dataFin minim un dia mes que dataIni    
        dataplusD = datetime.datetime.strptime(dataIni, '%Y-%m-%d')+ datetime.timedelta(days=1)
        dataplusT = dataplusD.strftime('%Y-%m-%d')
        dataFin=dataplusT 
                     
        nomExpedient = i[4]
        #nomExpedient = nomExpedient.encode('ascii', 'ignore').decode('ascii')
        try:
            numExpedient = str(numExpedient)
        except:
            numExpedient=""
        try:
            nomExpedient = str(nomExpedient)
        except:
            nomExpedient=""
        try:
            claveEstat = str(claveEstat)
        except:
            claveEstat =""
        try:
            rgb = str(rgb)
        except:
            rgb=""
        try:
            comentari = str(comentari)
        except:
            comentari=""
        try:
            dataIni = str(dataIni)
        except:
            dataIni='2017-01-01'
        try:
            dataFin = str(dataFin)
        except:
            dataFin='2017-01-02'

 
        a = numExpedient+" "+nomExpedient+","+claveEstat+":"+comentari+","+rgb+","+dataIni+","+dataFin #Modificar si anyadim columna 
        
        b=b+a+"," 
        
        
        link = link+"/LiniatempsTareaSelect?idEsquema="+idEsquema+"&amp;idTarea="+idTarea+"," 
        #link = link+"/TareaSelectCal?idEsquema="+idEsquema+"&amp;idTarea="+idTarea+"&amp;idGrafica="+idGrafica+"," 

    
    c = b.rstrip(",")
    
    d = color.rstrip(",")
    
    e = link.rstrip(",")
     
    resultat = [c,d,e]

    return resultat


def graficaTimelineEsq (tabla, idGrafica, idTreballador, cursor):
    b=""     
    color = ""   
    link=""
       
    for i in tabla: #cada fila es converteix en un objecte de lista

        claveTreballador = str(i[0])
        idEsquema = str(i[5])
        idTarea = str(i[6])
        idTreballador = int(i[7])
        idGrafica = str(idGrafica)
        comentari = i[1]
        #comentari = comentari.encode('ascii', 'ignore').decode('ascii')
        dataIni=dataFormat(i[2])
        dataFin=dataFormat(i[3])
        marca = str(i[8])
        claveEstat = str(i[9])
        
        
        ara = datetime.datetime.today()
        hui = ara.strftime('%Y-%m-%d') 
                                         
        if idTreballador <> 19 and idTreballador <> -1:
            if dataIni<hui:
                cursor.execute('SELECT rgb2 FROM color WHERE idTreballador=%s',(idTreballador,))
            else:
                cursor.execute('SELECT rgb FROM color WHERE idTreballador=%s',(idTreballador,))
        else:
            if dataIni<hui:
                cursor.execute('SELECT rgb2 FROM color WHERE idColor=%s',(marca,))
            else:
                cursor.execute('SELECT rgb FROM color WHERE idColor=%s',(marca,))
                
        
        vector = cursor.fetchall()
        try:
            rgb= vector [0][0]
        except:
            rgb='#000000'
        
        
        ara = datetime.datetime.today()
        dillunsD = dillunsActual(ara, 0)
        dilluns = dillunsD.strftime('%Y-%m-%d')
        
        
        
        #dataIni minim hui
        if dataIni<dilluns:
            dataIni=dilluns
         
            
        #dataIni i dataFin max 10 sem mes 
        dataIniMaxD = dillunsDeuSem(ara,5)
        dataIniMaxT = dataIniMaxD.strftime('%Y-%m-%d')
        dataFinMaxD = dillunsDeuSem(ara,6)
        dataFinMaxT = dataFinMaxD.strftime('%Y-%m-%d')
        
        if dataIni>dataIniMaxT:
            dataIni=dataIniMaxT
        if dataFin>dataFinMaxT:
            dataFin = dataFinMaxT
                          
        #dataFin minim un dia mes que dataIni    
        dataplusD = datetime.datetime.strptime(dataIni, '%Y-%m-%d')+ datetime.timedelta(days=1)
        dataplusT = dataplusD.strftime('%Y-%m-%d')
        dataFin=dataplusT 
                     
        #nomExpedient = i[4]
        #nomExpedient = nomExpedient.encode('ascii', 'ignore').decode('ascii')
        

        try:
            claveEstat = str(claveEstat)
        except:
            claveEstat =""
        try:
            rgb = str(rgb)
        except:
            rgb=""
        try:
            comentari = str(comentari)
        except:
            comentari=""
        try:
            dataIni = str(dataIni)
        except:
            dataIni='2017-01-01'
        try:
            dataFin = str(dataFin)
        except:
            dataFin='2017-01-02'
            
        a = claveTreballador +","+claveEstat+":"+comentari+","+rgb+","+dataIni+","+dataFin #Modificar si anyadim columna 
        b=b+a+"," 
        

        
        #link = link+"/TareaSelectTemps?idEsquema="+idEsquema+"&amp;idTarea="+idTarea+"&amp;idGrafica="+idGrafica+"," 
        link = link+"/TareaSelectCal?idEsquema="+idEsquema+"&amp;idTarea="+idTarea+"&amp;idGrafica="+idGrafica+"," 

    
    c = b.rstrip(",")
    
    d = color.rstrip(",")
    
    e = link.rstrip(",")
     
    resultat = [c,d,e]

    return resultat

def passat():
    ara = datetime.datetime.today()
    data = ara - datetime.timedelta(days=7)
    anterior = data.strftime('%Y-%m-%d')
    return anterior



def tablaTareaFin(cursor):   #totes les tarees des de setmana passada
    dataIni = '2017-01-01'
    cursor.execute('SELECT ta.idTreballador, ta.comentari, ta.dataTarea, ta.dataFin, es.nomExpedient, es.idEsquema, ta.idTarea, es.numExpedient FROM esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball WHERE ta.dataTarea>%s AND ta.dataFin>%s AND ta.ok=%s AND ta.cancel=%s ORDER BY ta.dataTarea, ta.dataFin DESC',(dataIni, '2017-01-01',0,0,))
    tabla = cursor.fetchall() 
    idGrafica = 2
    idTreballador=-1
    grafica = graficaTimeline(tabla, idGrafica, idTreballador,cursor)
    return grafica


def tablaTareaTreballador(cursor, idTreballador):   #totes les tarees des de setmana passada  per a un treballador  
    dataIni = '2017-01-01'
    ara = datetime.datetime.today()
    hui = ara.strftime('%Y-%m-%d')
    dataFinMaxD = dillunsDeuSem(ara,6)
    dataFinMaxT = dataFinMaxD.strftime('%Y-%m-%d')
   
    #cursor.execute('SELECT ta.idTreballador, ta.comentari, ta.dataTarea, ta.dataFin, es.nomExpedient, es.idEsquema, ta.idTarea, es.numExpedient, ta.marca FROM treballadors tb INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball) ON ta.idTreballador = tb.idTreballador WHERE ta.dataTarea>%s AND ta.dataFin>%s AND ta.idTreballador=%s AND ta.ok=%s AND ta.cancel=%s  AND es.idEsquema <> %s OR  ta.ok=%s AND ta.cancel=%s AND es.idEsquema = %s AND ta.dataTarea >= %s  AND ta.dataTarea < %s OR ta.dataTarea>%s AND ta.dataFin>%s AND ta.idTreballador=%s AND ta.ok=%s AND ta.cancel=%s ORDER BY FIELD (ta.idTreballador, %s) DESC, tb.ordre, ta.dataTarea',(dataIni, '2017-01-01', idTreballador,0,0, 3848, 0, 0 , 3848, hui, dataFinMaxT, dataIni, '2017-01-01', 19,0,0, idTreballador,))
    #cursor.execute('SELECT ta.idTreballador, ta.comentari, ta.dataTarea, ta.dataFin, es.nomExpedient, es.idEsquema, ta.idTarea, es.numExpedient, ta.marca FROM treballadors tb INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball) ON ta.idTreballador = tb.idTreballador WHERE ta.dataTarea>%s AND ta.dataFin>%s AND ta.ok=%s AND ta.cancel=%s  AND es.idEsquema <> %s OR  ta.ok=%s AND ta.cancel=%s AND es.idEsquema = %s AND ta.dataTarea >= %s  AND ta.dataTarea < %s OR ta.dataTarea>%s AND ta.dataFin>%s AND ta.idTreballador=%s AND ta.ok=%s AND ta.cancel=%s ORDER BY FIELD (ta.idTreballador, %s) DESC, tb.ordre, ta.dataTarea',(dataIni, '2017-01-01',0,0, 3848, 0, 0 , 3848, hui, dataFinMaxT, dataIni, '2017-01-01', 19,0,0, idTreballador,))
    #cursor.execute('SELECT ta.idTreballador, ta.comentari, ta.dataTarea, ta.dataFin, es.nomExpedient, es.idEsquema, ta.idTarea, es.numExpedient, ta.marca, et.claveEstat FROM estat et INNER JOIN (treballadors tb INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball) ON ta.idTreballador = tb.idTreballador) ON et.idEstat = ta.idEstat WHERE ta.dataTarea>%s AND ta.dataFin>%s AND ta.ok=%s AND ta.cancel=%s  AND es.idEsquema <> %s OR  ta.ok=%s AND ta.cancel=%s AND es.idEsquema = %s AND ta.dataTarea >= %s  AND ta.dataTarea < %s OR ta.dataTarea>%s AND ta.dataFin>%s AND ta.idTreballador=%s AND ta.ok=%s AND ta.cancel=%s ORDER BY FIELD (ta.idTreballador, %s) DESC, et.ordre, ta.dataTarea',(dataIni, '2017-01-01',0,0, 3848, 0, 0 , 3848, hui, dataFinMaxT, dataIni, '2017-01-01', 19,0,0, idTreballador,))
    cursor.execute('SELECT ta.idTreballador, ta.comentari, ta.dataTarea, ta.dataFin, es.nomExpedient, es.idEsquema, ta.idTarea, es.numExpedient, ta.marca, et.claveEstat FROM estat et INNER JOIN (treballadors tb INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball) ON ta.idTreballador = tb.idTreballador) ON et.idEstat = ta.idEstat WHERE ta.dataTarea>%s AND ta.dataFin>%s AND ta.ok=%s AND ta.cancel=%s  AND es.idEsquema <> %s OR  ta.ok=%s AND ta.cancel=%s AND es.idEsquema = %s AND ta.dataTarea >= %s  AND ta.dataTarea < %s OR ta.dataTarea>%s AND ta.dataFin>%s AND ta.idTreballador=%s AND ta.ok=%s AND ta.cancel=%s ORDER BY   et.ordre, es.numExpedient DESC',(dataIni, '2017-01-01',0,0, 3848, 0, 0 , 3848, hui, dataFinMaxT, dataIni, '2017-01-01', 19,0,0,))
    
    
    tabla = cursor.fetchall() 
    idGrafica = 2
    grafica = graficaTimeline(tabla, idGrafica, idTreballador, cursor)
    return grafica



def tablaTareaEsquema(cursor, idEsquema):   #totes les tarees des de setmana passada  per a un treballador  
    #dataIni = passat()
    dataIni = '2017-01-01'
    #cursor.execute('SELECT tb.claveTreballador, ta.comentari, ta.dataTarea, ta.dataFin, es.nomExpedient, es.idEsquema, ta.idTarea, ta.idTreballador, ta.marca FROM treballadors tb INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball) ON ta.idTreballador = tb.idTreballador  WHERE ta.dataTarea>%s AND ta.dataFin>=%s AND es.idEsquema=%s AND ta.ok=%s AND ta.cancel=%s ORDER BY tb.ordre DESC, ta.dataTarea, ta.dataFin',(dataIni, '2017-01-01', idEsquema,0,0,))
    cursor.execute('SELECT tb.claveTreballador, ta.comentari, ta.dataTarea, ta.dataFin, es.nomExpedient, es.idEsquema, ta.idTarea, ta.idTreballador, ta.marca, et.claveEstat FROM estat et INNER JOIN (treballadors tb INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball) ON ta.idTreballador = tb.idTreballador) ON et.idEstat=ta.idEstat  WHERE ta.dataTarea>%s AND ta.dataFin>=%s AND es.idEsquema=%s AND ta.ok=%s AND ta.cancel=%s ORDER BY et.ordre DESC, ta.dataTarea, ta.dataFin',(dataIni, '2017-01-01', idEsquema,0,0,))
    
    tabla = cursor.fetchall() 
    idGrafica = 3
    idTreballador = -1
    grafica = graficaTimelineEsq(tabla, idGrafica, idTreballador, cursor)
    return grafica


###########################################################################################################################################################
# CONTROL     CONTROL     CONTROL     CONTROL     CONTROL     CONTROL     CONTROL     CONTROL     CONTROL     CONTROL     CONTROL     CONTROL
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariControl (usuari):
    

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)  
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    

    
    #desconectar de la bd
    db.commit()
    db.close()


    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,

              }
    return values  

# ACCIONS DEL FORMULARI
####################################

                
class ControlInicial (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                    
            
                #obtenim valors per al html
                values = formulariControl(usuari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'control.html') 
                self.response.out.write(template.render(path, values,))

###########################################################################################################################################################
# CAPSULA    CAPSULA    CAPSULA    CAPSULA    CAPSULA    CAPSULA    CAPSULA    CAPSULA    CAPSULA    CAPSULA    CAPSULA    CAPSULA    CAPSULA    CAPSULA
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariCapsula (usuari):
    

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    capsulaTots=tablaCapsulaTots(cursor) 
    treballadorTots = tablaTreballadorTots(cursor)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    

    
    idTreballador = -1
    ara = datetime.datetime.today()
    hui = ara
    dataHui = hui.strftime('%Y-%m-%d')
    
    capsulaDataHui = tablaCapsulaData(cursor, dataHui, idTreballador)
    
    ahir = ara - datetime.timedelta(days=1)
    dataAhir = ahir.strftime('%Y-%m-%d')
    
    capsulaDataAhir = tablaCapsulaData(cursor, dataAhir, idTreballador)
    
    #desconectar de la bd
    db.commit()
    db.close()


    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'capsulaTots': capsulaTots,
             'treballadorTots': treballadorTots,
             'iniciCapsula': iniciCapsula,
             'capsula':capsula,
             'fitxa': fitxa,
             'capsulaDataHui': capsulaDataHui,
             'capsulaDataAhir': capsulaDataAhir,

              }
    return values  

# ACCIONS DEL FORMULARI
####################################

                
class CapsulaInicial (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres

            
                #obtenim valors per al html
                values = formulariCapsula(usuari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'capsula.html') 
                self.response.out.write(template.render(path, values,))

class CapsulaNou (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idEsquema = novar(self.request.get('idEsquema'))
                idTreball = novar(self.request.get('idTreball'))
                idTreballador = usuari
                tipoCapsula = 1
                ara = araHora()
                iniciCapsula = tempsFormat(ara)
                
                
                
                            
                #accions sobre bd
                db= get_db()
                cursor = db.cursor()
                
                ultimaCapsula = tablaCapsulaUltima(cursor, usuari)
                capsula=comprobaCapsula(ultimaCapsula.iniciCapsula)
                
                if capsula == 0:               
                    cursor.execute('INSERT INTO capsula (idEsquema, idTreballador, tipoCapsula, iniciCapsula, idTreball) VALUES (%s, %s, %s, %s, %s)', (idEsquema, idTreballador, tipoCapsula, iniciCapsula, idTreball))
               
                db.commit()
                db.close()
           
                self.redirect("/Inicio")
                
                #parametres
                
#                idGrafica = 2
                
                
                
                #obtenim valors per al html
#                values = formulariLiniatemps(usuari, idGrafica, idTreballador, idEsquema)

                #imprimim el arxiu html
#                path = os.path.join(os.path.dirname(__file__), 'liniatemps.html') 
#                self.response.out.write(template.render(path, values,))
                

class CapsulaGestioNou (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idEsquema = novar(self.request.get('idEsquema'))
                numCapGestio = novar(self.request.get('numCapGestio'))
                idTreballador = usuari
                tipoCapsula = 2
                ara = araHora()
                iniciCapsula = tempsFormat(ara)
                numCapsules=int(numCapGestio)
                            
                #accions sobre bd
                db= get_db()
                cursor = db.cursor()
                i=0
                while i<numCapsules:
                    cursor.execute('INSERT INTO capsula (idEsquema, idTreballador, tipoCapsula, iniciCapsula) VALUES (%s, %s, %s, %s)', (idEsquema, idTreballador, tipoCapsula, iniciCapsula,))
                    i = i+1
                    
                db.commit()
                db.close()
                
                self.redirect("/Inicio")
           
                
                #parametres
#                idHistoria = -1
#                idTarea = -1
    
                #obtenim valors per al html
#                values = esquema(usuari, idEsquema, idTarea, idHistoria)
    
                #imprimim el arxiu html
#                path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
#                self.response.out.write(template.render(path, values,))

class CapsulaElimina (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idCapsula = novar(self.request.get('idCapsula'))

                
                            
                #accions sobre bd
                db= get_db()
                cursor = db.cursor()
                cursor.execute('DELETE FROM capsula WHERE idCapsula=%s',(idCapsula,))
                db.commit()
                db.close()
                
                
            
                #obtenim valors per al html
                values = formulariCapsula(usuari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'capsula.html') 
                self.response.out.write(template.render(path, values,))

class CapsulaRepetir (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
                idTreballador=usuari

                #accions sobre bd
                db= get_db()
                cursor = db.cursor()
                
                cursor.execute('SELECT idTreball,idEsquema FROM capsula WHERE idTreballador=%s ORDER BY idCapsula DESC LIMIT 0,1',(idTreballador,))
                lista = cursor.fetchall()
                idTreball = lista[0][0]
                idEsquema = lista[0][1]
                tipoCapsula = 1
                ara = araHora()
                iniciCapsula = tempsFormat(ara)
                
                ultimaCapsula = tablaCapsulaUltima(cursor, usuari)
                capsula=comprobaCapsula(ultimaCapsula.iniciCapsula)
                
                if capsula == 0:               
                    cursor.execute('INSERT INTO capsula (idEsquema, idTreballador, tipoCapsula, iniciCapsula, idTreball) VALUES (%s, %s, %s, %s, %s)', (idEsquema, idTreballador, tipoCapsula, iniciCapsula,idTreball))
               
                db.commit()
                db.close()
           
                self.redirect("/Inicio")



# FUNCIONS SECUNDARIES DEL FORMULARI
####################################

def tablaCapsulaTots(cursor):
        
        cursor.execute('SELECT  ca.idCapsula, ca.idTreballador, ca.idEsquema, ca.tipoCapsula, ca.iniciCapsula, es.numExpedient, es.nomExpedient, ca.idTreball FROM esquemes es INNER JOIN capsula ca ON es.idEsquema = ca.idEsquema ORDER BY iniciCapsula DESC LIMIT 0,500')
        tabla = cursor.fetchall()

        conta=0
        indice=0
        for i in tabla: #conta el numero de files de la tabla
            conta=conta+1
        lista=[0]*conta #creem lista
        
        for i in tabla: #cada fila es converteix en un objecte de lista

            inici = tempsFormat(i[4])

            lista[indice] = Capsula(i[0], i[1], i[2], i[3], inici, i[5], i[6], i[7]) #Modificar si anyadim columna 
            indice=indice+1  
            
        return lista 

def tablaCapsulaUltima(cursor, idTreballador):
        
        cursor.execute('SELECT  ca.idCapsula, ca.idTreballador, ca.idEsquema, ca.tipoCapsula, ca.iniciCapsula, es.numExpedient, es.nomExpedient, ca.idTreball FROM esquemes es INNER JOIN capsula ca ON es.idEsquema = ca.idEsquema WHERE ca.idTreballador=%s AND ca.tipoCapsula=%s ORDER BY iniciCapsula DESC LIMIT 0,1', (idTreballador, 1,))
        tabla = cursor.fetchall()
        lista = Capsula (1,1,1,1, '2017-01-01 00:00:00',1,1)
        for i in tabla: #cada fila es converteix en un objecte de lista

            inici = tempsFormat(i[4])
            lista= Capsula(i[0], i[1], i[2], i[3], inici, i[5], i[6], i[7])
             
        return lista 


def comprobaCapsula (iniciCapsula):
        inici=datetime.datetime.strptime(iniciCapsula,'%Y-%m-%d %H:%M:%S')
        ara = araHora()
        diferencia = ara - inici  
        
        segons = diferencia.total_seconds()
        
        if segons <= 1800:
            comproba=1
        else:
            comproba=0
        
        return comproba

def tablaCapsulaData(cursor, data, idTreballador):

        idTreballador = int(idTreballador)
        
        if idTreballador == -1:
            cursor.execute('SELECT  idTreballador, claveTreballador FROM treballadors WHERE enActiu=%s ORDER BY idTreballador',(1,))
        else:
            cursor.execute('SELECT  idTreballador, claveTreballador FROM treballadors WHERE enActiu=%s AND idTreballador = %s',(1, idTreballador,))
        
        tabla = cursor.fetchall()

        conta=0
        indice=0
        for i in tabla: #conta el numero de files de la tabla
            conta=conta+1
        lista=[0]*conta #creem lista
        
        for i in tabla: #cada fila es converteix en un objecte de lista
            
            idTreballador = int(i[0])
            claveTreballador = i[1]
            cursor.execute('SELECT  COUNT(tipoCapsula) FROM esquemes es INNER JOIN capsula ca ON es.idEsquema = ca.idEsquema WHERE ca.tipoCapsula=%s AND ca.idTreballador=%s  AND CAST(iniciCapsula AS DATE) = %s ORDER BY ca.idTreballador',(1, idTreballador, data,))
            vectorOfi = cursor.fetchall()
            ofi=vectorOfi[0][0]
            try:
                nofi=int(ofi)
            except:
                nofi=0
            cursor.execute('SELECT  COUNT(tipoCapsula) FROM esquemes es INNER JOIN capsula ca ON es.idEsquema = ca.idEsquema WHERE ca.tipoCapsula=%s AND ca.idTreballador=%s  AND CAST(iniciCapsula AS DATE) = %s ORDER BY ca.idTreballador',(2, idTreballador, data,))
            vectorGest = cursor.fetchall()
            gest=vectorGest[0][0]
            try:
                ngest=int(gest)
            except:
                ngest=0
            total=nofi+ngest

            lista[indice] = CapsulaTot(idTreballador, claveTreballador, data, nofi, ngest, total) #Modificar si anyadim columna 
            indice=indice+1  
            
        return lista 

def tablaCapsulaHui(cursor):
        arahui = datetime.datetime.today()
        hui = arahui.strftime('%Y-%m-%d')
        lista = tablaCapsulaData(cursor, hui)
        return lista
        
def tablaCapsulaAhir(cursor):        
        araahir = datetime.datetime.today() - datetime.timedelta(days=1)
        ahir = araahir.strftime('%Y-%m-%d')
        lista = tablaCapsulaData(cursor, ahir)
        return lista
    
def capsulaTrebAhir (cursor, idTreballador):
        araahir = datetime.datetime.today() - datetime.timedelta(days=1)
        ahir = araahir.strftime('%Y-%m-%d')
        data = ahir
        cursor.execute('SELECT  COUNT(tipoCapsula) FROM esquemes es INNER JOIN capsula ca ON es.idEsquema = ca.idEsquema WHERE ca.tipoCapsula=%s AND ca.idTreballador=%s  AND CAST(iniciCapsula AS DATE) = %s ORDER BY ca.idTreballador',(1, idTreballador, data,))
        vectorOfi = cursor.fetchall()
        ofi=vectorOfi[0][0]
        try:
            nofi=int(ofi)
        except:
            nofi=0
        cursor.execute('SELECT  COUNT(tipoCapsula) FROM esquemes es INNER JOIN capsula ca ON es.idEsquema = ca.idEsquema WHERE ca.tipoCapsula=%s AND ca.idTreballador=%s  AND CAST(iniciCapsula AS DATE) = %s ORDER BY ca.idTreballador',(2, idTreballador, data,))
        vectorGest = cursor.fetchall()
        gest=vectorGest[0][0]
        try:
            ngest=int(gest)
        except:
            ngest=0
        total=nofi+ngest
        return total

def capsulaTrebHui (cursor, idTreballador):
        arahui = datetime.datetime.today()
        hui = arahui.strftime('%Y-%m-%d')
        data = hui
        cursor.execute('SELECT  COUNT(tipoCapsula) FROM esquemes es INNER JOIN capsula ca ON es.idEsquema = ca.idEsquema WHERE ca.tipoCapsula=%s AND ca.idTreballador=%s  AND CAST(iniciCapsula AS DATE) = %s ORDER BY ca.idTreballador',(1, idTreballador, data,))
        vectorOfi = cursor.fetchall()
        ofi=vectorOfi[0][0]
        try:
            nofi=int(ofi)
        except:
            nofi=0
        cursor.execute('SELECT  COUNT(tipoCapsula) FROM esquemes es INNER JOIN capsula ca ON es.idEsquema = ca.idEsquema WHERE ca.tipoCapsula=%s AND ca.idTreballador=%s  AND CAST(iniciCapsula AS DATE) = %s ORDER BY ca.idTreballador',(2, idTreballador, data,))
        vectorGest = cursor.fetchall()
        gest=vectorGest[0][0]
        try:
            ngest=int(gest)
        except:
            ngest=0
        total=nofi+ngest
        return total

def capsulaTrebMes (cursor, idTreballador):
        #primer dia del mes actual
        arahui=datetime.datetime.today()
        dataIni='%d-%d-1'%(arahui.year, arahui.month)
        dataIni=datetime.datetime.strptime(dataIni,'%Y-%m-%d')
        dataFin= arahui.strftime('%Y-%m-%d')
        cursor.execute('SELECT  COUNT(tipoCapsula) FROM esquemes es INNER JOIN capsula ca ON es.idEsquema = ca.idEsquema WHERE ca.tipoCapsula=%s AND ca.idTreballador=%s  AND CAST(iniciCapsula AS DATE) >= %s AND CAST(iniciCapsula AS DATE) <= %s ORDER BY ca.idTreballador',(1, idTreballador, dataIni, dataFin,))
        vectorOfi = cursor.fetchall()
        ofi=vectorOfi[0][0]
        try:
            nofi=int(ofi)
        except:
            nofi=0
        cursor.execute('SELECT  COUNT(tipoCapsula) FROM esquemes es INNER JOIN capsula ca ON es.idEsquema = ca.idEsquema WHERE ca.tipoCapsula=%s AND ca.idTreballador=%s  AND CAST(iniciCapsula AS DATE) >= %s AND CAST(iniciCapsula AS DATE) <= %s ORDER BY ca.idTreballador',(2, idTreballador, dataIni, dataFin,))
        vectorGest = cursor.fetchall()
        gest=vectorGest[0][0]
        try:
            ngest=int(gest)
        except:
            ngest=0
        total=nofi+ngest
        return total

def ingressosMesActual(cursor):
        
        
        arahui=datetime.datetime.today()
        dataIni='%d-%d-1'%(arahui.year, arahui.month)
        dataIni=datetime.datetime.strptime(dataIni,'%Y-%m-%d')
        dataFin= arahui.strftime('%Y-%m-%d')
          
                
        
        cursor.execute('SELECT es.idEsquema, fa.idFactura, es.nomExpedient, fa.proforma, fa.dataCobro FROM esquemes es INNER JOIN factures fa ON es.idEsquema = fa.idEsquema INNER JOIN moviments mo ON mo.idFactura=fa.idFactura WHERE fa.enPis=%s AND mo.dataMov>=%s AND mo.dataMov<=%s', (1, dataIni, dataFin,))
        tabla = cursor.fetchall()

        tcobrat=0
        
        for i in tabla: #cada fila es converteix en un objecte de lista
            idFactura = i[1]
            #facturat
            cursor.execute('SELECT SUM(tr.preu) FROM factures fa INNER JOIN (treballs tr INNER JOIN liniesfactura lf ON tr.idTreball = lf.idTreball) ON fa.idFactura=lf.idFactura WHERE fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro>=%s AND fa.dataCobro<=%s',(idFactura, 1, dataIni, dataFin,))
            vector = cursor.fetchall()
            facturat = vector[0][0]
            if facturat:
                facturat=facturat
            else:
                facturat=0
                
            #suplido
            cursor.execute('SELECT SUM(ls.preuSuplido) FROM liniessuplidos ls LEFT JOIN factures fa ON ls.idFactura=fa.idFactura WHERE fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro>=%s AND fa.dataCobro<=%s',(idFactura, 1,dataIni,dataFin,))
            vector = cursor.fetchall()
            suplido = vector[0][0]
            if suplido:
                suplido=suplido
            else:
                suplido=0
            
            #cobrat
            cursor.execute('SELECT sum(quantitat) FROM moviments WHERE idFactura=%s AND dataMov>=%s AND dataMov<=%s',(idFactura, dataIni, dataFin,))
            vector = cursor.fetchall()
            cobrat  = vector[0][0]
            
            if cobrat:
                cobrat=int(cobrat)
                cursor.execute('SELECT dataFactura FROM factures WHERE idFactura=%s',(idFactura,))
                vector = cursor.fetchall()
                data  = vector[0][0]
                dataFactura=dataFormat(data)
                dataIni=dataFormat(dataIni)
                if dataFactura>dataIni:
                    factura=1
                else:
                    factura = 0
            else:
                cobrat=0
                factura=0
        
                
            if factura >0:
                #obtenir tipo IVA
                cursor.execute('SELECT tipoIVA FROM constants WHERE idConstant=%s',(1,))
                tTipoIVA = cursor.fetchall()
                try:
                    tipoIVA = tTipoIVA [0] [0]
                except:
                    tipoIVA = 0
                    
                if suplido == 0:
                    cobrat = cobrat/(1+tipoIVA)
                else:
                    cobrat = (cobrat-suplido)/(1+tipoIVA)

            tcobrat = tcobrat+cobrat
        
        cobrat = "%.2f" %tcobrat

            
        return cobrat 
    
def ingressosAnyActual(cursor):
        
        
        arahui=datetime.datetime.today()
        dataIni='%d-1-1'%(arahui.year)
        #dataIni='%d-1-1'%(arahui.year-1)
        dataIni=datetime.datetime.strptime(dataIni,'%Y-%m-%d')
        dataFin= arahui.strftime('%Y-%m-%d')
        #dataFin='%d-12-31'%(arahui.year-1)
          
                
        
        cursor.execute('SELECT es.idEsquema, fa.idFactura, es.nomExpedient, fa.proforma, fa.dataCobro FROM esquemes es INNER JOIN factures fa ON es.idEsquema = fa.idEsquema INNER JOIN moviments mo ON mo.idFactura=fa.idFactura WHERE fa.enPis=%s AND mo.dataMov>=%s AND mo.dataMov<=%s', (1, dataIni, dataFin,))
        tabla = cursor.fetchall()

        tcobrat=0
        
        for i in tabla: #cada fila es converteix en un objecte de lista
            idFactura = i[1]
            #facturat
            cursor.execute('SELECT SUM(tr.preu) FROM factures fa INNER JOIN (treballs tr INNER JOIN liniesfactura lf ON tr.idTreball = lf.idTreball) ON fa.idFactura=lf.idFactura WHERE fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro>=%s AND fa.dataCobro<=%s',(idFactura, 1, dataIni, dataFin,))
            vector = cursor.fetchall()
            facturat = vector[0][0]
            if facturat:
                facturat=facturat
            else:
                facturat=0
                
            #suplido
            cursor.execute('SELECT SUM(ls.preuSuplido) FROM liniessuplidos ls LEFT JOIN factures fa ON ls.idFactura=fa.idFactura WHERE fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro>=%s AND fa.dataCobro<=%s',(idFactura, 1,dataIni,dataFin,))
            vector = cursor.fetchall()
            suplido = vector[0][0]
            if suplido:
                suplido=suplido
            else:
                suplido=0
            
            #cobrat
            cursor.execute('SELECT sum(quantitat) FROM moviments WHERE idFactura=%s AND dataMov>=%s AND dataMov<=%s',(idFactura, dataIni, dataFin,))
            vector = cursor.fetchall()
            cobrat  = vector[0][0]
            
            if cobrat:
                cobrat=int(cobrat)
                cursor.execute('SELECT dataFactura FROM factures WHERE idFactura=%s',(idFactura,))
                vector = cursor.fetchall()
                data  = vector[0][0]
                dataFactura=dataFormat(data)
                dataIni=dataFormat(dataIni)
                if dataFactura>dataIni:
                    factura=1
                else:
                    factura = 0
            else:
                cobrat=0
                factura=0
        
                
            if factura >0:
                #obtenir tipo IVA
                cursor.execute('SELECT tipoIVA FROM constants WHERE idConstant=%s',(1,))
                tTipoIVA = cursor.fetchall()
                try:
                    tipoIVA = tTipoIVA [0] [0]
                except:
                    tipoIVA = 0
                    
                if suplido == 0:
                    cobrat = cobrat/(1+tipoIVA)
                else:
                    cobrat = (cobrat-suplido)/(1+tipoIVA)

            tcobrat = tcobrat+cobrat
        
        cobrat = "%.2f" %tcobrat

            
        return cobrat 

def ingressosAnyAnterior(cursor):
        
        
        arahui=datetime.datetime.today()
        dataIni='%d-1-1'%(arahui.year-1)
        dataIni=datetime.datetime.strptime(dataIni,'%Y-%m-%d')
        dataFin='%d-%d-%d'%(arahui.year-1, arahui.month, arahui.day)
          
                
        
        cursor.execute('SELECT es.idEsquema, fa.idFactura, es.nomExpedient, fa.proforma, fa.dataCobro FROM esquemes es INNER JOIN factures fa ON es.idEsquema = fa.idEsquema INNER JOIN moviments mo ON mo.idFactura=fa.idFactura WHERE fa.enPis=%s AND mo.dataMov>=%s AND mo.dataMov<=%s', (1, dataIni, dataFin,))
        tabla = cursor.fetchall()

        tcobrat=0
        
        for i in tabla: #cada fila es converteix en un objecte de lista
            idFactura = i[1]
            #facturat
            cursor.execute('SELECT SUM(tr.preu) FROM factures fa INNER JOIN (treballs tr INNER JOIN liniesfactura lf ON tr.idTreball = lf.idTreball) ON fa.idFactura=lf.idFactura WHERE fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro>=%s AND fa.dataCobro<=%s',(idFactura, 1, dataIni, dataFin,))
            vector = cursor.fetchall()
            facturat = vector[0][0]
            if facturat:
                facturat=facturat
            else:
                facturat=0
                
            #suplido
            cursor.execute('SELECT SUM(ls.preuSuplido) FROM liniessuplidos ls LEFT JOIN factures fa ON ls.idFactura=fa.idFactura WHERE fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro>=%s AND fa.dataCobro<=%s',(idFactura, 1,dataIni,dataFin,))
            vector = cursor.fetchall()
            suplido = vector[0][0]
            if suplido:
                suplido=suplido
            else:
                suplido=0
            
            #cobrat
            cursor.execute('SELECT sum(quantitat) FROM moviments WHERE idFactura=%s AND dataMov>=%s AND dataMov<=%s',(idFactura, dataIni, dataFin,))
            vector = cursor.fetchall()
            cobrat  = vector[0][0]
            
            if cobrat:
                cobrat=int(cobrat)
                cursor.execute('SELECT dataFactura FROM factures WHERE idFactura=%s',(idFactura,))
                vector = cursor.fetchall()
                data  = vector[0][0]
                dataFactura=dataFormat(data)
                dataIni=dataFormat(dataIni)
                if dataFactura>dataIni:
                    factura=1
                else:
                    factura = 0
            else:
                cobrat=0
                factura=0
        
                
            if factura >0:
                #obtenir tipo IVA
                cursor.execute('SELECT tipoIVA FROM constants WHERE idConstant=%s',(1,))
                tTipoIVA = cursor.fetchall()
                try:
                    tipoIVA = tTipoIVA [0] [0]
                except:
                    tipoIVA = 0
                    
                if suplido == 0:
                    cobrat = cobrat/(1+tipoIVA)
                else:
                    cobrat = (cobrat-suplido)/(1+tipoIVA)

            tcobrat = tcobrat+cobrat
        
        cobrat = "%.2f" %tcobrat

            
        return cobrat 
          
        


# CLASSES
####################################

class Capsula:
    def __init__(self, idCapsula=0, idTreballador=0, idEsquema=0, tipoCapsula=0, iniciCapsula=0, numExpedient=0, nomExpedient=0, idTreball=0):
        self.idCapsula = idCapsula
        self.idTreballador = idTreballador
        self.idEsquema= idEsquema
        self.tipoCapsula = tipoCapsula
        self.iniciCapsula = iniciCapsula
        self.numExpedient = numExpedient
        self.nomExpedient = nomExpedient
        self.idTreball = idTreball

class CapsulaTot:
    def __init__(self, idTreballador=0, claveTreballador=0, data=0, nofi=0, ngest=0, total=0):
        self.idTreballador = idTreballador
        self.claveTreballador= claveTreballador
        self.data = data
        self.nofi = nofi
        self.ngest = ngest
        self.total = total
        


###########################################################################################################################################################
# ROL   ROL     ROL    ROL    ROL    ROL    ROL    ROL    ROL    ROL    ROL    ROL    ROL    ROL    ROL    ROL    ROL    ROL    ROL    ROL    ROL        
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariRol (usuari, idRol, idEsquema):
    

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    
    if idRol == -1: #nou
        rolSelect = ''     
    else: # select    
        rolSelect = tablaRolSelect(cursor, idRol)
        
    rolEsq = tablaRolEsq(cursor, idEsquema)
    treballadorAct = tablaTreballadorAct(cursor)
    treballadorTots = tablaTreballadorTots(cursor)


    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'treballadorAct': treballadorAct,
             'treballadorTots': treballadorTots,
             'rolSelect': rolSelect,
             'rolEsq': rolEsq,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'idEsquema': idEsquema,
             'idRol': idRol,
              }
    return values  

# ACCIONS DEL FORMULARI
####################################

                
class RolNou (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idEsquema = novar(self.request.get('idEsquema'))
                idRol = -1
            
                #obtenim valors per al html
                values = formulariRol(usuari, idRol, idEsquema)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'rol.html') 
                self.response.out.write(template.render(path, values,))

                
            
class RolSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idRol= novar(self.request.get('idRol'))
            idEsquema = novar(self.request.get('idEsquema'))

            #obtenim valors per al html
            values = formulariRol(usuari, idRol, idEsquema)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'rol.html') 
            self.response.out.write(template.render(path, values,))

            

class RolEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idRol= novar(self.request.get('idRol'))
            idEsquema= novar(self.request.get('idEsquema'))
            idTreballador= novar(self.request.get('idTreballador'))
            rol= novar(self.request.get('rol'))
            marca= novar(self.request.get('marca'))


          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('UPDATE rol SET idTreballador=%s, rol=%s, marca=%s WHERE idRol=%s', (idTreballador, rol, marca, idRol,))          
            db.commit()
            db.close()

            #obtenim valors per al html
            values = formulariRol(usuari, idRol, idEsquema)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'rol.html') 
            self.response.out.write(template.render(path, values,))

class RolCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idEsquema= novar(self.request.get('idEsquema'))
            idTreballador = novar(self.request.get('idTreballador'))
            rol = novar(self.request.get('rol'))
            marca = novar(self.request.get('marca'))


            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('INSERT INTO rol (idEsquema, idTreballador, rol, marca) VALUES (%s, %s, %s, %s)', (idEsquema, idTreballador, rol, marca,))
            
            db.commit()
            db.close()
            
            idRol=-1

            #obtenim valors per al html
            values = formulariRol(usuari, idRol, idEsquema)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'rol.html') 
            self.response.out.write(template.render(path, values,))

class RolElimina (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idRol= novar(self.request.get('idRol'))
                idEsquema= novar(self.request.get('idEsquema'))

                #conectar a la bd
                db= get_db()
                cursor = db.cursor()
                
                cursor.execute('DELETE FROM rol WHERE idRol=%s',(idRol,))

                db.commit()
                db.close()

                #parametres
                idTarea=-1
                idHistoria = -1
    
                #obtenim valors per al html
                values = esquema(usuari, idEsquema, idTarea, idHistoria)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'esquema.html') 
                self.response.out.write(template.render(path, values,))



# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaRolEsq(cursor, idEsquema):   
    cursor.execute('SELECT idRol, idEsquema, idTreballador, rol, marca FROM rol WHERE idEsquema=%s ORDER BY marca DESC',(idEsquema,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Rol(i[0],i[1],i[2],i[3],i[4]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 


def tablaRolSelect(cursor, idRol):
    cursor.execute('SELECT idRol, idEsquema, idTreballador, rol, marca FROM rol WHERE idRol=%s',(idRol,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista = Rol(i[0],i[1],i[2],i[3],i[4]) #Modificar si anyadim columna 
    return lista 


class Rol:
    def __init__(self, idRol=0, idEsquema=0, idTreballador=0, rol='', marca=0):
        self.idRol = idRol
        self.idEsquema = idEsquema
        self.idTreballador = idTreballador
        self.rol = rol
        self.marca = marca


###########################################################################################################################################################
# RANKING        RANKING        RANKING        RANKING        RANKING        RANKING        RANKING        RANKING        RANKING        RANKING        
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariRanking (usuari):
    

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    ranking = tablaRanking(cursor)
    treballadorAct = tablaTreballadorAct(cursor)
    treballadorTots = tablaTreballadorTots(cursor)
    



    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'treballadorAct': treballadorAct,
             'treballadorTots': treballadorTots,
             'ranking': ranking,

              }
    return values  

# ACCIONS DEL FORMULARI
####################################

                
class RankingInicial (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
            
                #obtenim valors per al html
                values = formulariRanking(usuari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'ranking.html') 
                self.response.out.write(template.render(path, values,))

class EliminaRanking (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #captura del html
                idEsquema= novar(self.request.get('idEsquema'))

                #accions sobre bd
                db= get_db()
                cursor = db.cursor()
                cursor.execute('UPDATE esquemes SET check8=%s WHERE idEsquema=%s', (0,idEsquema,))          
                db.commit()
                db.close()
            
                #obtenim valors per al html
                values = formulariRanking(usuari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'ranking.html') 
                self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaRanking(cursor):   
    cursor.execute('SELECT es.idEsquema, es.numExpedient, es.nomExpedient, count(ca.idEsquema) as cap FROM esquemes es INNER JOIN capsula ca ON es.idEsquema = ca.idEsquema WHERE es.numExpedient>%s AND es.numExpedient<%s AND es.idEsquema <> %s AND es.check8=%s GROUP BY ca.idEsquema HAVING count(ca.idEsquema)>%s ORDER BY ca.idEsquema DESC', ('19000C', 'C00000', '3747',1,12,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    
    cost = 38.60 # COSTCAP
    
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        idEsquema = i[0]
        numExpedient = i[1]
        nomExpedient = i[2]
        cap = i[3]
        
        cursor.execute('SELECT idFactura FROM factures WHERE idEsquema=%s',(idEsquema,))
        tabla2 = cursor.fetchall()
        
        if tabla2:
            cobratT=0
            cobrat=0

            for i in tabla2: #cada fila es converteix en un objecte de lista
                idFactura = i[0]
                dataIni='2017-01-01'
                cursor.execute('SELECT sum(quantitat) FROM moviments WHERE idFactura=%s AND dataMov>=%s',(idFactura, dataIni,))
                vector = cursor.fetchall()
                cobratV  = vector[0][0]
                
                if cobratV:
                    cobrat=float(cobratV)
                    cursor.execute('SELECT dataFactura FROM factures WHERE idFactura=%s',(idFactura,))
                    vector = cursor.fetchall()
                    data  = vector[0][0]
                    dataFactura=dataFormat(data)
                    dataIni=dataFormat(dataIni)
                    if dataFactura>dataIni:
                        factura=1
                    else:
                        factura = 0
                else:
                    cobrat=0
                    factura=0
                
                #suplido
                cursor.execute('SELECT SUM(ls.preuSuplido) FROM liniessuplidos ls LEFT JOIN (factures fa INNER JOIN (treballs tr INNER JOIN liniesfactura lf ON tr.idTreball = lf.idTreball) ON fa.idFactura=lf.idFactura) ON ls.idFactura=fa.idFactura WHERE fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro IS NULL OR fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro>=%s OR fa.idFactura=%s AND fa.enPis=%s AND fa.dataCobro<%s',(idFactura, 1, idFactura, 1,dataIni,idFactura, 1,'1900-01-01',))
                vector = cursor.fetchall()
                suplido = vector[0][0]
                if suplido:
                    suplido=suplido
                else:
                    suplido=0
            
                    
                if factura >0:
                    #obtenir tipo IVA
                    cursor.execute('SELECT tipoIVA FROM constants WHERE idConstant=%s',(1,))
                    tTipoIVA = cursor.fetchall()
                    try:
                        tipoIVA = tTipoIVA [0] [0]
                    except:
                        tipoIVA = 0
                        
                    if suplido == 0:
                        cobrat = cobrat/(1+tipoIVA)
                    else:
                        cobrat = (cobrat-suplido)/(1+tipoIVA)
                
                cobratT=cobrat+cobratT
                
            eur = cobratT
            if eur == 0:
                rent = -cost
            else:
                rent = eur/cap-cost
            rentT = "%.2f"%rent
            eurT = "%.2f"%eur
                
        else:
            eur = 0
            rent =-cost
            rentT = "%.2f"%rent
            eurT = "%.2f"%eur
        
        benef = rent*cap
        costD = cost*cap
        benefT = "%.2f"%benef
        costT = "%.2f"%costD
        
        cursor.execute('SELECT ta.idTarea FROM tareas ta INNER JOIN treballs tr ON ta.idTreball = tr.idTreball INNER JOIN pressupostos pr ON tr.idPressupost = pr.idPressupost WHERE pr.idEsquema=%s AND ta.idTreballador<>%s AND ta.ok=%s',(idEsquema, '19', '0'))
        tareas = cursor.fetchall()
        
        if tareas:
            tramit=1
        else:
            tramit=0
        
        lista[indice] = Ranking(idEsquema,numExpedient,nomExpedient,cap,eur,rent,rentT,eurT,benef, benefT, tramit, costD, costT) #Modificar si anyadim columna 
        indice=indice+1 
        
    
    listaO = sorted(lista, key=lambda objeto: objeto.benef, reverse = True)

      
    return listaO 




class Ranking:
    def __init__(self, idEsquema, numExpedient, nomExpedient, cap, eur, rent, rentT, eurT, benef, benefT, tramit, costD, costT):
        self.idEsquema = idEsquema
        self.numExpedient = numExpedient
        self.nomExpedient = nomExpedient
        self.cap = cap
        self.eur = eur
        self.rent = rent
        self.rentT = rentT
        self.eurT = eurT
        self.benef = benef
        self.benefT = benefT
        self.tramit = tramit
        self.costD = costD
        self.costT = costT
    def __str__(self):
        return "%s - %s" % (self.rent, self.cap)
    def __cmp__(self, other):
        if self.rent == other.rent:
            return 1 if self.cap > other.cap else -1
        elif self.rent < other.rent:
            return -1
        else:
            return 1



###########################################################################################################################################################
# CONTROLCAPSULA       CONTROLCAPSULA        CONTROLCAPSULA       CONTROLCAPSULA       CONTROLCAPSULA       CONTROLCAPSULA       CONTROLCAPSULA                 
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariControlCapsula (usuari, idTreballador, dataIni, dataFin):
    

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    idTreballador = int(idTreballador)
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    treballadorAct = tablaTreballadorAct(cursor)
    treballadorTots = tablaTreballadorTots(cursor)
    controlCapsula = tablaControlCapsula(cursor, idTreballador, dataIni, dataFin)
    controlCapsulaTot = tablaControlCapsulaTot(cursor, idTreballador, dataIni, dataFin)
        
    



    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'treballadorAct': treballadorAct,
             'treballadorTots': treballadorTots,
             'controlCapsula': controlCapsula,
             'controlCapsulaTot': controlCapsulaTot,
             'idTreballador': idTreballador,
             'dataIni': dataIni,
             'dataFin': dataFin,

              }
    return values  

# ACCIONS DEL FORMULARI
####################################

                
class ControlCapsulaInicial (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
                ara = datetime.datetime.today()
                dillunsActD = dillunsActual(ara,0)
                dataHui = ara.strftime('%Y-%m-%d')
                dillunsAct = dillunsActD.strftime('%Y-%m-%d')
                
                #parametres
                
                idTreballador = 19
                dataIni = dillunsAct
                dataFin = dataHui
            
                #obtenim valors per al html
                values = formulariControlCapsula(usuari, idTreballador, dataIni, dataFin)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'controlcapsula.html') 
                self.response.out.write(template.render(path, values,))
                

class ControlCapsulaSelect (webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
                idTreballador= novar(self.request.get('idTreballador'))
                dataIni= novar(self.request.get('dataIni'))
                dataFin= novar(self.request.get('dataFin'))
                
                #parametres
            
                #obtenim valors per al html
                values = formulariControlCapsula(usuari, idTreballador, dataIni, dataFin)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'controlcapsula.html') 
                self.response.out.write(template.render(path, values,))




# FUNCIONS SECUNDARIES DEL FORMULARI
####################################



def tablaControlCapsula(cursor, idTreballador, dataIni, dataFin): 
    
    treb = int(idTreballador)  
    
    if treb==19: #armonic
        cursor.execute('SELECT  es.numExpedient, es.nomExpedient, COUNT(ca.tipoCapsula) AS cap  FROM esquemes es INNER JOIN capsula ca ON es.idEsquema = ca.idEsquema WHERE CAST(iniciCapsula AS DATE) >= %s AND CAST(iniciCapsula AS DATE) <= %s GROUP BY es.idEsquema ORDER BY cap DESC',(dataIni, dataFin,))
    else:
        cursor.execute('SELECT  es.numExpedient, es.nomExpedient, COUNT(ca.tipoCapsula) AS cap  FROM esquemes es INNER JOIN capsula ca ON es.idEsquema = ca.idEsquema WHERE ca.idTreballador=%s  AND CAST(iniciCapsula AS DATE) >= %s AND CAST(iniciCapsula AS DATE) <= %s GROUP BY es.idEsquema ORDER BY cap DESC',(idTreballador, dataIni, dataFin,))
    
        
        
    tabla = cursor.fetchall()
    
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista 
      
    for i in tabla: #cada fila es converteix en un objecte de lista
        
        lista[indice] = ControlCapsula(i[0],i[1],i[2]) #Modificar si anyadim columna 
        
        indice=indice+1  
            
    return lista

def tablaControlCapsulaTot(cursor, idTreballador, dataIni, dataFin): 
    
    treb = int(idTreballador)  
    
    
    if treb==19: #armonic
        cursor.execute('SELECT  es.numExpedient, es.nomExpedient, COUNT(ca.tipoCapsula) AS cap  FROM esquemes es INNER JOIN capsula ca ON es.idEsquema = ca.idEsquema WHERE CAST(iniciCapsula AS DATE) >= %s AND CAST(iniciCapsula AS DATE) <= %s GROUP BY es.idEsquema ORDER BY cap DESC',(dataIni, dataFin,))
    else:
        cursor.execute('SELECT  es.numExpedient, es.nomExpedient, COUNT(ca.tipoCapsula) AS cap  FROM esquemes es INNER JOIN capsula ca ON es.idEsquema = ca.idEsquema WHERE ca.idTreballador=%s  AND CAST(iniciCapsula AS DATE) >= %s AND CAST(iniciCapsula AS DATE) <= %s GROUP BY es.idEsquema ORDER BY cap DESC',(idTreballador, dataIni, dataFin,))
    
        
    vector = cursor.fetchall()

    total = 0

      
    for i in vector: #cada fila es converteix en un objecte de lista
        
        try:
            ncont=int(i[2])
        except:
            ncont=0
        total = total + ncont

            
    return total


class ControlCapsula:
    def __init__(self, numExpedient, nomExpedient, capsula):
        self.numExpedient = numExpedient
        self.nomExpedient = nomExpedient
        self.capsula = capsula





###########################################################################################################################################################
# GANT    GANT    GANT    GANT    GANT    GANT    GANT    GANT    GANT    GANT    GANT    GANT    GANT    GANT    GANT    GANT    GANT    GANT    GANT
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariGant (usuari, idTarea, idEsquema, zoom):
    


    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
    
    if idTarea == -1:
        tareaSelect = ''
        esquemaSelect = ''
    else:
        tareaSelect = tablaTareaSelect(cursor,idTarea)
        esquemaSelect = tablaEsquemaSelect(cursor, idEsquema)
        
    zoom = int(zoom)
        
    if zoom == 1:
        zoomE = str(6000)
    else:
        zoomE = str(1800)
        
        
        
    grafica = tablaGraficaGant(cursor,zoom)
    
    liniatempsVec = grafica
    liniatemps = liniatempsVec[0]
    linkTarea = liniatempsVec[2]
    
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    treballadorAct=tablaTreballadorAct(cursor)
    treballadorTots= tablaTreballadorTots(cursor)
    color = tablaColor(cursor)
    estat = tablaEstat(cursor)
    
    ara = datetime.datetime.today()
    hui = ara
    dataHui = hui.strftime('%Y-%m-%d')
    huiAny = hui.strftime('%j')
    huiAnyD = int(huiAny)
    objectiu = (230000+14000)/365*huiAnyD # COFRE
    
    if idTarea <> -1:  #divisio per a fer mes rapida la edicio
        ingAnyActual=""
        ingAnyAnterior=""
        ingMesActual =""
        difAnterior=""
        difObjectiu=""
        cofre=""
        objectiu=""

        
    else:
        ingAnyActual = ingressosAnyActual(cursor)
        ingAnyAnterior = ingressosAnyAnterior(cursor)
        ingMesActual = ingressosMesActual(cursor)
        
        ingAnyActual = float(ingAnyActual)
        ingAnyAnterior = float(ingAnyAnterior)
        
        difAnterior= ingAnyActual-ingAnyAnterior
        difObjectiu= ingAnyActual - objectiu
        
        cofre = difObjectiu*0.25
    
        
        objectiu = "%.2f" %objectiu
        cofre = "%.2f" %cofre
        difObjectiu = "%.2f" %difObjectiu
           

    
    
    #desconectar de la bd
    db.commit()
    db.close()
    
    ara = datetime.datetime.today()
    dillunsFinD = dillunsDeuSem(ara,6)
    #dillunsActD = dillunsActual(ara,0)
    
    dillunsFin = dataFormat(dillunsFinD)
    #dillunsAct = dataFormat(dillunsActD)
    
    

    
    eixTemps = zoomE+","+dillunsFin
    
    



        
    


    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'treballadorAct': treballadorAct,
             'liniatemps': liniatemps,
             'linkTarea': linkTarea,
             'eixTemps': eixTemps,
             'treballadorTots': treballadorTots,
             'color': color,
             'tareaSelect': tareaSelect,
             'esquemaSelect': esquemaSelect,
             'zoom': zoom,
             'estat': estat,           
             'ingAnyActual': ingAnyActual,
             'ingAnyAnterior': ingAnyAnterior,
             'ingMesActual': ingMesActual,
             'difAnterior': difAnterior,
             'objectiu': objectiu,
             'difObjectiu': difObjectiu,
             'cofre': cofre,
             'huiAny': huiAny,
             'dataHui': dataHui,
             }
    return values  

# ACCIONS DEL FORMULARI
####################################

                
class GantInicial (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                
                idTarea = -1
                idEsquema = -1
                zoom = 1
                #obtenim valors per al html
                values = formulariGant(usuari, idTarea, idEsquema,zoom)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'gant.html') 
                self.response.out.write(template.render(path, values,))
                
class GantZoom (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                
                idTarea = -1
                idEsquema = -1
                zoom= novar(self.request.get('zoom'))
                #obtenim valors per al html
                values = formulariGant(usuari, idTarea, idEsquema, zoom)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'gant.html') 
                self.response.out.write(template.render(path, values,))
                
class GantTareaSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTarea= novar(self.request.get('idTarea'))
            idEsquema = novar(self.request.get('idEsquema'))
            zoom = novar(self.request.get('zoom'))

            #obtenim valors per al html
            values = formulariGant(usuari, idTarea, idEsquema, zoom)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'gant.html') 
            self.response.out.write(template.render(path, values,))

     

class GantTareaEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTarea= novar(self.request.get('idTarea'))
            idTreballador= novar(self.request.get('idTreballador'))
            comentari = novar(self.request.get('comentari'))
            dataTarea = novar(self.request.get('dataTarea'))
            dataFin = novar(self.request.get('dataFin'))
            ok = novar(self.request.get('ok'))
            marca = novar(self.request.get('marca'))
            zoom = novar(self.request.get('zoom'))
            idEstat= novar(self.request.get('idEstat'))
            idTreballadorEsq= novar(self.request.get('idTreballadorEsq'))
            idEsquema= novar(self.request.get('idEsquema'))
            
            try:
                ok=int(ok)
            except:
                ok=0

            comentari = eliminaComes(comentari)
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('UPDATE tareas SET comentari=%s, dataTarea=%s, ok=%s, marca=%s, dataFin=%s, idTreballador=%s, idEstat=%s WHERE idTarea=%s', (comentari, dataTarea, ok, marca, dataFin, idTreballador, idEstat, idTarea,))                  
            cursor.execute('UPDATE esquemes SET idTreballador=%s WHERE idEsquema=%s', (idTreballadorEsq, idEsquema,))                  
            
            db.commit()
            db.close()
            
            
            
            #parametres
            #idTarea = -1
            #idEsquema = -1


            #obtenim valors per al html

            values = formulariGant(usuari, idTarea, idEsquema, zoom)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'gant.html') 
            self.response.out.write(template.render(path, values,))
                


# FUNCIONS SECUNDARIES DEL FORMULARI
####################################





def graficaGant (tabla, cursor,zoom):
    b=""     
    color = ""   
    link=""
       
    for i in tabla: #cada fila es converteix en un objecte de lista

        idTreballador = i[0]
        idEsquema = str(i[5])
        idTarea = str(i[6])
        numExpedient = str(i[7])
        comentari = i[1]
        dataIni=dataFormat(i[2])
        dataFin=dataFormat(i[3])
        marca = str(i[8])
        claveEstat = str(i[9])
        
        ara = datetime.datetime.today()
        hui = ara.strftime('%Y-%m-%d') 
                                         
        if idTreballador <> 19 and idTreballador <> -1:
            if dataIni < hui:
                cursor.execute('SELECT rgb2 FROM color WHERE idTreballador=%s',(idTreballador,))
            else:
                cursor.execute('SELECT rgb FROM color WHERE idTreballador=%s',(idTreballador,))
        else:
            if dataIni < hui:
                cursor.execute('SELECT rgb2 FROM color WHERE idColor=%s',(marca,))
            else:
                cursor.execute('SELECT rgb FROM color WHERE idColor=%s',(marca,))
            

        vector = cursor.fetchall()
        
            
        try:
            rgb= vector [0][0]
        except:
            rgb=''
        
        
        ara = datetime.datetime.today()
        dillunsD = dillunsActual(ara, 0)
        dilluns = dillunsD.strftime('%Y-%m-%d')
        
        #dataIni minim dilluns
        if dataIni<dilluns:
                dataIni=dilluns

        #dataIni i dataFin max 10 sem mes 
        dataIniMaxD = dillunsDeuSem(ara,5)
        dataIniMaxT = dataIniMaxD.strftime('%Y-%m-%d')
        dataFinMaxD = dillunsDeuSem(ara,6)
        dataFinMaxT = dataFinMaxD.strftime('%Y-%m-%d')
        

        if dataIni>dataIniMaxT:
            dataIni=dataIniMaxT
        if dataFin>dataFinMaxT:
            dataFin = dataFinMaxT
                          
        #dataFin minim un dia mes que dataIni    
        dataplusD = datetime.datetime.strptime(dataIni, '%Y-%m-%d')+ datetime.timedelta(days=1)
        dataplusT = dataplusD.strftime('%Y-%m-%d')
        dataFin=dataplusT 
                     
        nomExpedient = i[4]
        #nomExpedient = nomExpedient.encode('ascii', 'ignore').decode('ascii')
        try:
            nomExpedient = str(nomExpedient)
        except:
            nomExpedient=""
        
        try:
            dataIni = str(dataIni)
        except:
            dataIni=""
        
        try:
            a = numExpedient+" "+nomExpedient+","+claveEstat+":"+comentari+","+rgb+","+dataIni+","+dataFin #Modificar si anyadim columna 
        except:
            a =""
        b=b+a+"," 
        
        zoom = str(zoom)
        

        
        #link = link+"/TareaSelectTemps?idEsquema="+idEsquema+"&amp;idTarea="+idTarea+"&amp;idGrafica="+""+"," 
        #link = link+"/TareaSelectCal?idEsquema="+idEsquema+"&amp;idTarea="+idTarea+"&amp;idGrafica="+idGrafica+"," 
        link = link+"/GantTareaSelect?idEsquema="+idEsquema+"&amp;idTarea="+idTarea+"&amp;zoom="+zoom+"," 
        

    
    c = b.rstrip(",")
    
    d = color.rstrip(",")
    
    e = link.rstrip(",")
     
    resultat = [c,d,e]

    return resultat





def tablaGraficaGant(cursor,zoom):   #totes les tarees des de setmana passada  per a un treballador  
    dataIni = '2017-01-01'
    #idTreballador = 19
    ara = datetime.datetime.today()
    hui = ara.strftime('%Y-%m-%d')  
    #dilluns=dillunsActual(ara,0)  
    #dataIni max 10 sem 
    dataIniMaxD = dillunsDeuSem(ara,6)
    dataIniMaxT = dataIniMaxD.strftime('%Y-%m-%d')
    
    cursor.execute('SELECT ta.idTreballador, ta.comentari, ta.dataTarea, ta.dataFin, es.nomExpedient, es.idEsquema, ta.idTarea, es.numExpedient, ta.marca, et.claveEstat FROM estat et INNER JOIN (treballadors tb INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball) ON ta.idTreballador = tb.idTreballador) ON et.idEstat = ta.idEstat WHERE ta.dataTarea>%s AND ta.dataTarea<%s AND ta.dataFin>=%s AND ta.ok=%s AND ta.cancel=%s AND es.idEsquema <> %s OR  ta.ok=%s AND ta.cancel=%s AND es.idEsquema = %s AND ta.dataTarea >= %s AND ta.dataTarea <= %s  ORDER BY et.ordre, ta.dataTarea, ta.dataFin DESC, es.numExpedient',(dataIni, dataIniMaxT, dataIni,0,0, 3848, 0,0, 3848, hui, dataIniMaxT,))
    tabla = cursor.fetchall() 

    grafica = graficaGant(tabla, cursor,zoom)
    return grafica



###########################################################################################################################################################
# VACANCES        VACANCES        VACANCES        VACANCES        VACANCES        VACANCES        VACANCES        VACANCES        VACANCES        VACANCES    
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariVacances (usuari, idTarea):
    
    idEsquema = 3848
    
    #dataHui
    ara = datetime.datetime.today()
    dataHui = ara.strftime('%Y-%m-%d')


    #connexio
    db= get_db()
    cursor = db.cursor()
    
    treballadorSelect=tablaTreballadorSelect(cursor, usuari)
    iniciCapsula = tablaCapsulaUltima(cursor, usuari)
    capsula=comprobaCapsula(iniciCapsula.iniciCapsula)
    fitxa=estatFitxa(cursor,usuari)
    esquemaSelect=tablaEsquemaSelect(cursor, idEsquema)
    color = tablaColor(cursor)            
    treballadorAct = tablaTreballadorAct(cursor)
    treballadorTots = tablaTreballadorTots(cursor)
    vacancesPassat = tablaVacancesPassat(cursor)
    vacancesPendent = tablaVacancesPendent(cursor)
    vacancesAny = tablaVacancesAny(cursor)
    vacancesAnyTotal = tablaVacancesAnyTotal(cursor)
      
    if idTarea >0:
        tareaSelect=tablaTareaSelect(cursor,idTarea)           
    else:
        tareaSelect=Tarea(idTarea,'','','','','','','')

    grafica = tablaTareaVacances(cursor,idEsquema)
    liniatempsVec = grafica
    liniatemps = liniatempsVec[0]
    linkTarea = liniatempsVec[2]
       
    db.commit()
    db.close()
        
        
    zoomE = str(6000)
        
    eixTemps = zoomE+","+zoomE

    #pasem les llistes al arxiu html
    values = {
             'idEsquema': idEsquema,
             'treballadorSelect': treballadorSelect,
             'iniciCapsula': iniciCapsula,
             'capsula': capsula,
             'fitxa': fitxa,
             'esquemaSelect': esquemaSelect,
             'tareaSelect': tareaSelect,
             'vacancesPassat': vacancesPassat,
             'vacancesPendent': vacancesPendent,
             'vacancesAny': vacancesAny,
             'vacancesAnyTotal': vacancesAnyTotal,
             'treballadorAct': treballadorAct,
             'treballadorTots': treballadorTots,
             'dataHui': dataHui,
             'liniatemps':liniatemps,
             'eixTemps': eixTemps,
             'linkTarea': linkTarea,
             'color': color,
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class VacancesSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            idTarea = -1
            #obtenim valors per al html
            values = formulariVacances(usuari, idTarea)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'vacances.html') 
            self.response.out.write(template.render(path, values,))

class VacancesTareaSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            idTarea  = novar(self.request.get('idTarea'))
            
            #hui
            ara = datetime.datetime.today()  
            hui = ara.strftime('%Y-%m-%d')
    
            #connexio
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('SELECT dataTarea, idTreballador FROM tareas WHERE idTarea=%s', (idTarea,))
            lista = cursor.fetchall()
            dataTarea = lista[0][0]
            idTreballador = lista[0][1]
            inicial = dataTarea.strftime('%Y-%m-%d')
            
            cursor.execute('SELECT nivell FROM treballadors WHERE idTreballador=%s', (usuari,))
            lista2 = cursor.fetchall()
            nivell = lista2[0][0]
            
            if idTreballador <> usuari:
                if nivell<2:
                    idTarea=-1
            else:
                if inicial < hui:
                    if nivell < 2:
                        idTarea=-1
            
            db.commit()
            db.close()
            
            
            #obtenim valors per al html
            values = formulariVacances(usuari, idTarea)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'vacances.html') 
            self.response.out.write(template.render(path, values,))            

class VacancesTareaNou(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            idTarea = -2
            #obtenim valors per al html
            values = formulariVacances(usuari, idTarea)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'vacances.html') 
            self.response.out.write(template.render(path, values,))

class VacancesTareaCrea(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            #captura del html
            idTarea= novar(self.request.get('idTarea'))
            idEsquema= 3848
            idTreballador = novar(self.request.get('idTreballador'))
            comentari = novar(self.request.get('comentari'))
            dataTarea = novar(self.request.get('dataTarea'))
            ok = novar(self.request.get('ok'))
            
            try:
                ok=int(ok)
            except:
                ok=0
                
            comentari = eliminaComes(comentari)
            
            idTipoTarea = 1
            cancel=0
            ok = 0
            dataFin = dataTarea
            marca=0
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            #comproba que la data no esta ocupada
            
            cursor.execute('SELECT ta.dataTarea FROM esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball WHERE es.idEsquema=%s AND ta.ok=%s AND ta.dataTarea=%s',(idEsquema, 0, dataTarea,))
            existe = cursor.fetchall()
            if existe:
                cursor.execute('SELECT nivell FROM treballadors WHERE idTreballador=%s', (usuari,))
                lista2 = cursor.fetchall()
                nivell = lista2[0][0]
                    
                if nivell < 2:
                    self.redirect("/ErrorVacances")
                else:
                    cursor.execute('SELECT tr.idTreball FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost=tr.idPressupost WHERE pr.idEsquema = %s ORDER BY idTreball LIMIT 0,1', (idEsquema,))
                    lista = cursor.fetchall()
                    idTreball = lista[0][0]
                    cursor.execute('INSERT INTO tareas (idTreballador, idTipoTarea, idTreball, comentari, dataTarea, ok, cancel, marca, dataFin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (idTreballador, idTipoTarea, idTreball, comentari, dataTarea, ok, cancel, marca, dataFin,))
                    cursor.execute('SELECT idTarea FROM tareas ORDER BY idTarea DESC LIMIT 0,1')
                    lista = cursor.fetchall()
                    idTarea = lista[0][0]
                    db.commit()
                    db.close()
            
                    #obtenim valors per al html
                    values = formulariVacances(usuari, idTarea)
        
                    #imprimim el arxiu html
                    path = os.path.join(os.path.dirname(__file__), 'vacances.html') 
                    self.response.out.write(template.render(path, values,))

            else:
                cursor.execute('SELECT tr.idTreball FROM pressupostos pr INNER JOIN treballs tr ON pr.idPressupost=tr.idPressupost WHERE pr.idEsquema = %s ORDER BY idTreball LIMIT 0,1', (idEsquema,))
                lista = cursor.fetchall()
                idTreball = lista[0][0]
                cursor.execute('INSERT INTO tareas (idTreballador, idTipoTarea, idTreball, comentari, dataTarea, ok, cancel, marca, dataFin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (idTreballador, idTipoTarea, idTreball, comentari, dataTarea, ok, cancel, marca, dataFin,))
                cursor.execute('SELECT idTarea FROM tareas ORDER BY idTarea DESC LIMIT 0,1')
                lista = cursor.fetchall()
                idTarea = lista[0][0]
                db.commit()
                db.close()
            
                #obtenim valors per al html
                values = formulariVacances(usuari, idTarea)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'vacances.html') 
                self.response.out.write(template.render(path, values,))

class ErrorVacances(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1): 
            self.response.write('Data ocupada, torna arrere per ficar un altra o consulta si es pot agafar eixa data')

class VacancesTareaEdita(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            #captura del html
            idTarea= novar(self.request.get('idTarea'))
            idTreballador = novar(self.request.get('idTreballador'))
            comentari = novar(self.request.get('comentari'))
            dataTarea = novar(self.request.get('dataTarea'))
            dataFin = dataTarea
            ok = novar(self.request.get('ok'))
            marca = 0
            idEsquema = 3848
            
            try:
                ok=int(ok)
            except:
                ok=0
            

            comentari = eliminaComes(comentari)
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            #comproba si la dataTarea ha canviat
            cursor.execute('SELECT dataTarea FROM tareas WHERE idTarea=%s', (idTarea,))
            vector = cursor.fetchall()
            dataTareaInicial = vector [0][0]
            
            if dataTarea <> dataTareaInicial:
                #comproba que la data no esta ocupada
                cursor.execute('SELECT ta.dataTarea FROM esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball WHERE es.idEsquema=%s AND ta.ok=%s AND ta.dataTarea=%s',(idEsquema, 0, dataTarea,))
                existe = cursor.fetchall()
                if existe:
                    cursor.execute('SELECT nivell FROM treballadors WHERE idTreballador=%s', (usuari,))
                    lista2 = cursor.fetchall()
                    nivell = lista2[0][0]
                    
                    if nivell < 2:
                        self.redirect("/ErrorVacances")
                    else:
                        cursor.execute('UPDATE tareas SET idTreballador=%s, comentari=%s, dataTarea=%s, ok=%s, marca=%s, dataFin=%s WHERE idTarea=%s', (idTreballador, comentari, dataTarea, ok, marca, dataFin, idTarea,))          
                        db.commit()
                        db.close()
                        #obtenim valors per al html
                        values = formulariVacances(usuari, idTarea)
            
                        #imprimim el arxiu html
                        path = os.path.join(os.path.dirname(__file__), 'vacances.html') 
                        self.response.out.write(template.render(path, values,))
                    
                else:
                    cursor.execute('UPDATE tareas SET idTreballador=%s, comentari=%s, dataTarea=%s, ok=%s, marca=%s, dataFin=%s WHERE idTarea=%s', (idTreballador, comentari, dataTarea, ok, marca, dataFin, idTarea,))          
                    db.commit()
                    db.close()
                    #obtenim valors per al html
                    values = formulariVacances(usuari, idTarea)
        
                    #imprimim el arxiu html
                    path = os.path.join(os.path.dirname(__file__), 'vacances.html') 
                    self.response.out.write(template.render(path, values,))

            else:
                cursor.execute('UPDATE tareas SET idTreballador=%s, comentari=%s, dataTarea=%s, ok=%s, marca=%s, dataFin=%s WHERE idTarea=%s', (idTreballador, comentari, dataTarea, ok, marca, dataFin, idTarea,))          
                db.commit()
                db.close()
                #obtenim valors per al html
                values = formulariVacances(usuari, idTarea)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'vacances.html') 
                self.response.out.write(template.render(path, values,))   

def tablaTareaVacances(cursor, idEsquema):   #totes les tarees des de setmana passada  per a un treballador  
    #primer dia del any actual
    dataAny=datetime.datetime.today()
    dataAny='%d-1-1'%(dataAny.year)
    dataAny=datetime.datetime.strptime(dataAny,'%Y-%m-%d')
    
    cursor.execute('SELECT tb.claveTreballador, ta.comentari, ta.dataTarea, ta.dataFin, es.nomExpedient, es.idEsquema, ta.idTarea, ta.idTreballador, ta.marca FROM treballadors tb INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball) ON ta.idTreballador = tb.idTreballador  WHERE ta.dataTarea>%s AND ta.dataFin>=%s AND es.idEsquema=%s AND ta.ok=%s AND ta.cancel=%s ORDER BY tb.ordre DESC, ta.dataTarea, ta.dataFin',(dataAny, '2017-01-01', idEsquema,0,0,))
    tabla = cursor.fetchall() 
    idGrafica = 3
    idTreballador = -1
    grafica = graficaTimelineVacances(tabla, idGrafica, idTreballador, cursor)
    return grafica

def graficaTimelineVacances (tabla, idGrafica, idTreballador, cursor):
    b=""     
    color = ""   
    link=""
       
    for i in tabla: #cada fila es converteix en un objecte de lista

        claveTreballador = str(i[0])
        #idEsquema = str(i[5])
        idTarea = str(i[6])
        idTreballador = int(i[7])
        idGrafica = str(idGrafica)
        comentari = i[1]
        #comentari = comentari.encode('ascii', 'ignore').decode('ascii')
        dataIni=dataFormat(i[2])
        dataFin=dataFormat(i[3])
        marca = str(i[8])
                                         
        if idTreballador <> 19 and idTreballador <> -1:
            cursor.execute('SELECT rgb FROM color WHERE idTreballador=%s',(idTreballador,))
        else:
            cursor.execute('SELECT rgb FROM color WHERE idColor=%s',(marca,))
        
        vector = cursor.fetchall()
        rgb= vector [0][0]
        
        #dataFin minim un dia mes que dataIni    
        dataplusD = datetime.datetime.strptime(dataIni, '%Y-%m-%d')+ datetime.timedelta(days=1)
        dataplusT = dataplusD.strftime('%Y-%m-%d')
        dataFin=dataplusT 
                       
        #nomExpedient = i[4]
        #nomExpedient = nomExpedient.encode('ascii', 'ignore').decode('ascii')
        a = claveTreballador +","+comentari+","+rgb+","+dataIni+","+dataFin #Modificar si anyadim columna 
        b=b+a+"," 
        

        
        #link = link+"/TareaSelectTemps?idEsquema="+idEsquema+"&amp;idTarea="+idTarea+"&amp;idGrafica="+idGrafica+"," 
        #link = link+"/TareaSelectCal?idEsquema="+idEsquema+"&amp;idTarea="+idTarea+"&amp;idGrafica="+idGrafica+"," 
        link = link+"/VacancesTareaSelect?idTarea="+idTarea+"," 

    
    c = b.rstrip(",")
    
    d = color.rstrip(",")
    
    e = link.rstrip(",")
     
    resultat = [c,d,e]

    return resultat

def tablaVacancesPassat(cursor):
    idEsquema = 3848
    #primer dia del any actual
    dataAny=datetime.datetime.today()
    dataAny='%d-1-1'%(dataAny.year)
    dataAny=datetime.datetime.strptime(dataAny,'%Y-%m-%d')
        
    #hui
    ara = datetime.datetime.today()  
    hui = ara.strftime('%Y-%m-%d')
       
    cursor.execute('SELECT ta.idTarea, ta.idTreballador, ta.idTipoTarea, ta.idTreball, ta.comentari, ta.dataTarea, ta.ok, ta.cancel, ta.marca, ta.dataFin FROM esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball WHERE es.idEsquema=%s AND ta.ok=%s AND ta.dataTarea>=%s AND ta.dataTarea <=%s ORDER BY ta.dataTarea',(idEsquema, 0, dataAny, hui,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[5])
        dataFin=dataFormat(i[9])
        lista[indice] = Tarea(i[0],i[1],i[2],i[3],i[4],data,i[6],i[7], i[8],dataFin) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

def tablaVacancesPendent(cursor):
    idEsquema = 3848
    #primer dia del any actual
    dataAny=datetime.datetime.today()
    dataAny='%d-1-1'%(dataAny.year)
    dataAny=datetime.datetime.strptime(dataAny,'%Y-%m-%d')
        
    #hui
    ara = datetime.datetime.today()  
    hui = ara.strftime('%Y-%m-%d')
       
    cursor.execute('SELECT ta.idTarea, ta.idTreballador, ta.idTipoTarea, ta.idTreball, ta.comentari, ta.dataTarea, ta.ok, ta.cancel, ta.marca, ta.dataFin FROM esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball WHERE es.idEsquema=%s AND ta.ok=%s AND ta.dataTarea>=%s AND ta.dataTarea >%s ORDER BY ta.dataTarea',(idEsquema, 0, dataAny, hui,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[5])
        dataFin=dataFormat(i[9])
        lista[indice] = Tarea(i[0],i[1],i[2],i[3],i[4],data,i[6],i[7], i[8],dataFin) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

def tablaVacancesAny (cursor):
    idEsquema = 3848
    #primer dia del any actual
    dataAny=datetime.datetime.today()
    dataAny='%d-1-1'%(dataAny.year)
    dataAny=datetime.datetime.strptime(dataAny,'%Y-%m-%d')

    #hui
    ara = datetime.datetime.today()  
    hui = ara.strftime('%Y-%m-%d')
    
    cursor.execute('SELECT tb.idTreballador, tb.claveTreballador, COUNT(ta.idTarea) FROM treballadors tb INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball) ON ta.idTreballador = tb.idTreballador WHERE es.idEsquema = %s AND ta.dataTarea>=%s AND ta.dataTarea <= %s AND ta.ok=%s GROUP BY tb.claveTreballador ORDER BY tb.ordre',(idEsquema, dataAny, hui, 0,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = DiesVacances(i[0],i[1],i[2]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

def tablaVacancesAnyTotal (cursor):
    idEsquema = 3848
    #primer dia del any actual
    dataAny=datetime.datetime.today()
    dataAny='%d-1-1'%(dataAny.year)
    dataAny=datetime.datetime.strptime(dataAny,'%Y-%m-%d')
        
    dataFin='%d-1-1'%(dataAny.year+1)
    dataFin=datetime.datetime.strptime(dataFin,'%Y-%m-%d')
    
    cursor.execute('SELECT tb.idTreballador, tb.claveTreballador, COUNT(ta.idTarea) FROM treballadors tb INNER JOIN (esquemes es INNER JOIN pressupostos pr ON es.idEsquema = pr.idEsquema INNER JOIN treballs tr ON tr.idPressupost = pr.idPressupost INNER JOIN tareas ta ON ta.idTreball=tr.idTreball) ON ta.idTreballador = tb.idTreballador WHERE es.idEsquema = %s AND ta.dataTarea>=%s AND ta.dataTarea <= %s AND ta.ok=%s GROUP BY tb.claveTreballador ORDER BY tb.ordre',(idEsquema, dataAny, dataFin, 0,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista   
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = DiesVacances(i[0],i[1],i[2]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

class DiesVacances:
    def __init__(self, idTreballador, claveTreballador, dies):
        self.idTreballador = idTreballador
        self.claveTreballador= claveTreballador
        self.dies = dies



###########################################################################################################################################################
# FITXAR      FITXAR      FITXAR      FITXAR      FITXAR      FITXAR      FITXAR      FITXAR      FITXAR      FITXAR      FITXAR      FITXAR      FITXAR
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
 

# ACCIONS DEL FORMULARI
####################################

                


class FitxaOn (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idTreballador = usuari
                treballant = 1
                ara = araHora()
                iniciFitxa = tempsFormat(ara)
                
           
                #accions sobre bd
                db= get_db()
                cursor = db.cursor()
                               
                cursor.execute('INSERT INTO fitxar (idTreballador, treballant, hora) VALUES (%s, %s, %s)', (idTreballador, treballant, iniciFitxa))
               
                db.commit()
                db.close()
           
                self.redirect("/Inicio")

class FitxaOff (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idTreballador = usuari
                treballant = 0
                ara = araHora()
                iniciFitxa = tempsFormat(ara)
                
           
                #accions sobre bd
                db= get_db()
                cursor = db.cursor()
                               
                cursor.execute('INSERT INTO fitxar (idTreballador, treballant, hora) VALUES (%s, %s, %s)', (idTreballador, treballant, iniciFitxa))
               
                db.commit()
                db.close()
           
                self.redirect("/Inicio")

def estatFitxa(cursor, idTreballador):       
    estat = 0   
    cursor.execute('SELECT  idFitxar, idTreballador, hora, treballant FROM fitxar WHERE idTreballador=%s ORDER BY idFitxar DESC LIMIT 0,1', (idTreballador,))
    tabla = cursor.fetchall() 
    #La data de la ultima fitxa es hui?
    data= dataFormat(tabla[0][2])
    treballant= int(tabla[0][3])
    hora = tempsFormat(tabla[0][2])
    horaT = datetime.datetime.strptime(hora, '%Y-%m-%d %H:%M:%S')       
    #obtenir hui
    ara = datetime.datetime.today()
    hui = ara.strftime('%Y-%m-%d') 
    if data==hui:
        #la ultima fitxa es on?
        if treballant==1:
            estat=1
        else:
            estat=0
    else:
        #la ultima fitxa es on?
        if treballant==1:
            #inserta off a les 18:00 de eixa data
            treballant2=0
            hora2='%d-%d-%d 18:00:00'%(horaT.year, horaT.month, horaT.day)
            hora2=datetime.datetime.strptime(hora2,'%Y-%m-%d %H:%M:%S')
            cursor.execute('INSERT INTO fitxar (idTreballador, treballant, hora) VALUES (%s, %s, %s)', (idTreballador, treballant2, hora2))
            estat=0
        else:
            estat=0
    return estat 

def tablaFitxaHuiTreballador(cursor, idTreballador):
    ara = datetime.datetime.today()
    hui = ara.strftime('%Y-%m-%d %H:%M:%S')
    huiT = datetime.datetime.strptime(hui, '%Y-%m-%d %H:%M:%S')
    huiIniT='%d-%d-%d 00:00:00'%(huiT.year, huiT.month, huiT.day)
    huiIni=datetime.datetime.strptime(huiIniT,'%Y-%m-%d %H:%M:%S')
    huiFinT='%d-%d-%d 23:59:59'%(huiT.year, huiT.month, huiT.day)
    huiFin=datetime.datetime.strptime(huiFinT,'%Y-%m-%d %H:%M:%S')
    
    
    cursor.execute('SELECT idFitxar, idTreballador, hora, treballant FROM fitxar WHERE idTreballador=%s AND hora>%s AND hora<%s ORDER BY idFitxar', (idTreballador,huiIni, huiFin))
    tabla = cursor.fetchall()
    
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        hora=tempsFormat(i[2])
        lista[indice] = Fitxa(i[0],i[1],hora,i[3]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista

class Fitxa:
    def __init__(self, idFitxar=0, idTreballador=0, hora=0, treballant=0):
        self.idFitxar = idFitxar
        self.idTreballador = idTreballador
        self.hora= hora
        self.treballant = treballant
        
def tablaHoresDiaTreballador(cursor,idTreballador):
    #definir hui
    ara = datetime.datetime.today()
    hui = ara.strftime('%Y-%m-%d %H:%M:%S')
    huiT = datetime.datetime.strptime(hui, '%Y-%m-%d %H:%M:%S')
    huiIniT='%d-%d-%d 00:00:00'%(huiT.year, huiT.month, huiT.day)
    huiIni=datetime.datetime.strptime(huiIniT,'%Y-%m-%d %H:%M:%S')
    huiFinT='%d-%d-%d 23:59:59'%(huiT.year, huiT.month, huiT.day)
    huiFin=datetime.datetime.strptime(huiFinT,'%Y-%m-%d %H:%M:%S')
    
    #esta el treballador en ON?
    
    estat = estatFitxa(cursor,idTreballador)
    
        
    treballant=1
    cursor.execute('SELECT SUM(TIME_TO_SEC(hora)) FROM fitxar WHERE idTreballador=%s AND hora>%s AND hora<%s AND treballant = %s', (idTreballador,huiIni, huiFin, treballant))
    tabla = cursor.fetchall()
    try:
        sumaEntrada=int(tabla[0][0])
    except:
        sumaEntrada=0
        
    treballant=0
    cursor.execute('SELECT SUM(TIME_TO_SEC(hora)) FROM fitxar WHERE idTreballador=%s AND hora>%s AND hora<%s AND treballant = %s', (idTreballador,huiIni, huiFin, treballant))
    tabla2 = cursor.fetchall()
    try:
        sumaSalida=int(tabla2[0][0])
    except:
        sumaSalida=0
            
    if estat == 1:
        ara = araHora()
        tiempo = ara - huiIni # Devuelve un objeto timedelta
        segDia = int(tiempo.total_seconds())
        
        sumaSalida=sumaSalida+segDia
    else:
        sumaSalida=sumaSalida
        
    try:
        segons = sumaSalida-sumaEntrada
    except:
        segons=0
        
    if segons > 7200:
        segons = segons - 1800
        if segons > 25200:
            segons = segons - 3600
            
    
    num=segons
    hor=(int(num/3600))
    minu=int((num-(hor*3600))/60)
    seg=num-((hor*3600)+(minu*60))
        
    hores =(str(hor)+"h "+str(minu)+"m "+str(seg)+"s")
    
    return hores
    
        
        


        
###########################################################################################################################################################
# REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO
###########################################################################################################################################################
       

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/Inicio', Inicio),
    ('/Index', Index),  
    ('/EsquemesTots', EsquemesTots),        #Esquemes Tots
    ('/EsquemesUltims', EsquemesUltims),
    ('/UsuariTots', UsuariTots),            #Control Usuaris 
    ('/UsuariNou', UsuariNou),
    ('/UsuariCrea', UsuariCrea),
    ('/UsuariSelect', UsuariSelect),
    ('/UsuariEdita', UsuariEdita), 
    ('/EsquemaSelect', EsquemaSelect),      #Esquema
    ('/EsquemaEdita', EsquemaEdita),
    ('/EsquemaNou', EsquemaNou),
    ('/EsquemaCrea', EsquemaCrea),
    ('/IntermediariTots', IntermediariTots), #Intermediari
    ('/IntermediariNou', IntermediariNou),
    ('/IntermediariCrea', IntermediariCrea),
    ('/IntermediariSelect', IntermediariSelect),
    ('/IntermediariEdita', IntermediariEdita), 
    ('/ClientTots', ClientTots),                #Client
    ('/ClientNou', ClientNou),
    ('/ClientCrea', ClientCrea),
    ('/ClientSelect', ClientSelect),
    ('/ClientEdita', ClientEdita),
    ('/TareaNou', TareaNou),                  #Tarea
    ('/TareaCrea', TareaCrea),
    ('/TareaSelect', TareaSelect),
    ('/TareaSelectCal', TareaSelectCal),
    ('/TareaSelectTemps', TareaSelectTemps),
    ('/TareaEdita', TareaEdita),
    ('/HistoriaNou', HistoriaNou),
    ('/HistoriaCompleta', HistoriaCompleta), 
    ('/HistoriaCrea', HistoriaCrea),            #Historia
    ('/HistoriaSelect', HistoriaSelect),
    ('/HistoriaEdita', HistoriaEdita),
    ('/IncidenciaNou', IncidenciaNou),          #Incidencia
    ('/IncidenciaCrea', IncidenciaCrea),
    ('/IncidenciaSelect', IncidenciaSelect),
    ('/IncidenciaEdita', IncidenciaEdita), 
    ('/IncidenciaTots', IncidenciaTots), 
    ('/PressupostNou', PressupostNou),          #Pressupostos
    ('/PressupostCrea', PressupostCrea),
    ('/PressupostSelect', PressupostSelect),
    ('/PressupostEdita', PressupostEdita),
    ('/ImpPressupost', ImpPressupost), 
    ('/TreballNou', TreballNou),                #Treball 
    ('/TreballSelect', TreballSelect),
    ('/TreballEdita', TreballEdita),
    ('/TreballAcceptatNo', TreballAcceptatNo),
    ('/TreballAcceptatNoPre', TreballAcceptatNoPre),
    ('/TreballCrea', TreballCrea), 
    ('/TipoTreballNou', TipoTreballNou),        #TipoTreball
    ('/TipoTreballTots', TipoTreballTots), 
    ('/TipoTreballSelect', TipoTreballSelect),
    ('/TipoTreballEdita', TipoTreballEdita),  
    ('/TipoTreballCrea', TipoTreballCrea),
    ('/CalendariInicial', CalendariInicial),    #Calendari
    ('/CalendariFiltro', CalendariFiltro),  
    ('/TareaHui', TareaHui),
    ('/TareaDema', TareaDema),
    ('/TareaDemaTarea', TareaDemaTarea),
    ('/TareaDilluns', TareaDilluns),
    ('/ProformaNou', ProformaNou),                #Proforma 
    ('/ProformaSelect', ProformaSelect),
    ('/ProformaEdita', ProformaEdita),
    ('/ProformaCrea', ProformaCrea),
    ('/ProformaElimina', ProformaElimina),
    ('/ProformaCreaPercent', ProformaCreaPercent),
    ('/ImpFactura', ImpFactura), 
    ('/MovimentInicial', MovimentInicial),        #Moviment
    ('/MovimentNouIngres', MovimentNouIngres),
    ('/MovimentNouGasto', MovimentNouGasto),
    ('/MovimentNouTraspas', MovimentNouTraspas),
    ('/MovimentSelect', MovimentSelect),
    ('/MovimentCreaIngres', MovimentCreaIngres),
    ('/MovimentCreaGasto', MovimentCreaGasto),
    ('/MovimentEdita', MovimentEdita),
    ('/MovimentElimina', MovimentElimina),  
    ('/QuadraCaixa', QuadraCaixa),  
    ('/MovimentNouIngresProf', MovimentNouIngresProf), 
    ('/CreaIngresProf', CreaIngresProf), 
    ('/PissarraInicial', PissarraInicial),        #Pissarra  
    ('/PissarraFacturacio', PissarraFacturacio),
    ('/PissarraFac', PissarraFac), 
    ('/PissarraCobro', PissarraCobro),
    ('/PissarraCobroMes', PissarraCobroMes),
    ('/PissarraFacMes', PissarraFacMes),
    ('/SelectNoPisFact', SelectNoPisFact),
    ('/SelectNoPisCob', SelectNoPisCob),
    ('/ComiInicial', ComiInicial),                 #Comi  
    ('/IntermediariComiSelect', IntermediariComiSelect),
    ('/IntermediariComiSol', IntermediariComiSol),  
    ('/IntermediariComiPagada', IntermediariComiPagada), 
    ('/IntermediariComiElimina', IntermediariComiElimina), 
    ('/TreballFacSelect', TreballFacSelect),        #treballs fac     
    ('/TreballFacNou', TreballFacNou),
    ('/TreballFacElimina', TreballFacElimina),
    ('/LiniaFacturaCrea', LiniaFacturaCrea), 
    ('/LiniaFacturaEdita', LiniaFacturaEdita),
    ('/SuplidoFacSelect', SuplidoFacSelect),        #suplidos fac     
    ('/SuplidoFacNou', SuplidoFacNou),
    ('/SuplidoFacElimina', SuplidoFacElimina),
    ('/LiniaSuplidoCrea', LiniaSuplidoCrea), 
    ('/LiniaSuplidoEdita', LiniaSuplidoEdita), 
    ('/ProformaTotsInicial', ProformaTotsInicial),   #proformaTots                    
    ('/ImprimirPresupuesto', ImprimirPresupuesto),
    ('/ImprimirFactura',ImprimirFactura),
    ('/LiniatempsInicial',LiniatempsInicial),       #Liniateps
    ('/LiniatempsTots',LiniatempsTots),
    ('/LiniatempsTreballador',LiniatempsTreballador),
    ('/LiniatempsEsquema',LiniatempsEsquema),
    ('/LiniatempsTareaSelect',LiniatempsTareaSelect),
    ('/LiniatempsTareaEdita',LiniatempsTareaEdita),
    ('/LiniatempsHistoria',LiniatempsHistoria),
    ('/LiniatempsHistoriaCrea',LiniatempsHistoriaCrea),
    ('/LiniatempsTarea',LiniatempsTarea),
    ('/LiniatempsTareaCrea',LiniatempsTareaCrea),
    ('/ControlInicial',ControlInicial),             #Control
    ('/CapsulaInicial',CapsulaInicial),             #Capsula
    ('/CapsulaNou',CapsulaNou),
    ('/CapsulaGestioNou',CapsulaGestioNou),
    ('/CapsulaElimina',CapsulaElimina),
    ('/CapsulaRepetir',CapsulaRepetir),
    ('/RolNou', RolNou),                             #Rol
    ('/RolCrea', RolCrea),
    ('/RolSelect', RolSelect),
    ('/RolEdita', RolEdita),
    ('/RolElimina', RolElimina),
    ('/RankingInicial', RankingInicial),
    ('/EliminaRanking', EliminaRanking),
    ('/ControlCapsulaInicial', ControlCapsulaInicial), #ControlCapsula
    ('/ControlCapsulaSelect', ControlCapsulaSelect),
    ('/GantInicial', GantInicial),                      #Gant
    ('/GantTareaSelect', GantTareaSelect), 
    ('/GantTareaEdita', GantTareaEdita), 
    ('/GantZoom', GantZoom), 
    ('/VacancesSelect', VacancesSelect),                #Vacances
    ('/VacancesTareaSelect', VacancesTareaSelect),
    ('/VacancesTareaNou', VacancesTareaNou),
    ('/VacancesTareaCrea', VacancesTareaCrea),  
    ('/VacancesTareaEdita', VacancesTareaEdita), 
    ('/ErrorVacances', ErrorVacances),  
    ('/TreballTabla', TreballTabla),            #TreballTabla
    ('/TreballSelectOrdre', TreballSelectOrdre), 
    ('/TreballSelectOrdreTabla', TreballSelectOrdreTabla), 
    ('/TreballEditaOrdre', TreballEditaOrdre), 
    ('/TreballEditaOrdreTabla', TreballEditaOrdreTabla), 
    ('/TreballenTablaNo', TreballenTablaNo), 
    ('/TreballadorTablaSelect', TreballadorTablaSelect), 
    ('/TreballValeva', TreballValeva), 
    ('/TreballenActiuNo', TreballenActiuNo),
    ('/FitxaOn', FitxaOn), #Fitxa
    ('/FitxaOff', FitxaOff),
    ('/VipTots', VipTots),
    ], debug=True)
