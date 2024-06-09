#------------------------------------------DESCRIPCIÓN-----------------------------------------------#                                       
# El módulo se encarga interpolar los datos faltantes y visualizar los datos.                        #
# -Parámetros:                                                                                       #
#   dataset -> Columnas con los datos de la fecha (objet) y nivel (float)                            #
#   fecha_col -> Etiqueta de la columna de la fecha (str)                                            #
#   nivel_vol -> Etiqueta de la columna del nivel (str)                                              #
#   periodo_anios -> Periodo a graficar (int)                                                        #
#   cantidad_periodos -> Cantidad de gráficos (int)                                                  #
#   temporalidad -> Formato en el que se encuentra los datos de la fecha (str). Ejemplo: '%Y-%m-%d'  #
#   start_year -> Año en el que comenzará el gráfico                                                 #
#   start_month -> Mes en el que comenzará el gráfico                                                #
#   start_day -> Día en el que comenzará el gráfico                                                  #
######################################################################################################

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def level_interpolate_plot(dataset, fecha_col, nivel_col, periodo_anios, cantidad_periodos, temporalidad, start_year, start_month=1, start_day=1):
    dataset[fecha_col] = pd.to_datetime(dataset[fecha_col], format=temporalidad) # Convierte la columna de la fecha a tipo datetime
    df = dataset.set_index(fecha_col) # Define un dataframe con la fecha indexada 
    df = df.interpolate(limit = 35, method = 'quadratic', limit_direction = 'both') # Interpola los datos de niveles 
    start_date = pd.Timestamp(year=start_year, month=start_month, day=start_day) # Define la fecha de inicio (tipo de dato datetime)
    for _ in range(cantidad_periodos): # Bucle que se encarga en realizar la cantidad de ploteos elegido
        period_start = start_date # Define la fecha de inicio del ploteo del periodo actual
        period_end = start_date + pd.DateOffset(years=periodo_anios) - pd.DateOffset(days=1) # Calculo de la fecha final del ploteo del periodo actual
        df_period = df[period_start:period_end] # Filtro de los datos para el ploteo del periodo actual
        if df_period.empty: # Condición para la detección del ploteo
            break
        max_level = df_period[nivel_col].max() # Identifica el nivel máximo del periodo actual
        min_level = df_period[nivel_col].min() # Identifica el nivel mínimo del periodo actual
        max_date = df_period[nivel_col].idxmax() # Identifica el indice (la fecha) del nivel máximo del periodo actual
        min_date = df_period[nivel_col].idxmin() # Identifica el indice (la fecha) del nivel mínimo del periodo actual
        fig, ax = plt.subplots(figsize=(14, 7)) # Crea la figura en conjunto con los ejes
        ax.plot(df_period.index, df_period[nivel_col], label='Caudal de Concepción', color='blue') # Plot de los niveles del periodo actual
        ax.plot(max_date, max_level, 'ro', label=f'Pico más alto: {max_level:.2f}m ({max_date.date()})') # Plot del nivel máximo del periodo actual
        ax.plot(min_date, min_level, 'go', label=f'Pico más bajo: {min_level:.2f}m ({min_date.date()})') # Plot del nivel mínimo del periodo actual
        
        #-----CONFIGURACIONES EXTRAS PARA MEJORAR LA VISUALIZACIÓN EN EL PLOT------#
        #
        # Añade títulos y etiquetas
        ax.set_title(f'Periodo ({period_start.year}-{period_end.year})')
        ax.set_ylabel('Caudal [m^3/s]')
        ax.legend()
        #
        # Añade grid
        ax.grid(True)
        #
        # Añade grid para cada mes
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        ax.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')
        #
        # Formatea el eje de fechas
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        #
        #------------------------FIN DE LAS CONFIGURACIONES-------------------------#                
        
        plt.show() # Muestra la gráfica
        start_date = period_end + pd.DateOffset(days=1) # Actualiza la fecha de inicio para el siguiente periodo a plotear