# -*- coding: utf-8 -*-
from models import Pages
# Plantillas:
from django.template.loader import get_template
from django.template import Context

# Nuevo
from datetime import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from models import Usuario
from models import Alojamiento
from models import Foto
from models import Comentario
from models import FechaSeleccion
# Internet Manage
import urllib2
from django.http import HttpResponse, HttpResponseRedirect
# SAXs
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
# Loggin Loggout
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
# Plantillas:
from django.template.loader import get_template
from django.template import Context

NameGlobal = ''
DescriptionGlobal = ''
WebGlobal = ''

# ================= Clases =================
# ----------------- myContentHandlerAltLeng -----------------
class myContentHandlerAltLeng(ContentHandler):
    global DescriptionGlobal, WebGlobal, NameGlobal
    seqN = 1

    def __init__ (self):
        self.inService = False
        self.inContent = False
        self.theContent = ''
        self.newname = ''
        self.newdescription = ''
        self.newweb = ''

    def startElement (self, name, attrs):
        if name == 'service':
            self.inService = True
        elif self.inService:
            if name == 'name':
                self.inContent = True
            elif name == 'body':
                self.inContent = True
            elif name == 'web':
                self.inContent = True
            
    def endElement (self, name):
        global DescriptionGlobal, WebGlobal, NameGlobal
        if name == 'service':
            self.inService = False
        elif self.inService:
            if name == 'name':
                self.newname = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'body':
                self.newdescription = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'web':  
                self.newweb = self.theContent
                self.inContent = False
                self.theContent = ""
                if self.newname == NameGlobal:
                    print 'Encontro la traduccion'
                    print 'Nombre Durante la traduccion: ' + NameGlobal
                    DescriptionGlobal = self.newdescription
                    WebGlobal = self.newweb
                    print 'Descripcion: ' + DescriptionGlobal
                    print ''
                    print 'Web: ' + WebGlobal
                    
                    
    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
            
            


# ----------------- myContentHandler -----------------
class myContentHandler(ContentHandler): 
    seqN = 1

    def __init__ (self):
        self.inService = False
        self.inContent = False
        self.Categoria = False
        self.SubCategoria = False
        self.theContent = ''
        self.newname = ''
        self.newphone = ''
        self.newdescription = ''
        self.newweb = ''
        self.newaddress = ''
        self.newlatitude = ''
        self.newlongitude = ''
        self.AlojamientoAUX = 0
        self.newcategoria = ''
        self.newsubcategoria = ''

    def startElement (self, name, attrs):
        if name == 'service':
            self.inService = True
        elif self.inService:
            if name == 'name':
                self.inContent = True
            elif name == 'phone':
                self.inContent = True
            elif name == 'body':
                self.inContent = True
            elif name == 'web':
                self.inContent = True
            elif name == 'address':
                self.inContent = True
            elif name == 'latitude':
                self.inContent = True
            elif name == 'longitude':
                self.inContent = True
            elif name == 'url':
                self.inContent = True
            elif name == 'item':
                if (attrs.getValue(attrs.getNames()[0]) == 'Categoria'):
                    self.inContent = True
                    self.Categoria = True
                elif (attrs.getValue(attrs.getNames()[0]) == 'SubCategoria'):
                    self.inContent = True
                    self.SubCategoria = True
            
    def endElement (self, name):
        if name == 'service':
            self.inService = False
        elif self.inService:
            if name == 'name':
                self.newname = self.theContent
                self.inContent = False
                self.theContent = ""
                self.AlojamientoAUX = Alojamiento(Nombre=self.newname,id=self.seqN,\
                                                     NumeroComentarios=0)
                self.AlojamientoAUX.save()
            elif name == 'phone':
                self.newphone = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'body':
                self.newdescription = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'web':
                self.newweb = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'address':
                self.newaddress = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'latitude':
                self.newlatitude = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'longitude':
                self.newlongitude = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'url':
                FotoAUX = Foto(Alojamiento=self.AlojamientoAUX, URL=self.theContent)
                FotoAUX.save()
                self.inContent = False
                self.theContent = ""
            elif name == 'item':
                if (self.Categoria == True):
                    self.Categoria = False
                    self.newcategoria = self.theContent
                    self.inContent = False
                    self.theContent = ""
                elif (self.SubCategoria == True):
                    self.SubCategoria = False
                    self.newsubcategoria = self.theContent
                    self.inContent = False
                    self.theContent = ""
                    self.AlojamientoAUX = Alojamiento(Nombre=self.newname,id=self.seqN,\
                                            Telefono=self.newphone,\
                                            Descripcion=self.newdescription, URL= self.newweb,\
                                            Direccion=self.newaddress, NumeroComentarios=0,\
                                            Latitud = self.newlatitude,\
                                            Longitud = self.newlongitude,\
                                            Categoria=self.newcategoria,\
                                            SubCategoria=self.newsubcategoria)
                    self.AlojamientoAUX.save()
                    self.seqN += 1;

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# ================= Funciones =================
# ----------------- RetrieveEnInfo -----------------
def RetrieveLenInfo(Lenguage):
    # Este código carga el XML ingles o frances y lo parsea, guardando en las variables
    # globales DescGlobal y WebGlobal las traducciones del texto, para luego usarse en
    # vez de las españolas.
    # Solo lo hara para el nombre de alojamiento almacenado en "NameGlobal"

    # Obtencion del xml desde internet en ingles
    if Lenguage == 'en':
        f = urllib2.urlopen('http://www.esmadrid.com/opendata/alojamientos_en.xml')
    elif Lenguage == 'fr':
        f = urllib2.urlopen('http://www.esmadrid.com/opendata/alojamientos_fr.xml')
    else:
        f = urllib2.urlopen('http://www.esmadrid.com/opendata/alojamientos_es.xml')
    fBody = f.read()
    # Inicializacion del Parser
    theParser = make_parser()
    theHandler = myContentHandlerAltLeng()  # Parser alternativo para no almacenamiento
    theParser.setContentHandler(theHandler)
    # Escritura Dummy en archivo .xml
    xmlFile = open('AlojamientosLeng.xml',"w")
    xmlFile.writelines(fBody)
    xmlFile.close()
    # Apertura dummy del archivo .xml
    xmlFile = open('AlojamientosLeng.xml',"r")
    # Parse
    print ('')
    print ('Inicio del Parser Foraneo...')
    theParser.parse(xmlFile)    # Launch Parse
    xmlFile.close()
    print ('Fin del Parser Foraneo...')
    print ('')
        
