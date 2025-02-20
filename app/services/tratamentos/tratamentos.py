
from app.models.banco.variaveis import Variaveis
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
