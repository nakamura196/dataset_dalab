import json
import argparse
import yaml
from classes.downloader import Downloader
import os
import glob
import shutil
import requests


def download(url, path):
    response = requests.get(url)

    file = open(path, "wb")
    file.write(response.content)
    file.close()

top = "../docs"
prefix = "https://diyhistory.org/public/dalab"

files = glob.glob("../docs/api/media/*.json")

arr = ["original", "large", "medium", "square"]

for i in range(len(files)):
    if i % 10 == 0:
        print(i+1, len(files))

    file = files[i]
    with open(file) as f:
        obj = json.load(f)
        original_url = obj["o:original_url"]

        for e in arr:

            url = original_url.replace("/original/", "/"+e+"/")
            path = url.replace(prefix, top)

            if not os.path.exists(path):
                dirname = os.path.dirname(path)
                os.makedirs(dirname, exist_ok=True)
                download(url, path)