# ----------------- RetrieveInfo -----------------
def RetrieveInfo():
    # Obtencion del xml desde internet
    f = urllib2.urlopen('http://www.esmadrid.com/opendata/alojamientos_es.xml')
    fBody = f.read()
    # Inicializacion del Parser
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    # Escritura Dummy en archivo .xml
    try:
        print ('Abriendo .xml ...')
        xmlFile = open('Alojamientos.xml',"r")
        fBody_aux = xmlFile.read()
        xmlFile.close()
        if fBody_aux == fBody:
            print('Iguales!!!!')
            # En realidad no hacer NADA mas...
            # Apertura dummy del archivo .xml
            #xmlFile = open('AlojamientosCorto.xml',"r")
            # Borrar base de datos vieja...
            #Alojamiento.objects.all().delete()
            #Foto.objects.all().delete()
            #Comentario.objects.all().delete()
            # Parse
            #print ('')
            #print ('Inicio del Parser...')
            #theParser.parse(xmlFile)    # Launch Parse
            #xmlFile.close()
            #print ('Fin del Parser...')
            #print ('')
        else:
            print('Distintos...')
            xmlFile = open('Alojamientos.xml',"w")
            xmlFile.writelines(fBody)
            xmlFile.close()
            # Apertura dummy del archivo .xml
            xmlFile = open('Alojamientos.xml',"r")
            # Borrar base de datos vieja...
            Alojamiento.objects.all().delete()
            Foto.objects.all().delete()
            Comentario.objects.all().delete()
            # Parse
            print ('')
            print ('Inicio del Parser...')
            theParser.parse(xmlFile)    # Launch Parse
            xmlFile.close()
            print ('Fin del Parser...')
            print ('')
    except:
        print ('No existia .xml, creando ...')
        xmlFile = open('Alojamientos.xml',"w")
        xmlFile.writelines(fBody)
        xmlFile.close()
        #xmlFile = open('Alojamientos.xml',"w")
        #xmlFile.writelines(fBody)
        #xmlFile.close()
        # Apertura dummy del archivo .xml
        xmlFile = open('Alojamientos.xml',"r")
        # Parse
        print ('')
        print ('Inicio del Parser...')
        theParser.parse(xmlFile)    # Launch Parse
        xmlFile.close()
        print ('Fin del Parser...')
        print ('')
        
# ----------------- decorateHTML -----------------
def decorateHTML (text):
    return ("<html><body>" + text + "</body></html>")

