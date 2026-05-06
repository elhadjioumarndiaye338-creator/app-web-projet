import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="Système d'Information Géographique", layout="wide")

st.title("📍 Application de Cartographie Interactive")
st.subheader("Analyse des infrastructures et du réseau routier")

# Fonction pour charger les données
@st.cache_data
def load_data(file_path):
    try:
        gdf = gpd.read_file(file_path)
        # S'assurer que le CRS est en WGS84 pour Folium
        if gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs(epsg=4326)
        return gdf
    except Exception as e:
        return None

# Liste de vos fichiers
files = {
    "Arrêts": "Arrêts.shp",
    "Axes de sorties": "Axes de sorties.shp",
    "Axes d'entrées": "Axes d'entrées.shp",
    "Dégâts routiers": "Dégats routiers.shp",
    "Écoles": "école.shp",
    "Hôpitaux": "hopitaux.shp",
    "Intersections": "Intersections.shp",
    "Itinéraires AFTU": "Itinéraires réseau aftu.shp",
    "Sapeurs Pompiers": "pompier sapeur.shp",
    "Stations Service": "station service.shp"
}

# Sidebar pour le filtrage
st.sidebar.header("Couches thématiques")
selected_layers = []
for label, path in files.items():
    if st.sidebar.checkbox(label, value=True):
        selected_layers.append((label, path))

# Initialisation de la carte centrée sur la zone d'étude
m = folium.Map(location=[14.7167, -17.4677], zoom_start=13, control_scale=True)

# Ajout des couches à la carte
for label, path in selected_layers:
    data = load_data(path)
    if data is not None:
        # Style spécifique selon le type de donnée
        color = "blue"
        if "Dégâts" in label: color = "red"
        elif "Hôpitaux" in label or "Pompiers" in label: color = "orange"
        elif "Écoles" in label: color = "green"
        
        folium.GeoJson(
            data,
            name=label,
            tooltip=folium.GeoJsonTooltip(fields=[data.columns[0]], aliases=["Info:"]),
            style_function=lambda x, color=color: {'color': color, 'weight': 3, 'fillOpacity': 0.5}
        ).add_to(m)

folium.LayerControl().add_to(m)

# Affichage de la carte
folium_static(m, width=1000, height=600)

# Statistiques rapides
st.write("### Résumé des données affichées")
cols = st.columns(3)
for i, (label, path) in enumerate(selected_layers):
    data = load_data(path)
    if data is not None:
        cols[i % 3].metric(label, f"{len(data)} entités")