import pandas as pd


def translation_dict():
    original_halias_data = pd.read_csv("data\localization.csv",
                                       usecols=[0, 2], encoding="mac_roman", sep=";")
    bird_species_fin = [bird for bird in
                        pd.read_csv("data\haliasdata-2010-2019_new.csv",
                                    index_col=0).fillna(0)]

    list_of_names_tuples = []
    list_of_names_tuples_eng = []

    for i in range(len(original_halias_data["FIN_name"])):
        list_of_names_tuples.append(original_halias_data["FIN_name"][i])

    for i in range(len(original_halias_data["ENG_name"])):
        list_of_names_tuples_eng.append(original_halias_data["ENG_name"][i])

    zipped_bird_names = set(list(zip(list_of_names_tuples, list_of_names_tuples_eng)))
    final_bird_name_tuples = [item for item in zipped_bird_names if item[0] in bird_species_fin]

    translation_dictionary = dict(final_bird_name_tuples)
    return translation_dictionary