# ----------------- logger -----------------
@csrf_exempt
def logger(request):
    if request.user.is_authenticated():
        try:
            usuario = Usuario.objects.get(Nombre=request.user.username)
            print('Usuario "Loggeado"')
        except:
            usuario = Usuario(Nombre=request.user.username,\
                                TituloPagina=('Pagina de '+request.user.username),\
                                Letra=12, ColorFondo='')
            usuario.save()
            print('Usuario no Encontrado, lo creo... y "Loggeo"')
    else:
        usuario = 0
    return usuario

# ----------------- pickFotos -----------------
def pickFotos(alojamiento,limit,width,height):
    fotosAlojamiento = Foto.objects.all().filter(Alojamiento=alojamiento)
    count = 0
    respuesta = ''
    for foto in fotosAlojamiento:
        respuesta += '<br><img src="'+foto.URL+'"style="width:'+str(width)\
                  +  'px;height:'+str(height)+'px;"><br>'
        count = count + 1
        if count == limit:
            break
    return respuesta

# ----------------- entregaColor -----------------
def entregaColor(colorSust):
    # BackGround Colors and Global Text Size:
    # background: #FFF; # Blanco
    # rgba(192,192,192,0.3) # Gris
    # rgba(215, 147, 44, 0.9) # Naranja
    if (colorSust == 'naranja' or colorSust == 'Naranja'):
        color = 'rgba(215, 147, 44, 0.9)'
    elif (colorSust == 'gris' or colorSust == 'Gris'):
        color = 'rgba(192,192,192,0.3)'
    elif (colorSust == 'rojo' or colorSust == 'Rojo'):
        color = 'rgba(248,80,50,1)'
    elif (colorSust == 'verde' or colorSust == 'Verde'):
        color = 'rgba(210,255,82,1)'
    elif (colorSust == 'azul' or colorSust == 'Azul'):
        color = 'rgba(183,222,237,1)'
    elif (colorSust == 'amarillo' or colorSust == 'Amarillo'):
        color = 'rgba(255,251,41,1)'
    elif (colorSust == 'marron' or colorSust == 'Marron'):
        color = 'rgba(243,226,199,0.8)'
    elif (colorSust == 'negro' or colorSust == 'Negro'):
        color = '#000'
    else:
        color = '#FFF'
    return color


# ================= Vistas =================
# ----------------- xmlV ----------------- GET /(.*)
def xmlV(request, usuariopedido):
    print 'en xmlV GET/: ' + usuariopedido
    respuesta = '<?xml version="1.0" encoding="UTF-8"?><serviceList>'
    AlojamientosAux = Alojamiento.objects.all().filter(Usuario=usuariopedido)
    if (len(AlojamientosAux)>0):
        for alojamiento in AlojamientosAux:
            #print alojamiento.Descripcion
            respuesta += '<service>'
            respuesta += '<name>'
            respuesta += '<![CDATA['+alojamiento.Nombre+']]>'
            respuesta += '</name>'
            respuesta += '<phone>'
            respuesta += alojamiento.Telefono
            respuesta += '</phone>'
            respuesta += '<body>'
            respuesta += '<![CDATA['+alojamiento.Descripcion+']]>'
            respuesta += '</body>'
            respuesta += '<web>'
            respuesta += alojamiento.URL
            respuesta += '</web>'
            respuesta += '<address>'
            respuesta += alojamiento.Direccion
            respuesta += '</address>'
            respuesta += '<latitude>'
            respuesta += alojamiento.Latitud
            respuesta += '</latitude>'
            respuesta += '<longitude>'
            respuesta += alojamiento.Longitud
            respuesta += '</longitude>'
            respuesta += '<extradata>'
            respuesta += '<item name="Categoria">'+alojamiento.Categoria+'</item>'
            respuesta += '<item name="SubCategoria">'+alojamiento.SubCategoria+'</item>'
            respuesta += '</extradata>'
            respuesta += '</service>'
    else:
        respuesta += 'El usuario no dispone de Alojamientos'
    respuesta += '</serviceList>'
    return HttpResponse(respuesta, content_type="application/xml")

