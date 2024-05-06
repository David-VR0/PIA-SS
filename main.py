import requests
import streamlit as st
import plotly.graph_objs as go
import pandas as pd


# Obtener lista de criptomonedas desde la API de CoinStats
def get_crypto_data():
    url = "https://openapiv1.coinstats.app/coins?limit=40"
    headers = {"accept": "application/json", "X-API-KEY": "demo-api-key"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa
        data = response.json()
        coins_data = [(coin['name'], coin['id'], coin['symbol'], coin['icon'], coin['price'], coin['volume'], coin['marketCap'], coin['rank']) for coin in data['result']]
        return coins_data
    except requests.exceptions.RequestException as e:
        st.error(f'Error al obtener la lista de criptomonedas: {str(e)}')

# Función para obtener datos históricos de precios de una criptomoneda 
def get_crypto_prices(id, period):
    period_mapping = {
        '24 horas': '24h',
        '1 semana': '1w',
        '1 mes': '1m',
        '3 meses': '3m',
        '6 meses': '6m',
        '1 año': '1y',
        'Todo': 'all',
    }
    if period not in period_mapping:
        st.error("Período no válido. Los períodos válidos son: 24h, 1w, 1m, 3m, 6m, 1y, all")
        return None
    
    url = f'https://openapiv1.coinstats.app/coins/{id}/charts?period={period_mapping[period]}'
    headers = {"accept": "application/json", "X-API-KEY": """api secreta dd"""}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa
        data = response.json()
        df_prices = pd.DataFrame(data, columns=['time', 'price_usd', 'status', 'volume'])  # Asegúrate de que los nombres de las columnas sean correctos
        df_prices['time'] = pd.to_datetime(df_prices['time'], unit='s')  # Ajusta el formato de tiempo según los datos
        return df_prices
    except requests.exceptions.RequestException as e:
        st.error(f'Error al obtener el historial de precios: {str(e)}')

# Crear el menú de selección de criptomonedas en Streamlit
coins_data = get_crypto_data()
selected_coin, selected_coin_icon = st.selectbox('Selecciona una criptomoneda', [(coin_data[0], coin_data[3]) for coin_data in coins_data], format_func=lambda x: x[0])


# Mostrar el icono de la criptomoneda seleccionada
st.image(selected_coin_icon, width=100)


# Agregar menú de selección de período
selected_period = st.selectbox('Selecciona un período', ['24 horas', '1 semana', '1 mes', '3 meses', '6 meses', '1 año', 'Todo'])

# Obtener datos históricos de precios de la criptomoneda seleccionada
df_prices = get_crypto_prices([coin_data[1] for coin_data in coins_data if coin_data[0] == selected_coin][0], selected_period)

# Crear gráfico interactivo con Plotly
if df_prices is not None:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_prices['time'], y=df_prices['price_usd'], mode='lines', name='Precio USD'))
    fig.update_layout(title=f'Historial de Precios de {selected_coin}', xaxis_title='Fecha', yaxis_title='Precio (USD)')
    st.plotly_chart(fig)
   
    # Datos estadísticos en texto
    st.subheader('Datos Estadísticos')
    st.write(f"Precio Máximo: ${df_prices['price_usd'].max():,.2f}")
    st.write(f"Precio Mínimo: ${df_prices['price_usd'].min():,.2f}")
    st.write(f"Precio Promedio: ${df_prices['price_usd'].mean():,.2f}")
    st.write(f"Volumen Total: ${df_prices['price_usd'].sum():,.2f}")
else:
    st.error('No se pudieron obtener datos para la criptomoneda seleccionada.')

# Crear tabla de criptomonedas
st.subheader('Tabla de Criptomonedas')
df_coins = pd.DataFrame(coins_data, columns=['Nombre','ID' ,'Símbolo', 'icon', 'Precio Actual', 'Volumen (USD)', 'Capitalización de Mercado', 'Ranking'])
df_coins = df_coins.drop(columns=['ID'])
df_coins = df_coins.drop(columns=['icon'])
st.table(df_coins.sort_values(by='Ranking'))
# Crear gráfico interactivo con Plotly para el volumen de transacciones
if df_prices is not None:
    fig_volume = go.Figure()
    fig_volume.add_trace(go.Bar(x=df_prices['time'], y=df_prices['volume'], name='Volumen de Transacciones', marker_color='blue'))
    fig_volume.update_layout(title=f'Volumen de Transacciones de {selected_coin}', xaxis_title='Fecha', yaxis_title='Volumen')
    st.plotly_chart(fig_volume)

# Calcular el cambio porcentual
if df_prices is not None:
    df_prices['price_change_percent'] = df_prices['price_usd'].pct_change() * 100

    # Crear gráfico interactivo con Plotly para el cambio porcentual
    fig_percent_change = go.Figure()
    fig_percent_change.add_trace(go.Scatter(x=df_prices['time'], y=df_prices['price_change_percent'], mode='lines', name='Cambio Porcentual', line=dict(color='green')))
    fig_percent_change.update_layout(title=f'Cambio Porcentual de {selected_coin}', xaxis_title='Fecha', yaxis_title='Cambio Porcentual')
    st.plotly_chart(fig_percent_change)

