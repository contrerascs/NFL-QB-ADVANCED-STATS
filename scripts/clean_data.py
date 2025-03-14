import pandas as pd

def clean_data(year):
    input_txt = f"data/data_txt/qb_red_zone_{year}.txt"
    output_csv = f"data/data_csv/qb_red_zone_{year}.csv"

    # Leer el archivo TXT y eliminar las primeras 5 filas
    with open(input_txt, "r", encoding="utf-8") as file:
        lines = file.readlines()[5:]  # Omitimos las primeras 5 líneas
    
    # Guardar las líneas procesadas en un nuevo archivo temporal sin encabezado incorrecto
    clean_txt = "temp_cleaned.txt"
    with open(clean_txt, "w", encoding="utf-8") as file:
        file.writelines(lines)
    
    # Cargar los datos en un DataFrame
    df = pd.read_csv(clean_txt, sep=",", encoding="utf-8")

    if df.columns[-1] != "Player-additional":
        df = df.rename(columns={df.columns[-1]: "Player-additional"})

    # Filtrar solo jugadores con posición 'QB'
    #df = df[df['Pos'] == 'QB']

    # Filtrar solo jugadores con mas de 100 atts
    df = df[df['Att'] >= 10]

    # Eliminar la última fila del DataFrame
    df = df[:-1]

    # Eliminar la columna 'Link' si existe
    if 'Link' in df.columns:
        df = df.drop(columns=['Link'])

    if 'Tm' in df.columns:
        df = df.drop(columns=['Tm'])

    # Identificar columnas duplicadas
    new_columns = []
    section_map = {
        'Cmp': 'Inside_20', 'Att': 'Inside_20', 'Cmp%': 'Inside_20', 'Yds': 'Inside_20', 'TD': 'Inside_20', 'Int': 'Inside_20',
        'Cmp.1': 'Inside_10', 'Att.1': 'Inside_10', 'Cmp%.1': 'Inside_10', 'Yds.1': 'Inside_10', 'TD.1': 'Inside_10', 'Int.1': 'Inside_10'
    }

    for col in df.columns:
        if col in section_map:
            new_columns.append(f"{section_map[col]}_{col.replace('.1', '')}")
        else:
            new_columns.append(col)

    # Renombrar columnas
    df.columns = new_columns
    
    # Guardar como CSV
    df.to_csv(output_csv, index=False, encoding="utf-8")

    print(f"✅ Archivo convertido con éxito: {output_csv}")

for year in range(2018,2025):
    clean_data(year)