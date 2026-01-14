import requests
import pandas as pd
import json

# API-url'er
url_all_schools = "https://data-nsr.udir.no/v4/enheter"
base_url_info_schools = "https://data-nsr.udir.no/v4/enhet/"

# Hent alle privatskole-organisasjonsnumre
all_data = []
try:  
    first_response = requests.get(url_all_schools)
    start_side = first_response.json()["Sidenummer"]
    pages_total = first_response.json()["AntallSider"]
    for i in range(start_side, pages_total + 1):
        response_page = requests.get(url_all_schools, params={"Sidenummer":i})
        response_page.raise_for_status()
        data = response_page.json()
        all_data.append(data["EnhetListe"])
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

all_data_flat = [item for sublist in all_data for item in sublist]
df = pd.DataFrame(all_data_flat)

# Lag ulike dataframes basert på hva som skal filtreres
privatskoler_vgs = df[(df["ErVideregaaendeSkole"] == True) & (df["ErPrivatskole"] == True) & (df["ErAktiv"] == True)]
offentlige_skoler_vgs = df[(df["ErVideregaaendeSkole"] == True) & (df["ErPrivatskole"] == False) & (df["ErAktiv"] == True)]
nedlagte_privatskoler_vgs = df[(df["ErVideregaaendeSkole"] == True) & (df["ErPrivatskole"] == True) & (df["ErAktiv"] == False)]
nedlagte_offentlige_skoler_vgs = df[(df["ErVideregaaendeSkole"] == True) & (df["ErPrivatskole"] == False) & (df["ErAktiv"] == False)]
# nedlagte offentlige skoler og nye privatskoler i samme kart
private_grunnskoler = df[(df["ErGrunnskole"] == True) & (df["ErPrivatskole"] == True) & (df["ErAktiv"] == True)]
offentlige_grunnskoler = df[(df["ErGrunnskole"] == True) & (df["ErPrivatskole"] == False) & (df["ErAktiv"] == True)]

# Hent ut koordinatene til skolene via organisasjonsnummer - gør denne om til generell funksjon som henter utfra df-ene over og gjør om til csv

def get_coordinates(base_url_info_schools: str, filtered_df: pd.DataFrame, new_file_name: str) -> pd.DataFrame:
    res = pd.DataFrame(columns=["Navn", "Lengdegrad", "Breddegrad"])
    count = 0
    for school_id in filtered_df.loc[:, "Organisasjonsnummer"]:
        try:
            response_school = requests.get(base_url_info_schools + str(school_id))
            #print(f"Response Status Code: {response_school.status_code}")
            response_school.raise_for_status()  # Raise an error for bad status codes
            data = response_school.json()
            koordinater = data.get("Koordinat")
            lengdegrad = koordinater.get("Lengdegrad")
            breddegrad = koordinater.get("Breddegrad")
            res = pd.concat([res, pd.DataFrame({"Navn": [data.get("Navn")], "Lengdegrad": [lengdegrad], "Breddegrad": [breddegrad]})], ignore_index=True)
            count += 1
            print(f"La til skole nummer {count} av {len(filtered_df)}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching school info: {e}")
    res.to_csv(new_file_name, index=False)
    return res


#get_coordinates(base_url_info_schools, privatskoler_vgs, "privatskoler_vgs.csv")         
#get_coordinates(base_url_info_schools, private_grunnskoler, "private_grunnskoler.csv")     
#get_coordinates(base_url_info_schools, offentlige_skoler_vgs, "offentlige_vgs")
#get_coordinates(base_url_info_schools, offentlige_grunnskoler, "offentlige_grunnskoler")