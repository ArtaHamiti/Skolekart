import numpy as np
import folium as fm
import pandas as pd

Norway_coords = [59.9127, 10.7461]
# Lage et kart over Norge
m = fm.Map(location=Norway_coords, zoom_start=7)

# Lag ulike grupper
private_skoler = fm.FeatureGroup(name="Private skoler")
offentlige_skoler = fm.FeatureGroup(name="Offentlige skoler")
private_grunnskoler = fm.FeatureGroup(name="Private grunnskoler")

df = pd.read_csv("privatskoler_vgs.csv", comment="#")
for _, row in df.iterrows():
    fm.Marker(
        location=[row["Breddegrad"], row["Lengdegrad"]],
        popup=row["Navn"],
        icon=fm.Icon(color="blue", icon="graduation-cap", prefix="fa")
    ).add_to(private_skoler)

df = pd.read_csv("private_grunnskoler.csv", comment="#")
for _, row in df.iterrows():
    fm.Marker(
        location=[row["Breddegrad"], row["Lengdegrad"]],
        popup=row["Navn"],
        icon=fm.Icon(color="blue", icon="school", prefix="fa")
    ).add_to(private_grunnskoler)

# Legg gruppen til kartet
private_skoler.add_to(m)
private_grunnskoler.add_to(m)

# Legg til lagkontroll
fm.LayerControl().add_to(m)

m.save("norgeskart_med_private_vgs_manuelt_fylt_inn_for_0_verdier_og_private_grunnskoler.html")
