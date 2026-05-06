import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="SIG Hann Bel-Air", layout="wide")

st.title("📍 Application SIG - Hann Bel-Air")
st.subheader("Gestion des infrastructures et du réseau routier")

# Fonction optimisée pour charger les données
@st.cache_data
def load_data(file_path):
    try:
        gdf = gpd.read_file(file_path)
        if gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs(epsg=4326)
        return gdf
    except Exception as e:
        return None

# Dictionnaire mis à jour avec TOUS vos fichiers
files = {
    "Limites de la Commune": "commune.shp",
    "Réseau Routier Hann Bel-Air": "routes hann bel air.shp",
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

# Sidebar pour le contrôle des couches
st.sidebar.header("Paramètres d'affichage")
selected_layers = []
for label, path in files.items():
    # On coche par défaut la commune et les routes
    default_value = True if label in ["Limites de la Commune", "Réseau Routier Hann Bel-Air"] else False
    if st.sidebar.checkbox(label, value=default_value):
        selected_layers.append((label, path))

# Centrage de la carte sur Hann Bel-Air
m = folium.Map(location=[14.7167, -17.4333], zoom_start=14, control_scale=True)

# Boucle d'affichage des couches
for label, path in selected_layers:
    data = load_data(path)
    if data is not None:
        # Personnalisation des styles
        style = {'weight': 2, 'fillOpacity': 0.1}
        
        if "Commune" in label:
            style = {'color': 'black', 'weight': 3, 'dashArray': '5, 5', 'fillOpacity': 0}
        elif "Routes" in label:
            style = {'color': 'gray', 'weight': 1.5}
        elif "Dégâts" in label:
            style = {'color': 'red', 'weight': 4}
        elif "AFTU" in label:
            style = {'color': 'blue', 'weight': 2.5}
            
        folium.GeoJson(
            data,
            name=label,
            style_function=lambda x, s=style: s,
            tooltip=folium.GeoJsonTooltip(fields=[data.columns[0]], aliases=["Détail :"])
        ).add_to(m)

folium.LayerControl().add_to(m)

# Affichage Web
folium_static(m, width=1100, height=700)

# Section Statistiques
st.sidebar.markdown("---")
st.sidebar.write("### Statistiques des données")
for label, path in selected_layers:
    data = load_data(path)
    if data is not None:
        st.sidebar.info(f"**{label}**: {len(data)} éléments")