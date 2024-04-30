import tkinter as tk
from tkinter import messagebox, Toplevel
import requests


class CryptoAPIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto API App")

        # Crear menú
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Submenú Consultas Web
        self.consultas_web_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.consultas_web_menu.add_command(label="Global Stats", command=self.consultar_global_stats)
        self.consultas_web_menu.add_command(label="Top Coins", command=self.consultar_top_coins)
        self.consultas_web_menu.add_command(label="Exchange Info", command=self.consultar_exchange_info)

        # Agregar submenú Consultas Web al menú principal
        self.menu_bar.add_cascade(label="Consultas Web", menu=self.consultas_web_menu)

        # Agregar opciones al menú principal
        self.menu_bar.add_command(label="Generar Reporte", command=self.generar_reporte)
        self.menu_bar.add_command(label="Analisis Estadistico", command=self.analisis_estadistico)
        self.menu_bar.add_command(label="Generar Grafica", command=self.generar_grafica)
        self.menu_bar.add_command(label="Salir", command=self.salir)

        # Crear un cuadro de texto para mostrar resultados
        self.textbox = tk.Text(self.root, height=20, width=60)
        self.textbox.pack(pady=10)

    def consultar_global_stats(self):
        # Consultar API para Global Stats y mostrar los resultados
        url = 'https://api.coinlore.net/api/global/'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            self.mostrar_datos(data)
        else:
            messagebox.showerror("Error", "Error en la consulta al API")

    def consultar_top_coins(self):
        # Consultar API para Top Coins y mostrar los resultados
        url = 'https://api.coinlore.net/api/tickers/'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()['data']
            self.mostrar_datos(data)
        else:
            messagebox.showerror("Error", "Error en la consulta al API")

    def consultar_exchange_info(self):
        # Consultar API para Exchange Info y mostrar los resultados
        url = 'https://api.coinlore.net/api/exchanges/'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            self.mostrar_datos(data)
        else:
            messagebox.showerror("Error", "Error en la consulta al API")

    def generar_reporte(self):
        # Generar un reporte de ejemplo
        reporte = "Ejemplo de reporte:\n\n1. Bitcoin: $50000\n2. Ethereum: $2000\n3. Binance Coin: $300\n"
        self.mostrar_datos(reporte)

    def analisis_estadistico(self):
        # Realizar análisis estadístico de ejemplo
        estadisticas = "Estadísticas de ejemplo:\n\nPromedio: $10000\nDesviación estándar: $5000\n"
        self.mostrar_datos(estadisticas)

    def generar_grafica(self):
        # Generar una gráfica de ejemplo
        grafica = "Aquí iría la generación de la gráfica\n"
        self.mostrar_datos(grafica)

    def salir(self):
        # Cerrar la aplicación
        self.root.destroy()

    def mostrar_datos(self, datos):
        # Mostrar los datos en el cuadro de texto
        self.textbox.delete(1.0, tk.END)
        self.textbox.insert(tk.END, datos)


# Inicializar la aplicación
root = tk.Tk()
app = CryptoAPIApp(root)
root.mainloop()