# ----------------- alojamientoIdLengTempV ----------------- GET/ y POST/
@csrf_exempt
def alojamientoIdLengTempV(request, alojamientoid, Lenguage):
    global DescriptionGlobal, WebGlobal, NameGlobal
    print 'En alojamientoIdVLen. Idioma: ' + Lenguage + '. Alojamiento: ' + alojamientoid
    usuarioLogeado = logger(request)
    
    # Datos de Alojamiento
    try:
        alojamientoPedido = Alojamiento.objects.get(id=alojamientoid)
        # Traducir: URL + Descripcion
        NameGlobal = alojamientoPedido.Nombre
        DescriptionGlobal = ''
        WebGlobal = ''
        RetrieveLenInfo(Lenguage)
        if DescriptionGlobal == '':
            DescriptionGlobal = '<p1>Alojamiento no traducido al idioma pedido.</p1><br>'
        if WebGlobal == '':
            WebGlobal = '<p1>Web no traducida al idioma pedido.</p1><br>'        
        imagenes = pickFotos(alojamientoPedido,5,500,300)
        YaComentado = 0
        # Almacena el comentario
        if request.method == 'POST':
            print 'En alojamientoIdV /POST'
            # Reconocimiento de primer y unico comentario...
            comsAux = Comentario.objects.all().filter(Alojamiento=alojamientoPedido,\
                                                   Usuario=usuarioLogeado)
            for comentario in comsAux:
                YaComentado = 1
            # Permite comentar o no, segun si este user ya a comentado antes este hotel...
            if YaComentado == 0:
                comentarioSubido = request.POST['comentario']
                if comentarioSubido != '':
                    comentarioGuardar = Comentario(Alojamiento = alojamientoPedido,\
                                                   Usuario = usuarioLogeado,\
                                                   Descripcion = comentarioSubido)
                    comentarioGuardar.save()
                    NComAux = alojamientoPedido.NumeroComentarios
                    alojamientoPedido.NumeroComentarios = NComAux+1
                    alojamientoPedido.save()
        # Comentarios
        listaComentarios = ''
        comentariosAlojamiento = Comentario.objects.all().filter(Alojamiento=alojamientoPedido)
        for comentario in comentariosAlojamiento:
            listaComentarios += '<p1>De '+comentario.Usuario.Nombre+': '\
                             +  comentario.Descripcion+'</p1><br>'
        # Comentar y  Seleccionar
        if usuarioLogeado != 0:
            if YaComentado == 0:
                comentador  = '<br><p1> Comentar: </p1>'\
                            + '<form method="POST" action="">'\
                            + '<input type="text" name="comentario"><br>'\
                            + '<input type="submit" value="Enviar">'\
                            + '</form>'\
                            + '<br><a href="http://127.0.0.1:8000/sel/'\
                            + usuarioLogeado.Nombre + '/' + alojamientoid\
                            + '"> Seleccionar</a>'
            else:
                comentador  = '<br><p1>Ya has comentado este alojamiento.</p1>'\
                            + '<br><br><a href="http://127.0.0.1:8000/sel/'\
                            + usuarioLogeado.Nombre + '/' + alojamientoid\
                            + '"> Seleccionar</a>'
        # Carga de plantillas según dicte Logger
        if usuarioLogeado == 0:
            template = get_template('alojamientoIDLen/UnLogged/index.html')
            respuesta = template.render(Context({'alojamientoPedido': alojamientoPedido,\
                                                 'imagenes': imagenes,\
                                                 'listaComentarios': listaComentarios,\
                                                 'alojamientoid': alojamientoid,\
                                                 'DescriptionGlobal': DescriptionGlobal,\
                                                 'WebGlobal': WebGlobal}))
        else:
            template = get_template('alojamientoIDLen/Logged/index.html')
            respuesta = template.render(Context({'alojamientoPedido': alojamientoPedido,\
                                                 'imagenes': imagenes,\
                                                 'usuario': usuarioLogeado.Nombre,\
                                                 'listaComentarios': listaComentarios,\
                                                 'comentador': comentador,\
                                                 'alojamientoid': alojamientoid,\
                                                 'DescriptionGlobal': DescriptionGlobal,\
                                                 'WebGlobal': WebGlobal}))
    except:
        respuesta = 'El alojamiento Pedido no existe'\
                    + '<meta http-equiv="Refresh" content="2;\
                    url=http://127.0.0.1:8000/">'
    return HttpResponse(decorateHTML(respuesta))

