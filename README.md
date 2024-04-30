# PIA-SS
Proyecto Servicio Social 2024

Información financiera de criptomonedas: Crypto API | CoinLore
Esta API proporciona datos públicos y gratuitos sobre criptomonedas. 

Endpoints que ofrece:

/api/global/: Obtiene estadísticas globales sobre criptomonedas, como el número total de monedas, capitalización de mercado, dominancia de BTC, volumen de negociación total, capitalización de mercado ATH, entre otros datos.
/api/tickers/: Recupera datos de tick para múltiples criptomonedas, ordenadas por capitalización de mercado. Los datos incluyen detalles como nombre, ID, símbolo, precio, cambio de precio, capitalización de mercado, volumen y suministro para cada criptomoneda.
/api/ticker/{ID}: Recupera datos de tick para una criptomoneda específica, proporcionando su ID obtenida a través del endpoint /api/tickers/. Los datos son similares a los del endpoint anterior, pero para una sola criptomoneda.
/api/coin/markets/?id={ID}: Obtiene los principales 50 exchanges y mercados para una criptomoneda específica.
/api/exchanges/: Obtiene información sobre todos los exchanges listados en la plataforma.
/api/exchange/?id={ID}: Obtiene información detallada sobre un exchange específico utilizando su ID obtenido a través del endpoint anterior.
/api/coin/social_stats/?id={ID}: Proporciona estadísticas sociales, incluyendo datos de Twitter y Reddit, para una criptomoneda específica.

Análisis estadísticos:

Calcular el precio promedio de las criptomonedas.
Analizar la volatilidad de los precios.
Identificar las criptomonedas con mayor volumen de operaciones.
Estudiar la correlación entre los precios de diferentes criptomonedas.
Para generar gráficas, podríamos:

Crear gráficas de barras para comparar precios o volúmenes de operaciones.
Generar gráficas de líneas para visualizar tendencias históricas.
Utilizar gráficas de dispersión para analizar la relación entre dos variables, como precio y volumen.