"""
Requisição de dados
"""
import requests

class CoinsAPI:
    """
    Class request data
    """
    def request_uri(date, base):
        """
        Função para obter o retorno de dados da API.
        """
        url = "https://api.vatcomply.com/rates"
        try:
            response = requests.request("GET", "{0}?date={1}&base={2}".format(url, date, base))
            if 199 > response.status_code or response.status_code < 299:
                print(f"Request to API Successful: {response.status_code}")
                res = response.json()

                return res
            else:
                valorproapi_error = (
                    f"Request to APInfailed: {response.status_code} - {response.text}"
                )
                raise Exception(valorproapi_error)
        except:
            connection_error = f"Error connection: {response.status_code} - {response.text}"
            raise Exception(connection_error)
