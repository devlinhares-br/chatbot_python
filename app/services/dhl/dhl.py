from os import getenv
import requests


class DHL():
    __BASE_URL = 'https://dhl.runteccorp.com/apiprod/hodieapiisapi.dll/dhl/mondelez/'
    # __BASE_URL = 'https://dhl.runteccorp.com/apiqa/hodieapiisapi.dll/dhl/mondelez/'
    __USER = getenv('DHL_USER')
    __PASSWD = getenv('DHL_PASSWD')
    __SUCESSO = [200, 201]
    __BLACKLIST = [2, 3, 6, 7, 10, 16, 17,
                   23, 41, 42, 50, 59, 83, 84, 266, 500]

    def __init__(self) -> None:
        self.__data = {}
        self.motivos = []

    def get_motivos(self) -> None:
        payload = {}
        try:
            response = requests.post(
                f'{self.__BASE_URL}ocorrencia/motivos', json=payload, auth=(self.__USER, self.__PASSWD))
        except requests.HTTPError:
            return {'message': 'Erro na requisição HTTP'}
        except requests.JSONDecodeError:
            return {'message': 'Erro ao decodificar o JSON'}
        except requests.ConnectionError:
            return {'message': 'Erro na conexão'}
        except requests.ConnectTimeout:
            return {'message': 'Excedeu o limite de tempo da requisição'}

        if response.status_code in self.__SUCESSO:
            return self.__filtro_motivos(response.json())
        else:
            return {}

    def __filtro_motivos(self, data: dict) -> dict:
        if not isinstance(data, dict):
            raise TypeError(
                f"\'data\' deve ser um dicionário.\nO tipo passado foi \'{type(data)}\'")
        if 'motivos' not in data:
            raise NameError('Não há motivos')
        motivos = []
        for motivo in data.get('motivos', []):
            if motivo['codigo'] not in self.__BLACKLIST:
                motivos.append(motivo)
        data['motivos'] = motivos
        return data
    
    def cria_ocorrencia(self, data:list) -> dict:
        payload = {'notas': data}
        print(payload)
        try:
            response = requests.post(
                f'{self.__BASE_URL}ocorrencia/insertlista', json=payload, auth=(self.__USER, self.__PASSWD))
        except requests.HTTPError:
            return {'message': 'Erro na requisição HTTP'}
        except requests.JSONDecodeError:
            return {'message': 'Erro ao decodificar o JSON'}
        except requests.ConnectionError:
            return {'message': 'Erro na conexão'}
        except requests.ConnectTimeout:
            return {'message': 'Excedeu o limite de tempo da requisição'}

        if response.status_code in self.__SUCESSO:
            return response.json()
        else:
            return {}

    def get_veiculo(self, tipo, perfil):
        """Veiculos
            Type: dict
                tipo:
                    type: dict
                    perfil: id_veiculo
        """
        veiculos = {
            '1': { # Refrigerados
                '1': 11, # Fiorino
                '2': 17, # 3/4
                '3': 10, # Vuc/Van
                '4': 8, # Toco
                '5': 9, # Truck
                '6': 7, # Carreta
                '7': 12 # Bi-Trem
            },
            '2': { # Seco
                '1': 5, # Fiorino
                '2': 16, # 3/4
                '3': 4, # Vuc/Van
                '4': 8, # Toco
                '5': 2, # Truck
                '6': 1, # Carreta
                '7': 6 # Bi-Trem
            },
            '3': {# Elétrico Seco
                '1': 18, # Fiorino
                '2': 18, # 3/4
                '3': 18, # Vuc/Van
                '4': 18, # Toco
                '5': 18, # Truck
                '6': 18, # Carreta
                '7': 18 # Bi-Trem
            },
            '4': {# Elétrico Refrigerado
                '1': 19, # Fiorino
                '2': 19, # 3/4
                '3': 19, # Vuc/Van
                '4': 19, # Toco
                '5': 19, # Truck
                '6': 19, # Carreta
                '7': 19 # Bi-Trem
            }

        }
        return veiculos[str(tipo)][str(perfil)]