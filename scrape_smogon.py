import lxml
from lxml import html
import pandas as pd
import requests
import re
import ast
import json

#Scraped from Smogon

def flatten(a_list):
    if a_list == []:
        return None
    return a_list[0]

def main():
    response = requests.get("https://www.smogon.com/dex/sm/formats/uber/")
    cleaned_response = response.text.replace('\x00', '')
    parser = html.fromstring(cleaned_response)
    
    pokemon_dat = parser.__getitem__(0)
    content = pokemon_dat.text_content().replace("\n","").strip()
    filt_content = content[content.find("{"):]
    pokes = json.loads(filt_content)
    pokemon = pokes["injectRpcs"][1][1]

    raw_df = pd.io.json.json_normalize(pokemon["pokemon"])
    
    example = raw_df["alts"].apply(flatten)[0]
    
    raw_df[list(example.keys())] = pd.DataFrame(raw_df["alts"].apply(flatten).apply(pd.Series))
    
    df = raw_df.drop("alts",axis = 1)
    df[["Type1","Type2"]] = pd.DataFrame(df["types"].tolist(),columns = ["Type1","Type2"])
    df["formats"] = df["formats"].apply(flatten)
    df["evos"] = df["evos"].apply(flatten)
    df = df.drop(["types"],axis=1)

    df.to_csv("smogon.csv", index=False)


if __name__ == "__main__":
    main()
