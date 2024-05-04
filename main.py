import requests
import pandas as pd
import streamlit as st
import plotly.graph_objs as go


# Función para obtener datos históricos de precios de una criptomoneda
def get_crypto_prices(id, days):
    url = f'https://api.coingecko.com/api/v3/coins/{id}/market_chart'
    params = {'vs_currency': 'usd', 'days': days}  # Número de días para los datos históricos

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df_prices = pd.DataFrame(data['prices'], columns=['time', 'price'])
        df_prices['time'] = pd.to_datetime(df_prices['time'], unit='ms')
        return df_prices
    else:
        st.error('Error al obtener el historial de precios.')


# Obtener lista de criptomonedas disponibles en CoinGecko
url_coins = 'https://api.coingecko.com/api/v3/coins/list'
response_coins = requests.get(url_coins)
if response_coins.status_code == 200:
    coins_data = response_coins.json()
    coins_list = {coin['id']: coin['name'] for coin in coins_data}
else:
    st.error('Error al obtener la lista de criptomonedas.')

# Crear el menú de selección de criptomonedas en Streamlit
selected_coin = st.selectbox('Selecciona una criptomoneda', list(coins_list.values()))

# Obtener datos históricos de precios de la criptomoneda seleccionada
days = 30  # Últimos 30 días
df_prices = get_crypto_prices(list(coins_list.keys())[list(coins_list.values()).index(selected_coin)], days)

# Crear gráfico interactivo con Plotly
if df_prices is not None:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_prices['time'], y=df_prices['price'], mode='lines', name='Precio USD'))
    fig.update_layout(title=f'Historial de Precios de {selected_coin}', xaxis_title='Fecha', yaxis_title='Precio (USD)')
    st.plotly_chart(fig)

    # Datos estadísticos en texto
    st.subheader('Datos Estadísticos')
    st.write(f"Precio Máximo: ${df_prices['price'].max():,.2f}")
    st.write(f"Precio Mínimo: ${df_prices['price'].min():,.2f}")
    st.write(f"Precio Promedio: ${df_prices['price'].mean():,.2f}")
    st.write(f"Volumen Total: ${df_prices['price'].sum():,.2f}")
else:
    st.error('No se pudieron obtener datos para la criptomoneda seleccionada.')
