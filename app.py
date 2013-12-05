import numpy as np
import matplotlib.pyplot as plt
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
        provinces = [i.text for i in soup.find_all(
                'td', style=re.compile(r"height:15.0pt"))[3:37]]
        return provinces

    def create_csv(self):
        soup = BeautifulSoup(self.get_html())
        rows = soup.find_all('tr', style=re.compile("userset;height:15.0pt"))
        data = ''
        for row in rows:
            data += ';'.join(
                [r.text.replace(',', '.') for r in row.find_all('td')])
            data += '\n'
        data_file = data.split('\n')
        with open("data.csv", "wb") as f:
            for d in data_file[6:39]: # the 1st 6 data are gibberish
                f.write(d.replace(';', ',') + '\n')

    def analyze_data(self):
        """analyze data with pandas
        """
        df = pd.read_csv("data.csv", sep=",", index_col=0, header=None)
        df.columns = ['2009|L', '2010|L', '2011|L', '2012|L', '2009|P', '2010|P', '2011|P', '2012|P', '2009|T', '2010|T', '2011|T', '2012|T']
        # data_lk = df[[1,2,3,4]]
        # data_prmp = df[[5,6,7,8]]
        # data_total = df[[9,10,11,12]]
        return df

    def show_graph(self):
        """show the graph with matplotlib
        """
        df = self.analyze_data()
        df2 = pd.DataFrame(df, columns=['2012|L', '2012|P'])
        #df[[1]].plot(kind='bar')
        df2.plot(kind='bar', 
                 title="Persentase Penduduk menurut Provinsi dan Jenis Kelamin Tahun 2012", 
                 legend=False)
        plt.legend(fancybox=True, shadow=True)
        plt.show()


if __name__ == "__main__":
    b = bpsData()
    b.create_csv()
    #b.analyze_data()
    b.show_graph()
