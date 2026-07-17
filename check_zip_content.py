import zipfile

with zipfile.ZipFile("data/ndwi/FL20230606UKR_SHP.zip") as z:
    for name in z.namelist():
        print(name)