# ----------------- alojamientoIdTempV ----------------- GET/ y POST/
@csrf_exempt
def alojamientoIdTempV(request, alojamientoid):
    print 'En alojamientoIdV: ' + alojamientoid
    usuarioLogeado = logger(request)
    
    # Datos de Alojamiento
    try:
        alojamientoPedido = Alojamiento.objects.get(id=alojamientoid)
        imagenes = pickFotos(alojamientoPedido,5,500,300)
        YaComentado = 0
        # Almacena el comentario
        if request.method == 'POST':
            print 'En alojamientoIdV /POST'
            # Reconocimiento de primer y unico comentario...
            comsAux = Comentario.objects.all().filter(Alojamiento=alojamientoPedido,\
                                                   Usuario=usuarioLogeado)
            for comentario in comsAux:
                YaComentado = 1
            # Permite comentar o no, segun si este user ya a comentado antes este hotel...
            if YaComentado == 0:
                comentarioSubido = request.POST['comentario']
                if comentarioSubido != '':
                    comentarioGuardar = Comentario(Alojamiento = alojamientoPedido,\
                                                   Usuario = usuarioLogeado,\
                                                   Descripcion = comentarioSubido)
                    comentarioGuardar.save()
                    NComAux = alojamientoPedido.NumeroComentarios
                    alojamientoPedido.NumeroComentarios = NComAux+1
                    alojamientoPedido.save()
        # Comentarios
        listaComentarios = ''
        comentariosAlojamiento = Comentario.objects.all().filter(Alojamiento=alojamientoPedido)
        for comentario in comentariosAlojamiento:
            listaComentarios += '<p1>De '+comentario.Usuario.Nombre+': '\
                             +  comentario.Descripcion+'</p1><br>'
        # Comentar y  Seleccionar
        if usuarioLogeado != 0:
            if YaComentado == 0:
                comentador  = '<br><p1> Comentar: </p1>'\
                            + '<form method="POST" action="">'\
                            + '<input type="text" name="comentario"><br>'\
                            + '<input type="submit" value="Enviar">'\
                            + '</form>'\
                            + '<br><a href="http://127.0.0.1:8000/sel/'\
                            + usuarioLogeado.Nombre + '/' + alojamientoid\
                            + '"> Seleccionar</a>'
            else:
                comentador  = '<br><p1>Ya has comentado este alojamiento.</p1>'\
                            + '<br><br><a href="http://127.0.0.1:8000/sel/'\
                            + usuarioLogeado.Nombre + '/' + alojamientoid\
                            + '"> Seleccionar</a>'
        # Carga de plantillas según dicte Logger
        if usuarioLogeado == 0:
            template = get_template('alojamientoID/UnLogged/index.html')
            respuesta = template.render(Context({'alojamientoPedido': alojamientoPedido,\
                                                 'imagenes': imagenes,\
                                                 'listaComentarios': listaComentarios,\
                                                 'alojamientoid': alojamientoid}))
        else:
            template = get_template('alojamientoID/Logged/index.html')
            respuesta = template.render(Context({'alojamientoPedido': alojamientoPedido,\
                                                 'imagenes': imagenes,\
                                                 'usuario': usuarioLogeado.Nombre,\
                                                 'listaComentarios': listaComentarios,\
                                                 'comentador': comentador,\
                                                 'alojamientoid': alojamientoid}))
    except:
        respuesta = 'El alojamiento Pedido no existe'\
                    + '<meta http-equiv="Refresh" content="2;\
                    url=http://127.0.0.1:8000/">'
    return HttpResponse(decorateHTML(respuesta))

