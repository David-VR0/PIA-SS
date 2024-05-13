import streamlit as st
import plotly.graph_objs as go
import pandas as pd
from criptomonedas import Criptomoneda
import plotly.io as pio


class App:
    def __init__(self):
        self.criptomoneda = Criptomoneda()
        self.datos_moneda = self.criptomoneda.obtener_lista()

    def mostrar_menu(self):
        coin_seleccionado, coin_seleccionado_icon = st.selectbox('Selecciona una criptomoneda', [(coin_data[0], coin_data[3]) for coin_data in self.datos_moneda], format_func=lambda x: x[0])
        st.image(coin_seleccionado_icon, width=100)
        periodo_seleccionado = st.selectbox('Selecciona un período', ['24 horas', '1 semana', '1 mes', '3 meses', '6 meses', '1 año', 'Todo'])
        return coin_seleccionado, periodo_seleccionado
    
    
    def run(self):
        coin_seleccionado, periodo_seleccionado = self.mostrar_menu()
        df_precios = self.criptomoneda.obtener_precios([coin_data[1] for coin_data in self.datos_moneda if coin_data[0] == coin_seleccionado][0], periodo_seleccionado)

        if df_precios is not None:
            # Plotly chart
            figura = go.Figure()
            figura.add_trace(go.Scatter(x=df_precios['time'], y=df_precios['price_usd'], mode='lines', name='Precio USD'))
            figura.update_layout(title=f'Historial de Precios de {coin_seleccionado}', xaxis_title='Fecha', yaxis_title='Precio (USD)')
            st.plotly_chart(figura)
            

            # Estadisticas en texto
            st.subheader('Datos Estadísticos')
            st.write(f"Precio Máximo: ${df_precios['price_usd'].max():,.2f}")
            st.write(f"Precio Mínimo: ${df_precios['price_usd'].min():,.2f}")
            st.write(f"Precio Promedio: ${df_precios['price_usd'].mean():,.2f}")
            st.write(f"Volumen Total: ${df_precios['price_usd'].sum():,.2f}")

        else:
            st.error('No se pudieron obtener datos para la criptomoneda seleccionada.')
        # Crear tabla de criptomonedas
        st.subheader('Tabla de Criptomonedas')
        df_monedas = pd.DataFrame(self.datos_moneda, columns=['Nombre','ID' ,'Símbolo', 'icon', 'Precio Actual', 'Volumen (USD)', 'Capitalización de Mercado', 'Ranking'])
        df_monedas = df_monedas.drop(columns=['ID'])
        df_monedas = df_monedas.drop(columns=['icon'])
        st.table(df_monedas.sort_values(by='Ranking'))
        if st.button("Guardar Tabla"):
            df_monedas.to_csv("tabla_criptomonedas.csv", index=False)
            st.success("Tabla guardada correctamente")
        # Crear gráfico interactivo con Plotly para el volumen de transacciones
        if df_precios is not None:
            figura_volumen = go.Figure()
            figura_volumen.add_trace(go.Bar(x=df_precios['time'], y=df_precios['volume'], name='Volumen de Transacciones', marker_color='blue'))
            figura_volumen.update_layout(title=f'Volumen de Transacciones de {coin_seleccionado}', xaxis_title='Fecha', yaxis_title='Volumen')
            st.plotly_chart(figura_volumen)
        # Calcular el cambio porcentual
        if df_precios is not None:
            df_precios['price_change_percent'] = df_precios['price_usd'].pct_change() * 100

            # Crear gráfico interactivo con Plotly para el cambio porcentual
            figura_cambio_porcentual = go.Figure()
            figura_cambio_porcentual.add_trace(go.Scatter(x=df_precios['time'], y=df_precios['price_change_percent'], mode='lines', name='Cambio Porcentual', line=dict(color='green')))
            figura_cambio_porcentual.update_layout(title=f'Cambio Porcentual de {coin_seleccionado}', xaxis_title='Fecha', yaxis_title='Cambio Porcentual')
            st.plotly_chart(figura_cambio_porcentual)
            
        #Boton para guardar las imagenes
        if st.button("Guardar Imágenes"):
            pio.write_image(figura_volumen, "graficaVolumen.jpg", format="jpg")
            pio.write_image(figura_cambio_porcentual, "graficaVolumen.jpg", format="jpg")
            pio.write_image(figura, "graficaPrecios.jpg", format="jpg")
            st.success("Imágenes guardadas correctamente")
if __name__ == "__main__":
    app = App()
    app.run()