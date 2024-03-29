import pandas as pd
import numpy as np
import keras.backend as K


def cargar_dataset():
    datos = pd.read_csv("dataset/nivel_procesado_1904-2023.csv")
    datos['fecha'] = pd.to_datetime(datos['fecha'])
    datos.set_index( 'fecha', inplace=True)
    datos_asuncion = datos['e218']
    datos_asuncion = datos_asuncion.interpolate(limit = 30, method ='linear', limit_direction='both')
    dataset = pd.DataFrame(datos_asuncion)
    dataset.columns = ['nivel']
    return dataset
def cargar_datasetOtherStations():
    datos = pd.read_csv("dataset/nivel_procesado_1904-2023.csv")
    datos['fecha'] = pd.to_datetime(datos['fecha'])
    datos.set_index( 'fecha', inplace=True)
    datos_asuncion = datos[[ 'e218','valor010' , 'valor088' , 'valor134' , 'valor183' , 'valor211' ,]]
    datos_asuncion = datos_asuncion.interpolate(limit = 30, method ='linear', limit_direction='both')
    dataset = pd.DataFrame(datos_asuncion)
    dataset.columns = ['nivel','valor010' , 'valor088' , 'valor134' , 'valor183' , 'valor211' ]
    return dataset


def obtener_datos_normalizados(datos_originales):
    transformados = datos_originales.copy()

    min= -0.8 #-0.55
    max= 8 #9.5
    cantidad_columnas = len(datos_originales.columns)

    for index in range (0,len(datos_originales)):
        for columna in range(0,cantidad_columnas):
            transformados.iat[index, columna] = (transformados.iat[index, columna] - min )/(max-min)

    return transformados

def obtener_datos_normalizados(datos_originales):
    transformados = datos_originales.copy()

    min= -0.8 #-0.55
    max= 8 #9.5
    cantidad_columnas = len(datos_originales.columns)

    for index in range (0,len(datos_originales)):
        for columna in range(0,cantidad_columnas):
            transformados.iat[index, columna] = (transformados.iat[index, columna] - min )/(max-min)

    return transformados

def obtener_datos_desnormalizados(datos_normalizados):
    transformados = datos_normalizados.copy()

    min= -0.8 #-0.55
    max= 8 #9.5
    cantidad_columnas = len(datos_normalizados.columns)

    for index in range (0,len(datos_normalizados)):
        for columna in range(0, cantidad_columnas):
            transformados.iat[index, columna] = transformados.iat[index, columna]*(max-min) + min

    return transformados
def ventanear_datos(tamanio_ventana, data):

    df = data.copy()

    i=tamanio_ventana
    while i > 0:
        columna_nueva= data.shift(i)
        columna_nueva.columns = [f'x_{i}']
        df = pd.concat([df, columna_nueva], axis=1)
        i = i - 1

    df = df.dropna(axis=0)

    return df
def preparar_datos(tamanio_ventana,horizonte, data):
    n_features=len(data.columns)
    x_train = np.zeros((len(data)-tamanio_ventana-horizonte+1,tamanio_ventana, n_features))
    y_train= np.zeros((len(data)-tamanio_ventana-horizonte+1, horizonte ))
    for i in range(tamanio_ventana, len(data)-horizonte +1):
        x_train[(i-tamanio_ventana), :, :] = data.iloc[(i-tamanio_ventana):(i), :]
        y_train[i-tamanio_ventana, :] = data['nivel'].iloc[(i):(i+horizonte)]
    return x_train,y_train
def preparar_datos_salto(tamanio_ventana,horizonte, data):
    n_features=len(data.columns)
    x_train = np.zeros(((len(data)-tamanio_ventana-horizonte+1)//horizonte+1,tamanio_ventana, n_features))
    y_train= np.zeros(((len(data)-tamanio_ventana-horizonte+1)//horizonte+1, horizonte ))
    for i in range(tamanio_ventana, len(data)-horizonte +1,horizonte):
        x_train[(i-tamanio_ventana)//horizonte, :, :] = data.iloc[(i-tamanio_ventana):(i), :]
        y_train[(i-tamanio_ventana)//horizonte, :] = data['nivel'].iloc[(i):(i+horizonte)]
    return x_train,y_train


def plotprediction(Prediccion,test,tamanio_ventana,horizonte):
    Y_prediction=Prediction
  

    x_val, y_val=preparar_datos(tamanio_ventana,horizonte, test)
    Y_val = y_val.reshape(-1)
    
    print('MSE:',mean_squared_error(np.array(Y_val), Y_prediction))
    print('RMSE:',np.sqrt(mean_squared_error(np.array(Y_val), Y_prediction)))
    print('R2:',r2_score(np.array(Y_val), Y_prediction))
    print('MAPE:',mean_absolute_percentage_error(np.array(Y_val), Y_prediction))
    
    df=test[['nivel']][ tamanio_ventana:]


    f, ax = plt.subplots(figsize=(15,5))
    sns.lineplot(data =df,ax=ax)
    fmt_month = mdates.MonthLocator(interval=3)
    # Minor ticks every year.
    fmt_year = mdates.YearLocator()

    ax.xaxis.set_minor_locator(fmt_month)
    # '%b' to get the names of the month
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(fmt_year)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    # fontsize for month labels
    ax.tick_params(labelsize=15, which='both')
    # create a second x-axis beneath the first x-axis to show the year in YYYY format
    sec_xaxis = ax.secondary_xaxis(-0.1)
    sec_xaxis.xaxis.set_major_locator(fmt_year)
    sec_xaxis.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Hide the second x-axis spines and ticks
    sec_xaxis.spines['bottom'].set_visible(False)
    sec_xaxis.tick_params(length=0, labelsize=15)

    ax.set_ylabel('Nivel Asunción (M)')
    ax.set_xlabel('')

    ax.set_xlim(df.index[tamanio_ventana],df.index[-1])
    j=0
    mse=[]
    maxe=[]

    for i in range(0, len(Y_prediction),horizonte):
        if(j%28==0 and (j+horizonte)<len(df)):
            mse.append(mean_squared_error(np.array(df.nivel[j:(j+horizonte)]), Y_prediction[i:i+horizonte]))
            maxe.append(max_error(np.array(df.nivel[j:(j+horizonte)]), Y_prediction[i:i+horizonte]))
            plt.plot(df.index[j:(j+horizonte)], Y_prediction[i:i+horizonte], color='red')
        j=j+1                                          

    plt.show()
