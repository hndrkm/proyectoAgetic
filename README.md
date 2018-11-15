# proyectoAgetic 

Herramientas para utilizar que no se tomaron en cuenta por ser incompleta o difícil de manipular o customizar para el proyecto deseado.  
#### Lemur Toolkit
https://www.lemurproject.org/  
Es una herramienta completa tanto para la investigación como la producción que ayuda en una gran medida a la búsqueda de documentos para ello, pero la herramienta tiene sus limitaciones como no permitir utilizar de manera sencilla su módulo nlp para poder encargarnos de la persistencia de consulta sencillas. 
#### Chatbot con ai y npl
https://github.com/alfredfrancis/ai-chatbot-framework/  
La herramienta ofrece una implementación rápida para la generación de una interfaz conversacional esto para facilitar la implantación, pero el problema encontrado es su difícil integración de un aprendizaje basado en documentos largos ya que los modelos que presenta evalúan textos cortos como las conversaciones de un chat.  


------------------------
Los pasos o módulos sugeridos para el desarrollo son:
### Procesamiento de lenguaje natural  
Para realizar el proceso se tomo en cuenta las herramientas de freeling, spacy y fastText.  
##### fastText
FastText es una biblioteca de código abierto, gratuita y ligera que permite a los usuarios aprender representaciones de texto y clasificadores de texto. Funciona en hardware estándar, genérico. Más tarde, los modelos pueden reducirse de tamaño para adaptarse incluso a dispositivos móviles.  
Para la instalación:  
´$ git clone https://github.com/facebookresearch/fastText.git´
´$ cd fastText´
´$ make´
Para la prueba de palabras incrustadas de fastText  
./fasttext skipgram -input data/fil9 -output result/fil9
el resultado del entrenamiento no supervisado es el siguiente  
´$ ls -l result
-rw-r-r-- 1 bojanowski 1876110778 978480850 Dec 20 11:01 fil9.bin
-rw-r-r-- 1 bojanowski 1876110778 190004182 Dec 20 11:01 fil9.vec´  
Para evaluar palabras se entiende que hay 2 métodos 
Para palabras sueltas
´$ echo "leyes" | ./fasttext print-word-vectors result/fil9.bin´
Para palabras continuas
´$ ./fasttext nn result/fil9.bin  
Pre-computing word vectors... done.´
un ejemplo de salida es el siguiente
´Query word? asparagus´
´beetroot 0.812384´
´tomato 0.806688´
´horseradish 0.805928´
´spinach 0.801483´
´licorice 0.791697´
´lingonberries 0.781507´
´asparagales 0.780756´
´lingonberry 0.778534´
´celery 0.774529´
´beets 0.773984´  
##### Freeling
Para freeling empezamos con   
sudo apt-get update -yq  
sudo apt-get install gdebi -yq  
sudo apt-get install libboost-regex-dev libicu-dev zlib1g-dev \  
                     libboost-system-dev libboost-program-options-dev \  
                     libboost-thread-dev -yq  

wget https://github.com/TALP-UPC/FreeLing/releases/download/4.0/freeling-4.0-trusty-amd64.deb   sudo gdebi -n freeling-4.0-trusty-amd64.deb   


Para probarlo, necesitamos conocer la ubicación de los archivos de configuración:  
+ En Debian: /usr/share/freeling/config/  
Luego podemos ejecutar:  
$ export FREELINGSHARE=/usr/local/Cellar/freeling/4.0/share/freeling/  
$ echo "Hola mundo" | analyzer -f /usr/local/Cellar/freeling/4.0/share/freeling/config/es.cfg  
Hola hola I 1  
mundo mundo NCMS000 1  
Y, como en este caso queremos el módulo nec de named entity classification, tendremos que correr:  
$ echo "Abuelas encontró al nieto número 114" | analyze -f \  
/usr/local/Cellar/freeling/4.0/share/freeling/config/es.cfg --nec --output json  


Nuestro output será:  
`{`  
  `"id": "1",`  
  `"tokens": [  
    {
      "id": "t1.2",  
      "form": "encontr\u00f3",  
      "lemma": "encontrar",  
      "tag": "VMIS3S0",  
      "ctag": "VMI",  
      "pos": "verb",  
      "type": "main",  
      "mood": "indicative",  
      "tense": "past",  
      "person": "3",  
      "num": "singular"  
    },  
    {  
      "id": "t1.3",  
      "form": "a",  
      "lemma": "a",  
      "tag": "SP",
      "ctag": "SP",
      "pos": "adposition",
      "type": "preposition"
    },  
    {  
      "id": "t1.4",  
      "form": "el",
      "lemma": "el",
      "tag": "DA0MS0",
      "ctag": "DA",
      "pos": "determiner",
      "type": "article",
      "gen": "masculine",
      "num": "singular"
    },
    {
      "id": "t1.5",
      "form": "nieto",
      "lemma": "nieto",
      "tag": "NCMS000",
      "ctag": "NC",
      "pos": "noun",
      "type": "common",
      "gen": "masculine",
      "num": "singular"
    },
    {
      "id": "t1.6",  
      "form": "n\u00famero",  
      "lemma": "n\u00famero",  
      "tag": "NCMS000",  
      "ctag": "NC",  
      "pos": "noun",  
      "type": "common",  
      "gen": "masculine",  
      "num": "singular"  
    },  
    {   
      "id": "t1.7",  
      "form": "114",  
      "lemma": "114",  
      "tag": "Z",  
      "ctag": "Z",  
      "pos": "number"  
    }  
  ]  
}`  