# ----------------- alojamientosTempV ----------------- GET/ y POST/
@csrf_exempt
def alojamientosTempV(request):
    print 'En alojamientosTempV'
    usuarioLogeado = logger(request)
    
    ListadoSeleccionado = ''
    if request.method == 'GET':
        print 'En alojamientosTempV GET/'
        # Lista Alojamientos
        Alojamientos = Alojamiento.objects.all()
        titular = 'Listado de Alojamientos:<ol>'
    elif request.method == 'POST':
        print 'En alojamientosTempV POST/'
        categoria = request.POST['categoria']
        estrellas = request.POST['estrellas']
        print categoria + ' de ' + estrellas
        if categoria != '':
            if estrellas != '':
                titular = categoria+' de '+estrellas+':<ol>'
                Alojamientos = Alojamiento.objects.all().filter(Categoria=categoria,\
                                                                SubCategoria=estrellas)
            else:
                titular = categoria+':<ol>'
                Alojamientos = Alojamiento.objects.all().filter(Categoria=categoria)
        else:
            if estrellas != '':
                titular = ' De '+estrellas+':<ol>'
                Alojamientos = Alojamiento.objects.all().filter(SubCategoria=estrellas)
            else:
                titular = 'Listado Completo de Alojamientos:<ol>'
                Alojamientos = Alojamiento.objects.all()
    else:
        titular = 'Listado de Alojamientos:<ol>'
    if usuarioLogeado == 0:
        for alojamiento in Alojamientos:
            ListadoSeleccionado += '<li>'+alojamiento.Nombre\
                      + '<br>Webs de info <a href="'+str(alojamiento.id)+'">local</a> y '\
                      + 'de <a href="'+alojamiento.URL+'"> Madrid</a>.<br><br>'
        ListadoSeleccionado += '</ol>'
    else:
        for alojamiento in Alojamientos:
            ListadoSeleccionado += '<li>'+alojamiento.Nombre\
                      + '<br>Webs de info <a href="'+str(alojamiento.id)+'">local</a> y '\
                      + 'de <a href="'+alojamiento.URL+'"> Madrid</a>.'\
                      + '<br><a href="http://127.0.0.1:8000/sel/'\
                      + usuarioLogeado.Nombre + '/' + str(alojamiento.id)\
                      + '"> Seleccionar</a><br><br>'
        ListadoSeleccionado += '</ol>'
    # Carga de plantillas según dicte Logger
    if usuarioLogeado == 0:
        template = get_template('alojamientos/UnLogged/index.html')
        respuesta = template.render(Context({'ListadoSeleccionado': ListadoSeleccionado,\
                                             'titular': titular}))
    else:
        template = get_template('alojamientos/Logged/index.html')
        respuesta = template.render(Context({'ListadoSeleccionado': ListadoSeleccionado,\
                                             'titular': titular,\
                                             'usuario': usuarioLogeado.Nombre}))
    return HttpResponse(decorateHTML(respuesta))
    
# ----------------- usuariosTempV ----------------- GET /(.*)/(.*) y POST /(.*)
@csrf_exempt
def usuariosTempV(request, usuariopedido, pagina):
    
    if request.method == 'GET':
        print 'En usuariosTempV GET/'
        if pagina == '':
            pagina = '0'
        pagina = int(pagina)
        try:
            # User Registrado. Sino Casca excepción y se reporta
            usuarioPedido = Usuario.objects.get(Nombre=usuariopedido)
            # User Loggeado? if (usuarioAuth == 0) then No Loggeado
            usuarioLogeado = logger(request)
            listaAlojamientos = ''
            # Alojamientos del usuario
            AlojamientosAux = Alojamiento.objects.all().filter(Usuario=usuarioPedido)
            buttL = ''
            buttR = ''
            if (len(AlojamientosAux)>0):
                Alojamientos = AlojamientosAux[pagina*10:min(len(AlojamientosAux),pagina*10+10)]
                # Lista de alojamientos de Usuario
                listaAlojamientos += '<h4>Mostrando de '\
                            +str(pagina*10+1)\
                            + ' a '+str(min(len(AlojamientosAux),pagina*10+10))+':</h4><ul>'
                for alojamiento in Alojamientos:
                    FechaSeleccionAux = FechaSeleccion.objects.all().filter(\
                                    Usuario=usuarioPedido, Alojamiento=alojamiento)[0]
                    listaAlojamientos += '<li>'+alojamiento.Nombre+'<br>'+alojamiento.Direccion\
                                + '<br>Seleccionado el: '+str(FechaSeleccionAux.Fecha)[0:19]
                    listaAlojamientos += pickFotos(alojamiento,1,100,60)
                    listaAlojamientos += '<a href="/alojamientos/'\
                                      + str(alojamiento.id) + '"> Mas info</a><br><br>'
                listaAlojamientos += '</ul>'
                # Botones de navegacion
                if (pagina>0):
                    buttL = '<a href="'+str(pagina-1)+'">Anterior</a>'
                if (len(AlojamientosAux)>((pagina+1)*10)):
                    buttR = '<a href="'+str(pagina+1)+'">Siguiente</a>'
            else:
                listaAlojamientos = '<br>Aun no has seleccionado alojamientos'
            # Carga de plantillas según dicte Logger
            if usuarioLogeado == 0:
                template = get_template('usuarios/UnLogged/index.html')
                respuesta = template.render(Context({'usuariopedido': usuariopedido,\
                                                     'listaAlojamientos': listaAlojamientos,\
                                                     'buttL': buttL,\
                                                     'buttR': buttR}))
            else:
                template = get_template('usuarios/Logged/index.html')
                respuesta = template.render(Context({'usuariopedido': usuariopedido,\
                                                     'listaAlojamientos': listaAlojamientos,\
                                                     'buttL': buttL,\
                                                     'buttR': buttR,\
                                                     'usuario': usuarioLogeado.Nombre}))
        except:
            respuesta = 'El usuario: '+usuariopedido+' no esta registrado...'\
                        + '<meta http-equiv="Refresh" content="2;\
                        url=http://127.0.0.1:8000/">'
    elif request.method == 'POST':
    # POST: Utilizacion en caso exclusivo de que un usaurio logeado quiera cambiar
    # su titulo de pagina o su confguracion de estilo (colo fondo y tamaño letra).
        print 'En usuarioV POST/'     
        # User Loggeado? if (usuarioAuth != 0) then Loggeado
        usuarioLogeado = logger(request)
        if usuarioLogeado != 0:
            if 'titulo' in request.POST:
                titulo = request.POST['titulo']
                if (titulo == ''):
                    usuarioLogeado.TituloPagina = 'Pagina de '+usuarioLogeado.Nombre
                else:
                    usuarioLogeado.TituloPagina = titulo
                usuarioLogeado.save()
                respuesta = '<meta http-equiv="Refresh" content="0;\
                            url=http://127.0.0.1:8000/"+usuariopedido>'
            else:
                letra = request.POST['letra']
                color = request.POST['color']
                if (letra != ''):
                    usuarioLogeado.Letra = int(letra)
                if (color != ''):
                    usuarioLogeado.ColorFondo = color
                usuarioLogeado.save()
                respuesta = '<meta http-equiv="Refresh" content="0;\
                            url=http://127.0.0.1:8000/"+usuariopedido>'
        else:
            respuesta = 'Usuario no permitido'\
                      + '<meta http-equiv="Refresh" content="2;\
                        url=http://127.0.0.1:8000/"+usuariopedido>'
    else:
        respuesta = 'Metodo no permitido...'\
                  + '<meta http-equiv="Refresh" content="2;\
                    url=http://127.0.0.1:8000/">'
    return HttpResponse(decorateHTML(respuesta))


