import json
import argparse
from classes.downloader import Downloader 
import glob
import os

name = "dataset_dalab"

dirs = ["iiif", "iiif2"]

for dir in dirs:

    files = glob.glob("../docs/"+dir+"/*/*.json")

    manifests = []
    manifests_full = []

    for i in range(len(files)):
        if i % 10 == 0:
            print(i+1, len(files))

        file = files[i]
        with open(file) as f:
            obj = json.load(f)

        manifests.append({
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@type": "sc:Manifest",
            "@id" : obj["@id"].replace("/iiif/", "/"+dir+"/"),
            "thumbnail" : obj["thumbnail"]["@id"],
            "label" : obj["label"]        
        })

        manifests_full.append({
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@type": "sc:Manifest",
            "@id" : obj["@id"].replace("/iiif/", "/"+dir+"/"),
            "thumbnail" : obj["thumbnail"]["@id"],
            "label" : obj["label"],
            "metadata" : obj["metadata"],
            "attribution" : obj["attribution"],
            "related" : obj["related"]["@id"],
            "seeAlso" : obj["seeAlso"]["@id"],
        })

    collection_path = "../docs/"+dir+"/top.json"

    fw = open(collection_path, 'w')

    collection = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": "https://nakamura196.github.io/"+name+"/"+dir+"/top.json",
        "@type": "sc:Collection",
        "vhint": "use-thumb",
        "manifests": manifests,
    }

    json.dump(collection, fw, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

    collection_full_path = "../docs/"+dir+"/top_full.json"

    fw = open(collection_full_path, 'w')

    collection_full = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": "https://nakamura196.github.io/"+name+"/"+dir+"/top_full.json",
        "@type": "sc:Collection",
        "vhint": "use-thumb",
        "manifests": manifests_full,
    }

    json.dump(collection_full, fw, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

    

    
