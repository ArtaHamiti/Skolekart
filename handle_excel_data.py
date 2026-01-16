import numpy as np
import pandas as pd

# df = pd.read_csv("privatskoler_vgs_med_manuell_fiks.csv")
# df = df.sort_values(by="Navn")
# df.to_csv("privatskoler_vgs_med_manuell_fiks_sortert.csv", index=False)

# pd.read_excel("Kopi av Private skoler i drift høst 2025 til KD.xlsx").to_csv("private_vgs_godkjente_etter_privatskoleloven_per_2025.csv", index=False)

# Vil lage kode som går gjennom csv-filene for private vgs og grunnskoler og fjerner de radene som ikke har et organisasjonsnummer som er i en annen csv-fil

def filter_private_schools(private_schools_csv, list_csv1, filter_csv2, output_csv):
    all_orgs = pd.read_csv(list_csv1)["Orgnummer"].astype(str).tolist()
    private_schools_df = pd.read_csv(private_schools_csv)
    filter_df = pd.read_csv(filter_csv2)
    for orgnr in filter_df["Orgnummer"]:
        all_orgs.append(orgnr)

    filter_org_numbers = set(all_orgs)
    added_schools = []
    left_out_schools = []
    for school_row in private_schools_df.iterrows():
        school_orgnr = str(school_row[1]["Organisasjonsnummer"])
        if school_orgnr in filter_org_numbers:
            added_schools.append(school_row)
        else:
            i = input(f"Skole {school_row[1]['Navn']} med orgnr {school_orgnr} ikke i liste. Ta med? (j/n) ")
            if i.lower() == "j":
                added_schools.append(school_orgnr)
                print(f"Tok med skole {school_row[1]['Navn']} med orgnr {school_orgnr}")
            else:
                left_out_schools.append(school_orgnr)
                print(f"Tok ikke med skole {school_row[1]['Navn']} med orgnr {school_orgnr}")
    output_df = private_schools_df[private_schools_df["Organisasjonsnummer"].astype(str).isin([str(school[1]["Organisasjonsnummer"]) for school in added_schools])]
    output_df.to_csv(output_csv, index=False)
    print("Skoler som ikke kom med med:", left_out_schools)

filter_private_schools("privatskoler_vgs.csv", "underenheter_privatskoler_per_2025.csv", "privatskoler_godkjente_etter_privatskoleloven_per_2025.csv", "privatskoler_vgs_godkjente_etter_privatskoleloven_per_2025.csv")