En este caso el resultado está en formato JSON.  
Análisis de entidades  
Una vez que tenemos los workers listos podemos llamar a freeling con:  
from pyfreeling import Analyzer  

`def tokenize(data):  
    try:  
        analyzer = Analyzer(config='/usr/share/freeling/config/es-ar.cfg')  
        tokens = []  
        xml_root = analyzer.run(data['parsedText'].encode('utf-8'), 'nec')  
        for element in xml_root.iter():  
            if element.tag == 'token':  
                tokens.append(dict(element.attrib))  
    except Exception as e:  
        print(data['idTramite'])  
        print(e)  

    return {'idTramite': data['idTramite'], 'tokens': tokens}  
tokens = df.map(tokenize)`    


Y luego bajamos todo a disco:  
`tokens.map(ujson.dumps).to_textfiles('{}.*.dat'.format(filename))`  


Esta tarea toma varias horas y como resultado obtendremos algunos archivos llamados: file1.dat.0.dat, file1.dat.1.dat, etc. Y su contenido será similiar a:  
`{
  "idTramite": "100000",
  "tokens": [
    {
      "ctag": "NP",
      "form": "MINISTERIO_DE_TRABAJO",
      "neclass": "organization",
      "pos": "noun",
      "nec": "ORG",
      "lemma": "ministerio_de_trabajo",
      "tag": "NP00O00",
      "type": "proper",
      "id": "t1.1"
    },
    {
      "ctag": "Fc",
      "form": ",",
      "pos": "punctuation",
      "lemma": ",",
      "tag": "Fc",
      "type": "comma",
      "id": "t1.2"
  },
  ...
  ]
}`  
##### Spacy  
Esta librería de análisis de texto está más especializado en el desarrollo, así que la producción de aplicaciones es sencilla y la adecuada para este tipo de proyectos.    
Para datos en español:  
`import spacy  
from spacy.lang.es.examples import sentences  
nlp = spacy.load('es_core_news_sm')
doc = nlp(sentences[0])
print(doc.text)
for token in doc:
    print(token.text, token.pos_, token.dep_)`

Para la tokenización y el análisis semántico
`import spacy

nlp = spacy.load('es_core_web_sm')
doc = nlp(u'Texto a analizar')

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop)`
Para el módulo de reconocimiento de entidades nombradas

`import spacy

nlp = spacy.load('es_core_web_sm')
doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)`

Para la comparación de palabras 
`import spacy
nlp = spacy.load('en_core_web_md')  # make sure to use larger model!
tokens = nlp(u'dog cat banana')
for token1 in tokens:
   for token2 in tokens:
       print(token1.text, token2.text, token1.similarity(token2))`


### Generación de una estructura de datos para guardar datos semánticos obtenidos de un texto plano 
#### Relaciones Semánticas
Para la estructura de datos, se vio necesario tener un sistema de relaciones en las palabras de las oraciones y la oraciones de los textos para una búsqueda simple y rápida.
`var oraciones = db._create("oraciones");  
var palabras = db._create("palabras");  
var relacionesPalOra = db._createEdgeCollection("relacionesPalOra");  
var relText = db._create("relText");  
var Texto = db._create("Texto");  
var CPE =Texto.save({_key: "CPE", title:'', creado:1999,tipo:''”})._id;  
var Bolivia =palabra.save({text,lema,pos,tag,dep,shape,alpha,stop})._id;  
var sentence1 = oraciones.save({text,lema,pos,tag})._id;  
relacionesPalOra.save(CPE, Bolivia, {roles: ["rol"]});  
 relText.save(sentece1, Bolivia, {roles: [""]});`  
#### Palabras incrustadas o vectores de palabras.
Se guardarán como archivos .bin o .vec de cada documento.
### Almacenamiento de los datos generados  
Para el almacenamiento de datos generados por Spacy, freling o fastText
En la parte de palabras incrustadas no es necesario una persistencia en la base de datos por que se guarda en archivos.
Para los generados por relaciones semánticas es necesario convertir las relaciones en grafos semánticos para su almacenamiento mediante la librería grafeno https://github.com/agarsev/grafeno .
Grafeno
Biblioteca de Python para la extracción de gráficos conceptuales de texto, operación y linealización. Se proporciona un servicio web integrado.
Esta biblioteca sigue siendo un trabajo en progreso, pero ya ha demostrado ser útil para varias aplicaciones, por ejemplo, el resumen de texto extractivo.
Requerimientos
python > = 3.4  
Los paquetes de Python para el uso de la biblioteca se enumeran en requirements.txt. Recomendamos utilizar conda para instalar grafeno y sus dependencias en un entorno virtual.  
Un analizador de dependencia. Por ahora, los siguientes son compatibles:  
spaCy (recomendado)  
freeling  
Si usa el simplenlglinealizador, un javaejecutable tendrá que estar disponible.  
También puede necesitar algunos datos NLTK, por ejemplo, 'wordnet' y 'wordnet_ic'. Se pueden descargar en python con:  
importar nltk  
nltk.download ([ ' wordnet ' , ' wordnet_ic ' ])  


### Extractor de información en forma de resumen de texto   
Para esta tarea se reviso el repositorio https://github.com/icoxfog417/awesome-text-summarization  
 el cual explica el proceso de resumenes automaticos de texto, como tambien el siguiente repositorio https://github.com/facebookarchive/NAMAS. Como un apoyo a la documentacion el repositorio https://github.com/icoxfog417/awesome-text-summarization esmuy util.


Para mas informacion
https://eprints.ucm.es/48879/1/100.pdf
http://scielo.sld.cu/scielo.php?script=sci_arttext&pid=S2227-18992013000100007  

