import numpy as np
import folium as fm
import pandas as pd

Norway_coords = [59.9127, 10.7461]
# Lage et kart over Norge
m = fm.Map(location=Norway_coords, zoom_start=7)

# Lag ulike grupper
private_vgs = fm.FeatureGroup(name="Private videregående skoler")
offentlige_vgs = fm.FeatureGroup(name="Offentlige videregående skoler", show=False)
private_grunnskoler = fm.FeatureGroup(name="Private grunnskoler")
offentlige_grunnskoler = fm.FeatureGroup(name="Offentlige grunnskoler", show=False)

# Generell funksjon for å legge til data fra csv-fil til en FeatureGroup
def add_csv_to_feature_group(csv_file_name: str, feature_group: fm.FeatureGroup, icon_colour: str, icon_name: str):
    df = pd.read_csv(csv_file_name, comment="#")
    for _, row in df.iterrows():
        fm.Marker(
            location=[row["Breddegrad"], row["Lengdegrad"]],
            popup=row["Navn"],
            icon=fm.Icon(color=icon_colour, icon = icon_name, prefix="fa") # Velg herfra: https://fontawesome.com/icons?d=gallery
        ).add_to(feature_group)

add_csv_to_feature_group("privatskoler_vgs_med_manuell_fiks.csv", private_vgs, "blue", "graduation-cap")
add_csv_to_feature_group("offentlige_vgs_med_manuell_fiks.csv", offentlige_vgs, "green", "graduation-cap")
add_csv_to_feature_group("private_grunnskoler_med_manuell_fiks.csv", private_grunnskoler, "blue", "school")
add_csv_to_feature_group("offentlige_grunnskoler_med_manuell_fiks.csv", offentlige_grunnskoler, "green", "school")

# Legg gruppen til kartet
private_vgs.add_to(m)
offentlige_vgs.add_to(m)
private_grunnskoler.add_to(m)
offentlige_grunnskoler.add_to(m)

# Legg til lagkontroll
fm.LayerControl().add_to(m)

m.save("Norgeskart_med_private_og_offentlige_vgs_og_grunnskoler.html")
