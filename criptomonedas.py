import requests
import pandas as pd


class Criptomoneda:
    def __init__(self):
        self.api_key = "demo-api-key"
        self.url_base = "https://openapiv1.coinstats.app/coins"

    def obtener_lista(self):
        url = f"{self.url_base}?limit=40"
        headers = {"accept": "application/json", "X-API-KEY": self.api_key}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()["result"]
            return [(coin["name"], coin["id"], coin["symbol"], coin["icon"], coin["price"], coin["volume"], coin["marketCap"], coin["rank"]) for coin in data]
        except requests.exceptions.RequestException as e:
            return None

    def obtener_precios(self, id, periodo):
        periodo_mapping = {
            '24 horas': '24h',
            '1 semana': '1w',
            '1 mes': '1m',
            '3 meses': '3m',
            '6 meses': '6m',
            '1 año': '1y',
            'Todo': 'all',
        }
        if periodo not in periodo_mapping:
            return None
        
        url = f"{self.url_base}/{id}/charts?period={periodo_mapping[periodo]}"
        headers = {"accept": "application/json", "X-API-KEY": self.api_key}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            df_precios = pd.DataFrame(data, columns=['time', 'price_usd', 'status', 'volume'])
            df_precios['time'] = pd.to_datetime(df_precios['time'], unit='s')
            return df_precios
        except requests.exceptions.RequestException as e:
            return None