import spacy
from spacy import displacy
nlp = spacy.load('es')
doc = nlp(u'''ARTÍCULO 1.-	Se encuentran comprendidos en el ámbito de este impuesto los actos jurídicos por los que se transfiera a título gratuito el dominio de bienes sujetos a registro, tales como herencias, legados, donaciones, anticipos de legítima y otros.

 

ARTÍCULO 2.-	Se presume que constituyen materia objeto del gravamen de la ley, las transferencias de dominio de los bienes indicados en el artículo 3 de este decreto supremo, en los siguientes casos:

 

Transmisiones de bienes a título oneroso a quienes sean herederos forzosos o en ausencia de éstos herederos legales del enajenante en la fecha de la transmisión.

Transmisiones de bienes a título oneroso en favor de los cónyugues de los herederos señalados en el inciso anterior.

Transmisiones de bienes a título oneroso en favor de quienes sean herederos forzosos sólo del cónyugue del enajenante, o de los cónyugues y de aquellos, en la fecha de transmisión.

Compras de bienes efectuadas a nombre de descendientes menores de edad.

Las acciones o cuotas de capital originadas en aportes de bienes registrables entregadas a herederos del aportante, en oportunidad de la constitución o aumento de capital de sociedades.

Constituye materia sometida al gravamen solamente el acervo hereditario, cuando se trate de bienes gananciales.

 

ARTÍCULO 3.-	De conformidad con el segundo párrafo del articulo 99 de la ley 843, están comprendidos en el objeto del impuesto los siguientes bienes sujetos a registro en el país:

Los vehículos automotores.

Las motonaves y aeronaves.

Los inmuebles urbanos y rurales.

Las acciones y cuotas de capital.

Derechos de propiedad científica, literaria y artística, marcas de fábrica o de comercio o similares, patentes rótulos comerciales, slogans, denominaciones de origen y otros similares relativos a. la propiedad industrial y derechos intangibles.

Otros bienes registrables a nivel nacional.

 ''')
for token in doc:
    print(token.text, token.lemma_ ,token.pos_,token.tag_,token.dep_,token.shape_,token.is_alpha,token.is_stop)
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
sentence_spans = list(doc.sents)
displacy.serve(sentence_spans, style='dep')
#displacy.serve(doc, style='dep')