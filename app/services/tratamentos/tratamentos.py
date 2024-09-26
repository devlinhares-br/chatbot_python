
from app.models.banco.variaveis import Variaveis
from app.models.banco.motivos import Motivos
from app import npl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# Adiciona variaveis na string

def get_variaveis(dialog_id):
    resultados = {}
    variaveis = Variaveis.query.filter_by(dialog_id=dialog_id).all()
    for variavel in variaveis:
        resultados.update(variavel.var_to_dict())
    return resultados
        
def substituir_variaveis(template:str, variaveis:dict):

    matches = re.findall(r'{{(.*?)}}', template)

    for match in matches:
        if match in variaveis:
            template = template.replace(f'{{{{{match}}}}}', variaveis[match])

    return template

# Seleciona motivos com base no nivel de similariedade de uma string

def select_motivo(message:str) -> list:
    if not isinstance(message, str):
        raise TypeError(f'\'message\' deve ser uma str e não {type(message)}')
    
    motivos = Motivos.query.all()

    motivos = [motivo.to_dict() for motivo in motivos]
    frases_semelhantes = []

    motivos = __preprocess_text(motivos)

    for motivo in motivos:
        similariedade = __calcular_similaridade(motivo['motivo'], message)

        if similariedade >= 0:
            motivo['similariedade'] = round(similariedade, 5)
            frases_semelhantes.append(motivo)
    
    frases_semelhantes = sorted(frases_semelhantes, key=lambda x: x['similariedade'], reverse=True)

    return frases_semelhantes

def __calcular_similaridade(frase1, frase2):
    doc1 = npl(frase1)
    doc2 = npl(frase2)

    return doc1.similarity(doc2) * 100

def __preprocess_text(frases: list):
    for frase in frases:
        frase['motivo'] = re.sub(r'\(.*?\)', '', frase['motivo']).strip()
        frase['motivo'] = re.sub(r'[^a-zA-Z0-9\s\ç\ã\õ\é]', '', frase['motivo']).strip()

        tokens = word_tokenize(frase['motivo'], language='portuguese')

        stop_words = set(stopwords.words('portuguese'))
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        frase['motivo'] = ' '.join(filtered_tokens)
    
    return frases