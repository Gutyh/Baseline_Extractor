from bs4 import BeautifulSoup
import re
import subprocess


class BaselineExtractor():
    """
    Objet pour extraire les donnees qui ont ete surlignees en couleur dans un
    logiciel de traitement de texte type LibreOffice

    """

    def __init__(self):
        # A AMELIORER POUR FAIRE CA DEPUIS UN FICHIER ET AVEC D'AUTRES NUANCES DE COULEURS
        self.colors = {
        "yellow" : "#ffff00",
        "orange" : "#ff8000",
        "green": "#81d41a",
        "blue": "#729fcf",
        "purple" :"#a1467e",
        "red" : "#ff4000",
        "grey" : "#cccccc",
        "pink" : "#ffd7d7",
        }

    def read_list(self, list):
        for i in list:
            yield i

    def extract(self, odt_file):

        self.convert_to_htm(odt_file)

        html_file = "{}.htm".format(odt_file[:-4])

        with open(html_file, "r") as f:
            # for line in f:
            #     print(line)
            soup = BeautifulSoup(f, features="lxml")

        tag = soup.find_all("span")
        # list_colors = [i["style"][i["style"].rfind("#"):] for i in tag if "style" in i.attrs if i["style"]]
        # print(list_colors)


        dic_colors = {}

        list_colors = []
        for a in self.read_list(tag):
            # print(a.attrs)
            if "style" in a.attrs:
                attr = a["style"]
                colorcode = attr[attr.rfind("#"):]
                text = a.text.replace("\n", " ")
                if colorcode not in dic_colors:
                    dic_colors[colorcode] = []
                list_colors.append((colorcode, text))


        for a in self.read_list(tuple(list_colors)):
            dic_colors[a[0]].append(a[1])

        print(dic_colors)



    def convert_to_htm(self, odt_file):
        subprocess.Popen(["soffice", "--headless", "--convert-to", "htm","{}".format(odt_file)])
if __name__ == "__main__":
    ble = BaselineExtractor()
    ble.extract("baseline_annonces.odt")