# ----------------- seleccion ----------------- GET sel/(.*)/(.*)
def seleccion(request, usuarioNombre, alojamientoId):
    try:
        usuarioPedido = Usuario.objects.get(Nombre=usuarioNombre)
        alojamientoPedido = Alojamiento.objects.get(id=alojamientoId)
        alojamientoPedido.Usuario.add(usuarioPedido)
        try:
            FechaSeleccionAux = FechaSeleccion.objects.all().filter(\
                                Usuario=usuarioPedido, Alojamiento=alojamientoPedido)[0]
            FechaSeleccionAux2 = FechaSeleccion(Usuario=usuarioPedido,\
                                                Alojamiento=alojamientoPedido,\
                                                Fecha=datetime.now(),\
                                                id=FechaSeleccionAux.id)
            FechaSeleccionAux2.save()
        except:
            FechaSeleccionAux = FechaSeleccion(Usuario=usuarioPedido,\
                                                Alojamiento=alojamientoPedido,\
                                                Fecha=datetime.now())
            FechaSeleccionAux.save()
        print 'Usuario, alojamiento y fecha asociados'
    except:
        print ('Algo no existia... Usuario o Alojamiento o fallo en FechaSeleccion')
    return HttpResponseRedirect('http://127.0.0.1:8000/'+usuarioNombre)

# ----------------- logoutV ----------------- GET /logout
def logoutV(request):
    logout(request)
    return HttpResponseRedirect('http://127.0.0.1:8000/')

# ----------------- loginV ----------------- GET /login
@csrf_exempt
def loginV(request):
    username = request.POST['username']
    password = request.POST['password']
    usuario = authenticate(username=username, password=password)
    if usuario is None:
        decision = 'Login incorrecto.'\
                 + '<meta http-equiv="Refresh" content="4;\
                   url=http://127.0.0.1:8000/">'
    else:
        if usuario.is_active:
            login(request, usuario)
            decision = 'Login Correcto!!'\
                     + '<meta http-equiv="Refresh" content="4;\
                       url=http://127.0.0.1:8000/">'
        else:
            respuesta = 'Usuario ya NO disponible.'
    template = get_template('Loggin/index.html')
    respuesta = template.render(Context({'decision': decision}))
    return HttpResponse(decorateHTML(respuesta))

# ----------------- About ----------------- GET /about
def about(request):
    print 'En About'
    # User Control
    usuarioLogeado = logger(request)
    if usuarioLogeado == 0:
        template = get_template('about/UnLogged/index.html')
        respuesta = template.render(Context({}))
    else:
        template = get_template('about/Logged/index.html')
        respuesta = template.render(Context({'usuario': usuarioLogeado.Nombre}))
    return HttpResponse(respuesta)

