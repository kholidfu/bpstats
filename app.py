from unidecode import unidecode
import urllib2
import re
from bs4 import BeautifulSoup
import pandas as pd

class bpsData(object):

    def __init__(self):
        self.url = "http://www.bps.go.id/tab_sub/view.php?kat=1&tabel=1&daftar=1&id_subyek=40&notab=1"

    def get_html(self):
        html = urllib2.urlopen(self.url).read()
        return html

    def get_provinces(self):
        soup = BeautifulSoup(self.get_html())
        provinces = [i.text for i in soup.find_all('td', style=re.compile(r"height:15.0pt"))[3:37]]
        return provinces

    def create_csv(self):
        soup = BeautifulSoup(self.get_html())
        rows = soup.find_all('tr', style=re.compile("userset;height:15.0pt"))
        data = ''
        for row in rows:
            #r = row.find_all('td')
            data += ';'.join([r.text for r in row.find_all('td') if r.text != None])
            data += '\n'
        data_file = data.split('\n')
        with open("data.csv", "wb") as f:
            for d in data_file[6:40]:
                f.write(d + '\n')

    def analyze_data(self):
        """analyze data with pandas
        """
        df = pd.read_csv("data.csv", sep=";", index_col=0, header=None)
        data_lk = df[[1,2,3,4]]
        data_prmp = df[[5,6,7,8]]
        data_total = df[[9,10,11,12]]
        print data_total


if __name__ == "__main__":
    b = bpsData()
    b.create_csv()
    b.analyze_data()
