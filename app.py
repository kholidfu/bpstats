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
        df = pd.read_csv("data.csv", header=None)
        df.columns = ['Provinsi', '2009|L', '2010|L', '2011|L', '2012|L', '2009|P', '2010|P', '2011|P', '2012|P', '2009|T', '2010|T', '2011|T', '2012|T']
        df = df.set_index(['Provinsi'])
        return df

    def show_graph(self):
        """show the graph with matplotlib
        """
        df = self.analyze_data()
        df2 = pd.DataFrame(df, columns=['2012|L', '2012|P'])
        df2 = df2.sort(['2012|L', '2012|P'], ascending=False)
        ax = df2.plot(kind='barh', 
                 stacked=True,
                 title="Persentase Penduduk menurut Provinsi dan Jenis Kelamin Tahun 2012",
                 legend=False,
                 fontsize='10')
        # custom legend
        patches, labels = ax.get_legend_handles_labels()
        ax.legend(patches, ['Laki-laki', 'Perempuan'], loc='best')

        plt.show()

    def show_graph2(self):
        """lets try back-to-back histogram
        """
        df = self.analyze_data() # raw data
        ind = np.arange(len(df.index)) # x locations for the groups
        width = 0.35 # width of the bars

        df2 = pd.DataFrame(df, columns=['2012|L', '2012|P']) # dataframe
        # begin plotting
        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, df[[1]].values, width, color='r')
        rects2 = ax.bar(ind+width, df[[5]].values, width, color='y')
        ax.set_xticklabels(df.index.tolist())
        plt.show()



if __name__ == "__main__":
    b = bpsData()
    b.create_csv()
    #b.analyze_data()
    b.show_graph()
