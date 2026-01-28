import numpy as np
import pandas as pd

# df = pd.read_csv("privatskoler_vgs_med_manuell_fiks.csv")
# df = df.sort_values(by="Navn")
# df.to_csv("privatskoler_vgs_med_manuell_fiks_sortert.csv", index=False)

# pd.read_excel("Kopi av Private skoler i drift høst 2025 til KD.xlsx").to_csv("private_vgs_godkjente_etter_privatskoleloven_per_2025.csv", index=False)

# Vil lage kode som går gjennom csv-filene for private vgs og grunnskoler og fjerner de radene som ikke har et organisasjonsnummer som er i en annen csv-fil

def filter_private_schools(private_schools_csv, list_csv1, filter_csv2, output_csv_file_name):
    all_orgs = pd.read_csv(list_csv1, comment="#")["Orgnummer"].astype(str).tolist()
    private_schools_df = pd.read_csv(private_schools_csv, comment="#")
    filter_df = pd.read_csv(filter_csv2, comment="#")
    for orgnr in filter_df["Orgnummer"]:
        all_orgs.append(orgnr)

    filter_org_numbers = set(all_orgs)
    added_schools = pd.DataFrame()
    left_out_schools = pd.DataFrame()
    for _, school_row in private_schools_df.iterrows():
        school_orgnr = str(school_row["Organisasjonsnummer"]).strip()
        school_name = school_row["Navn"]
        if school_orgnr in filter_org_numbers:
            added_schools = pd.concat([added_schools, school_row.to_frame().T], ignore_index=True)  
        else:
            i = input(f"{school_name} med orgnr: {school_orgnr} er ikke i listen. Ta med? (j/n) ")
            if i.lower() == "j":
                added_schools = pd.concat([added_schools, school_row.to_frame().T], ignore_index=True)
                print(f"Tatt med!")
            else:
                left_out_schools = pd.concat([left_out_schools, school_row.to_frame().T], ignore_index=True)
                print(f"Utelatt!")
    added_schools.to_csv(output_csv_file_name, index=False)
    print("Skoler som ikke kom med med:", left_out_schools)

#filter_private_schools("privatskoler_vgs_med_manuell_fiks_og_organisasjonsnummer.csv", "underenheter_privatskoler_per_2025.csv", "alle_privatskoler_godkjente_etter_privatskoleloven_per_2025.csv", "privatskoler_vgs_godkjente_etter_privatskoleloven_per_2025.csv")
filter_private_schools("private_grunnskoler_med_manuell_fiks_og_organisasjonsnummer.csv", "underenheter_privatskoler_per_2025.csv", "alle_privatskoler_godkjente_etter_privatskoleloven_per_2025.csv", "private_grunnskoler_godkjente_etter_privatskoleloven_per_2025.csv")

""" vgs_og_grskole = pd.merge(pd.read_csv("privatskoler_vgs_godkjente_etter_privatskoleloven_per_2025.csv"), pd.read_csv("private_grunnskoler_godkjente_etter_privatskoleloven_per_2025.csv"), how = "outer", on="Organisasjonsnummer")
pd.merge(vgs_og_grskole, pd.read_csv("alle_privatskoler_godkjente_etter_privatskoleloven_per_2025.csv"), how="left", on="Organisasjonsnummer", indicator=True).to_csv("skoler_vi_har_som_ikke_er_i_all_listen.csv", index=False)
pd.merge(vgs_og_grskole, pd.read_csv("alle_privatskoler_godkjente_etter_privatskoleloven_per_2025.csv"), how="right", on="Organisasjonsnummer", indicator=True).to_csv("skoler_i_all_listen_som_mangler_i_de_to_mine_lister.csv", index=False) """