import json
import argparse
from classes.downloader import Downloader 
import glob
import os

name = "dataset_dalab"

files = glob.glob("../docs/iiif/*/*.json")

prefix = "https://diyhistory.org/public/dalab"
prefix2 = "https://nakamura196.github.io/dataset_dalab"

def conv(value):
    return value.replace(prefix, prefix2) + ".json"

def conv2(obj):

    id = obj["@id"]
    oid = id.split("/iiif-img/")[1].split("/")[0]
    mfile = "../docs/api/media/"+oid+".json"
    with open(mfile) as f:
        media = json.load(f)
    original_url = media["o:original_url"]
    original_url = original_url.replace(prefix, prefix2)
    obj["@id"] = original_url
    del obj["service"]



    return obj

def conv3(obj, original_url):
    obj["@id"] = original_url.replace("/original/", "/medium/")
    del obj["service"]
    return obj

manifests = []
manifests_full = []

for i in range(len(files)):
    if i % 10 == 0:
        print(i+1, len(files))

    file = files[i]
    with open(file) as f:
        obj = json.load(f)

    id = obj["@id"]
    id = id.replace(prefix, prefix2) + ".json"
    obj["@id"] = id

    obj["seeAlso"]["@id"] = conv(obj["seeAlso"]["@id"])

    obj['related']["@id"] = "https://www.kanzaki.com/works/2016/pub/image-annotator?u="+obj["@id"]

    canvases = obj["sequences"][0]["canvases"]
    for j in range(len(canvases)):
        canvas = canvases[j]

        resource = canvas["images"][0]["resource"]
        canvas["images"][0]["resource"] = conv2(resource)

        canvas["thumbnail"] = conv3(canvas["thumbnail"], canvas["images"][0]["resource"]["@id"])

        if j == 0:
            obj["thumbnail"] = canvas["thumbnail"]

    opath = file.replace("/iiif/", "/iiif2/")

    dirname = os.path.dirname(opath)

    os.makedirs(dirname, exist_ok=True)

    fw = open(opath, 'w')
    json.dump(obj, fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))

    
