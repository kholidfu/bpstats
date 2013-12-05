import urllib2
import re
from bs4 import BeautifulSoup

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


if __name__ == "__main__":
    b = bpsData()
    print b.get_provinces()
