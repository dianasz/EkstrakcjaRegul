import urllib2
import time

minX = 5000
minY = 1450
maxX = 5180
maxY = 1850

adres = "http://api.openstreetmap.org/api/0.6/map?bbox="
krok = 2
dzielnik = 100
n = 0
i = 0

x1 = minX
for x in xrange(minX, maxX, krok):
    x1 = float(x) / dzielnik
    x2 = float(x + krok) / dzielnik
    for y in xrange(minY, maxY, krok):
        y1 = float(y) / dzielnik
        y2 = float(y + krok) / dzielnik
        url = adres + str(y1) + "," + str(x1) + "," + str(y2) + "," + str(x2)
        nieUdalo = True
        while nieUdalo:
            try:
                osm = urllib2.urlopen(url)
                nazwaPliku = "plikiOSM/" + str(n) + ".osm"
                plik = open(nazwaPliku,"w")
                plik.write(osm.read())
                plik.close()
                nieUdalo = False
            except:
                nieUdalo = True
                print "n= " + str(n) + ". Niepowodzenie :("
        i+=1
        if i == 50:
            time.sleep(60)
            i=0
        n+=1
    print "Wykonano " + str((x2 * dzielnik - minX)/(maxX - minX)*100) + "%. n= " + str(n)
    time.sleep(120)

print "To ju¿ jest koniec"
