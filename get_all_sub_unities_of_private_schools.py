import numpy as pd
import pandas as pd
import requests

def get_all_sub_unities_of_private_schools():
    sub_unity_list = []
    count = 0
    file = pd.read_csv("privatskoler_godkjente_etter_privatskoleloven_per_2025.csv")
    for overordnet_orgnr in file["Orgnummer"]:
        count += 1
        print(f"Henter underenheter for orgnr: {overordnet_orgnr}, nr: {count} av {len(file)}")
        brønnøysund_api_url = f"https://data.brreg.no/enhetsregisteret/api/underenheter?overordnetEnhet={overordnet_orgnr}"
        r = requests.get(brønnøysund_api_url)
        if r.status_code != 200:
            print(f"Feil ved henting av data for orgnr {overordnet_orgnr}: {r.status_code}")
            continue
        data = r.json()
        for unity in data.get("_embedded", {}).get("underenheter", []):
            sub_unity_list.append(unity["organisasjonsnummer"])
    return pd.DataFrame(sub_unity_list, columns=["Orgnummer"])

get_all_sub_unities_of_private_schools().to_csv("underenheter_privatskoler_per_2025.csv", index=False)