# ----------------- StyleV ----------------- GET /
def StyleV(request):
    print 'Devolviendo "default.css"'
    template = get_template('default.css')
    # User Control
    usuarioLogeado = logger(request)
    # Mod Estilo
    if usuarioLogeado == 0:
        respuesta = template.render(Context({'backG': 'rgba(255, 255, 255, 1)',\
                                             'FontS': '12pt'}))
    else:
        letra = usuarioLogeado.Letra;
        color = entregaColor(usuarioLogeado.ColorFondo)
        respuesta = template.render(Context({'backG': color,\
                                             'FontS': str(letra)+'pt'}))
    return HttpResponse(content=respuesta, content_type="text/css")
    
# ----------------- StylefontV ----------------- GET /
def StylefontV(request):
    print 'Devolviendo "fonts.css"'
    template = get_template('fonts.css')
    respuesta = template.render(Context())
    return HttpResponse(content=respuesta, content_type="text/css")
    
# ----------------- homePageTemp ----------------- GET /
@csrf_exempt
def homeTemp(request):
    # User Control
    usuarioLogeado = logger(request)

    # Alojamientos Actualizados
    RetrieveInfo()
 
    # Lista Alojamientos Cargada sobre: "ListadoAlojamientos"
    ListadoAlojamientos = ''
    if usuarioLogeado == 0:
        Alojamientos = Alojamiento.objects.all().filter(NumeroComentarios__gte=1)\
                        .order_by("-NumeroComentarios")[0:10]
        ListadoAlojamientos += '<ol>'
        for alojamiento in Alojamientos:
            ListadoAlojamientos += '<li><p1>'\
				+ '<a href="'+alojamiento.URL+'"> '+alojamiento.Nombre+'</a>'\
				+ '</p1><br>'\
                                + alojamiento.Direccion
            ListadoAlojamientos += pickFotos(alojamiento,1,130,78)
            ListadoAlojamientos += '<a href="alojamientos/'\
                        + str(alojamiento.id) + '"> Mas info</a><br><br>'
        ListadoAlojamientos += '</ol>'
    else:
        Alojamientos = Alojamiento.objects.all().filter(NumeroComentarios__gte=1)\
                        .order_by("-NumeroComentarios")[0:10]
        ListadoAlojamientos += '<ol>'
        for alojamiento in Alojamientos:
            ListadoAlojamientos += '<li><p1>'\
			+ '<a href="'+alojamiento.URL+'"> '+alojamiento.Nombre+'</a>'\
			+ '</p1>'\
                        + '  --->  '\
                        + '<a href="sel/'+usuarioLogeado.Nombre+'/'+str(alojamiento.id)\
                        + '"> Seleccionar</a><br>'\
                        + alojamiento.Direccion
            ListadoAlojamientos += pickFotos(alojamiento,1,130,78)
            ListadoAlojamientos += '<a href="alojamientos/'\
                        + str(alojamiento.id) + '"> Mas info</a><br><br>'
        ListadoAlojamientos += '</ol>'

    # Lista Usuarios Cargada sobre: "ListadoUsuarios"
    ListadoUsuarios = ''
    Usuarios = Usuario.objects.all()
    ListadoUsuarios += '<ol>'
    for usuario in Usuarios:
        ListadoUsuarios += '<li>'+usuario.Nombre+' ---> <a href="'\
                    + usuario.Nombre + '">'\
                    + usuario.TituloPagina + '</a>'
    ListadoUsuarios += '</ol>'
    # Carga de plantillas según Logger
    if usuarioLogeado == 0:
        template = get_template('home/UnLogged/index.html')
        respuesta = template.render(Context({'ListadoAlojamientos': ListadoAlojamientos,\
                                             'ListadoUsuarios': ListadoUsuarios}))
    else:
        template = get_template('home/Logged/index.html')
        respuesta = template.render(Context({'ListadoAlojamientos': ListadoAlojamientos,\
                                             'usuario': usuarioLogeado.Nombre,\
                                             'ListadoUsuarios': ListadoUsuarios}))
    return HttpResponse(respuesta)
    
# ----------------- faviconV ----------------- GET /favicon.ico
def faviconV(request):
    print 'En faviconV'
    respuesta = ''
    #respuesta = '<img src="images/favicon.ico">'
    return HttpResponse(decorateHTML(respuesta))











































