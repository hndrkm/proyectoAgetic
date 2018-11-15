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
´{
  "id": "1",
  "tokens": [
    {
      "id": "t1.1",
      "form": "Abuelas",
      "lemma": "abuelas",
      "tag": "NP00SP0",
      "ctag": "NP",
      "pos": "noun",
      "type": "proper",
      "neclass": "person",
      "nec": "PER"
    },
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
}´  


En este caso el resultado está en formato JSON.
Análisis de entidades
Una vez que tenemos los workers listos podemos llamar a freeling con:
from pyfreeling import Analyzer

´def tokenize(data):
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
tokens = df.map(tokenize)´  


Y luego bajamos todo a disco:
tokens.map(ujson.dumps).to_textfiles('{}.*.dat'.format(filename))


Esta tarea toma varias horas y como resultado obtendremos algunos archivos llamados: file1.dat.0.dat, file1.dat.1.dat, etc. Y su contenido será similiar a:
´{
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
}´

### Generación de una estructura de datos para guardar datos semánticos obtenidos de un texto plano 
Para la estructura de datos, se vio necesario tener un sistema de relaciones en las palabras de las oraciones 
### Almacenamiento de los datos generados  
### Extractor de información en forma de resumen de texto 
Para esta tarea se reviso el repositorio https://github.com/icoxfog417/awesome-text-summarization
 el cual explica el proceso de resumenes automaticos de texto, como tambien el siguiente repositorio https://github.com/facebookarchive/NAMAS. Como un apoyo a la documentacion el repositorio https://github.com/icoxfog417/awesome-text-summarization esmuy util.



https://docs.arangodb.com/3.2/Cookbook/Graph/ExampleActorsAndMovies.html  
https://github.com/laura-dietz/tutorial-kb4ir  
https://eprints.ucm.es/48879/1/100.pdf  
https://spacy.io/universe/?id=allennlp  
https://allennlp.org/tutorials  
http://scielo.sld.cu/scielo.php?script=sci_arttext&pid=S2227-18992013000100007  
https://github.com/d3/d3  
