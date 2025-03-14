import pandas as pd
import os 

# Cargar los datos en un DataFrame
def join_data_seasons(year):
    inputfile1 = f'data/data_csv/qb_passing_advanced_stats_{year}.csv'
    inputfile2 = f'data/data_csv/qb_red_zone_{year}.csv'
    inputfile3 = f'data/data_csv/qb_stats_{year}.csv'
    outputfile = f'data/data_csv/qb_complete_stats_season_{year}.csv'

    df = pd.read_csv(inputfile1, sep=",", encoding="utf-8")
    df_2 = pd.read_csv(inputfile2, sep=",", encoding="utf-8")
    df_3 = pd.read_csv(inputfile3, sep=",", encoding="utf-8")

    columnas = ['Player','Age','Pos','Team', 'G', 'GS','Awards','Cmp','Att']
    # Eliminar la columnas
    for col in columnas:
        if col in df.columns:
           df = df.drop(columns=[col])

    # Renombrar la columnas
    if 'Yds' in df.columns:
        df = df.rename(columns={'Yds': 'RPO_Yds'})
    if 'Plays' in df.columns:
        df = df.rename(columns={'Plays': 'RPO_Plays'})
    if 'RushAtt' in df.columns:
        df = df.rename(columns={'RushAtt': 'RPO_RushAtt'})
    if 'RushYds' in df.columns:
        df = df.rename(columns={'RushYds': 'RPO_RushYds'})
    
    # Agregar una columna 'Season'
    df['Season'] = year

    df_temp = pd.merge(df, df_2, on='Player-additional')

    df_temp = df_temp.drop(columns=['Player'])

    df_complete = pd.merge(df_3, df_temp, on='Player-additional')

    df_complete = df_complete.drop(columns=['Awards'])

    if 'Yds.1' in df_complete.columns:
        df_complete = df_complete.rename(columns={'Yds.1': 'SacksYds'})

    # Guardar como CSV
    df_complete.to_csv(outputfile, index=False, encoding="utf-8")

    print(f"✅ Archivo convertido con éxito: {outputfile}")

def join_all_data():
    # Lista para almacenar los DataFrames
    qb_dataframes = []
    for year in range(2018,2025):
        inputfile = f'data/data_csv/qb_complete_stats_season_{year}.csv'
        df = pd.read_csv(inputfile,sep=",", encoding="utf-8")
        # Agregar el DataFrame a la lista
        qb_dataframes.append(df)

    # Unir todos los DataFrames en uno solo
    qb_complete = pd.concat(qb_dataframes, ignore_index=True)

    # Reemplazar "0" con NaN en columnas numéricas
    qb_complete.replace(0, float('nan'), inplace=True)

    # Convertir columnas numéricas
    qb_complete = qb_complete.apply(pd.to_numeric, errors='ignore')

    # Guardar el DataFrame consolidado en un nuevo archivo CSV
    qb_complete.to_csv('data/qb_complete_stats.csv', index=False)

join_all_data()