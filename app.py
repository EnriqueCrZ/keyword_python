from flask import Flask
from flask import render_template
from datetime import datetime
import math

app = Flask(__name__)

texto = ["Administración Avanzada de Bases de Datos es un curso en el que se busca llevar al estudiante más allá del paradigma de base de datos relacional y SQL que se enseña tradicionalmente en el nivel de pregrado en  las  Escuelas  de  Ingeniería.  En  este  curso  se  pretende  introducir  al  estudiante  en  temas  de  gran importancia  en  el  ámbito  de  las  bases  de  datos  como  desempeño  y  escalabilidad.  Además,  se  busca presentar al estudiante paradigmas contemporáneos y complementarios del modelo relacional, como bases de datos multidimensionales, geográficas y NoSQL"]

directorioPalabras = {}
terminoFrecuente = {}
terminoFrecuenteNormalizado = {}
terminoFrecuenteNormalizadoLista = {}

todosLosDocumentos = ''
todosLosDocumentosNoDuplicates = []

directorioDocumentosConTerminoDentro = {}

directorioDeIDFNoDuplicados = {}
directorioDeIDFNoDuplicadosLista = {}

dictOfTF_IDF = {}
dictOfTF_IDFLista = {}

for index, oracion in enumerate(texto):
    tokens = oracion.split(' ')
    directorioPalabras[index] = [(palabra,tokens.count(palabra)) for palabra in tokens]
        

for i in range(0, len(texto)):
    listaDeNoDuplicados = []
    for frecPalabra in directorioPalabras[i]:
        if frecPalabra not in listaDeNoDuplicados:
            listaDeNoDuplicados.append(frecPalabra)
        terminoFrecuente[i] = listaDeNoDuplicados
            
y=0
for i in range(0, len(texto)):
    oracion = directorioPalabras[i]
    longitudOracion = len(oracion)
    listaNormalizada = []
    for frecPalabra in terminoFrecuente[i]:
        frecNormalizada = frecPalabra[1]/longitudOracion
        terminoFrecuenteNormalizadoLista[y] = frecPalabra[0]+": "+str(frecNormalizada)
        y=y+1
        listaNormalizada.append((frecPalabra[0],frecNormalizada))
        terminoFrecuenteNormalizado[i] = listaNormalizada

for oracion in texto:
    todosLosDocumentos += oracion + ' '
    
todosLosDocumentosTokenized = todosLosDocumentos.split(' ')

#print(todosLosDocumentosTokenized)


for palabra in todosLosDocumentosTokenized:
    if palabra not in todosLosDocumentosNoDuplicates:
        todosLosDocumentosNoDuplicates.append(palabra)
        
#print(todosLosDocumentosNoDuplicates)


for index, voc in enumerate(todosLosDocumentosNoDuplicates):
    count = 0
    for oracion in texto:
        if voc in oracion:
            count += 1
    directorioDocumentosConTerminoDentro[index] = (voc, count)

#print(directorioDocumentosConTerminoDentro)

#calculate IDF

y=0
for i in range(0, len(terminoFrecuenteNormalizado)):
    listaDeIDFCalculados = []
    for palabra in terminoFrecuenteNormalizado[i]:
        for x in range(0, len(directorioDocumentosConTerminoDentro)):
            if palabra[0] == directorioDocumentosConTerminoDentro[x][0]:
                directorioDeIDFNoDuplicadosLista[y] = palabra[0]+": "+str(math.log(len(texto)/directorioDocumentosConTerminoDentro[x][1]))
                listaDeIDFCalculados.append((palabra[0],math.log(len(texto)/directorioDocumentosConTerminoDentro[x][1])))
                directorioDeIDFNoDuplicados[i] = listaDeIDFCalculados
                y=y+1

y=0
for i in range(0, len(terminoFrecuenteNormalizado)):
    listOfTF_IDF = []
    TForacion = terminoFrecuenteNormalizado[i]
    IDForacion = directorioDeIDFNoDuplicados[i]
    for x in range(0, len(TForacion)):
        dictOfTF_IDFLista[y] = TForacion[x][0]+": "+ str(TForacion[x][1]*IDForacion[x][1])
        listOfTF_IDF.append((TForacion[x][0],TForacion[x][1]*IDForacion[x][1]))
        dictOfTF_IDF[i] = listOfTF_IDF
        y=y+1

@app.route("/")
def home():
    return render_template(
        "welcome.html",
        terminoNormal=terminoFrecuenteNormalizadoLista,
        termLen = len(terminoFrecuenteNormalizadoLista),
        freqInversa=directorioDeIDFNoDuplicadosLista,
        freqInvLen= len(directorioDeIDFNoDuplicadosLista),
        tfIdf = dictOfTF_IDFLista,
        tfIdfLen = len(dictOfTF_IDFLista)
    )

@app.route("/normal-freq/")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        terminoNormal=terminoFrecuenteNormalizado
    )

if __name__ == "__main__":
    app.run()