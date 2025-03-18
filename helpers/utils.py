import os

# Constantes
TEAM_NAMES = {
    'ARI': 'Arizona Cardinals', 'ATL': 'Atlanta Falcons', 'BAL': 'Baltimore Ravens',
    'BUF': 'Buffalo Bills', 'CAR': 'Carolina Panthers', 'CHI': 'Chicago Bears',
    'CIN': 'Cincinnati Bengals', 'CLE': 'Cleveland Browns', 'DAL': 'Dallas Cowboys',
    'DEN': 'Denver Broncos', 'DET': 'Detroit Lions', 'GNB': 'Green Bay Packers',
    'HOU': 'Houston Texans', 'IND': 'Indianapolis Colts', 'JAX': 'Jacksonville Jaguars',
    'KAN': 'Kansas City Chiefs', 'LVR': 'Las Vegas Raiders', 'LAC': 'Los Angeles Chargers',
    'LAR': 'Los Angeles Rams', 'MIA': 'Miami Dolphins', 'MIN': 'Minnesota Vikings',
    'NWE': 'New England Patriots', 'NOR': 'New Orleans Saints', 'NYG': 'New York Giants',
    'NYJ': 'New York Jets', 'PHI': 'Philadelphia Eagles', 'PIT': 'Pittsburgh Steelers',
    'SFO': 'San Francisco 49ers', 'SEA': 'Seattle Seahawks', 'TAM': 'Tampa Bay Buccaneers',
    'TEN': 'Tennessee Titans', 'WAS': 'Washington Commanders', 'STL': 'St. Louis Rams',
    'RAI': 'Los Angeles Raiders', 'RAM': 'Los Angeles Rams', 'SDG': 'San Diego Chargers'
}

# Verificar existencia de imagen
def get_image_path(qb_id):
    image_path = os.path.join("data", "images", f"{qb_id}.jpg")
    return image_path if os.path.exists(image_path) else os.path.join("data", "images", "Not_found_image.jpg")

def teams(player_name, qb_data):
    # Filtrar dataset para obtener las temporadas del QB seleccionado
    qb_seasons = qb_data[qb_data["Player-additional"] == player_name]
    # Obtener los equipos únicos en los que ha jugado el QB
    qb_teams_abbr = qb_seasons["Team"].unique()
    # Convertir abreviaciones a nombres completos
    qb_teams_full = [TEAM_NAMES[abbr] for abbr in qb_teams_abbr if abbr in TEAM_NAMES]

    return qb_teams_full