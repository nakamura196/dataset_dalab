import json
import argparse
import yaml
from classes.downloader import Downloader 
import glob
import os

f = open("settings.yml", "r+")
settings = yaml.load(f)

prefix = settings["github_pages_url"]

docs_dir = "../docs"

def get_sets():
    sets = {}
    files = glob.glob(docs_dir + "/omeka/item_sets/*.json")
    for file in files:
        with open(file, 'r') as f:
            df = json.load(f)
            title = df["dcterms:title"][0]["@value"]
            id = df["o:id"]
            sets[id] = title

    return sets

def get_manifest(uuid):
    file = docs_dir + "/iiif/item/"+uuid+"/manifest.json"
    if os.path.exists(file):
        with open(file, 'r') as f:
            df = json.load(f)
        return df
    else:
        return None

def create_collection(label, data):
    manifests = []
    for obj in data:
        if "manifest" in obj:
            manifest = obj["manifest"]
            mdata = {
                "@id" : manifest["@id"],
                "label" : manifest["label"],
                "metadata" : manifest["metadata"]
            }

            if "license" in manifest:
                mdata["license"] = manifest["license"]

            if "thumbnail" in manifest:
                mdata["thumbnail"] = manifest["thumbnail"]

            manifests.append(mdata)
    return {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": prefix + "/collections/"+label+"/image/collection.json",
        "@type": "sc:Collection",
        "label": label,
        "manifests": manifests,
        "vhint": "use-thumb"
    }

def create_ld(data):
    lds = []
    for obj in data:
        lds.append(obj["ld"])
    return lds

item_map = {}

files = glob.glob(docs_dir + "/ld/*.json")
for file in files:
    with open(file, 'r') as f:
        df = json.load(f)

        uuid = file.split("/")[-1].replace(".json", "")
        oid = df["o:id"]
        manifest = get_manifest(uuid)

        for obj in df["o:item_set"]:
            iset_id = obj["o:id"]
            if iset_id not in item_map:
                item_map[iset_id] = []

            item = {
                "id" : oid,
                "ld" : df
            }

            if manifest != None:
                item["manifest"] = manifest

            item_map[iset_id].append(item)

sets = get_sets()
for iset_id in sorted(item_map):
    obj = item_map[iset_id]
    title = sets[iset_id]

    odir = docs_dir + "/collections/" + title
    dirs = ["image", "metadata"]
    for dir in dirs:
        os.makedirs(odir+"/"+dir, exist_ok=True)

    collection = create_collection(title, obj)
    fw = open(odir+"/image/collection.json", 'w')
    json.dump(collection, fw, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))
    
    ld = create_ld(obj)
    fw = open(odir+"/metadata/data.json", 'w')
    json.dump(ld, fw, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

    

    
