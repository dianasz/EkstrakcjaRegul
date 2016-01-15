#lxml biblioteka, ktora pozwala na przetwarzanie danych z plikow XML i HTML
from lxml import etree
from os import walk	# funkcja walk() - pobranie listy plikow za pomoca biblioteki os

nazwaSQL = 'wstawDane.sql' #utworzenie pliku
plik = open(nazwaSQL, 'w')
#utworzenie dwóch zapytań, które sa odpowiedzialne za utworzenie tabeli Nodes
plik.writelines('Create table Nodes(id bigserial primary key, nodeID bigint, uzytkownik varchar(50), dataMod timestamp);\n')
plik.writelines("Select AddGeometryColumn('public', 'nodes', 'geom', 2180, 'POINT', 2);\n")
plik.close();



powiaty = []
#pobranie listę plików w folderze osm/Powiaty, gdzie znajdowaly sie pliki OSM dla powiatow
for (dirpath, dirnames, filenames) in walk(u'osm/Powiaty'):
    powiaty.extend(filenames)

#otwieranie plików i zapis zapytan do pliku wstawDane.sql	
for powiat in powiaty:
    print 'plik: ' + powiat
    nodes = []
    adresPliku = u'osm/Powiaty/' + powiat
    with open(adresPliku) as plik:
        tree = etree.parse(plik)
        root = tree.getroot()
		#wyszukiwanie znacznikow 'node' i pobranie atrybutów za pomocą metody .get, dodanie do listy 'nodes'
        for element in root:
            if element.tag == 'node':
                nodeID = element.get("id")
                geom = [float(element.get("lat")), float(element.get("lon"))]
                user = element.get("user")
                t = element.get("timestamp")
                time = t[0:10] + ' ' + t[11:19]
                nodes.append([nodeID, user, time, geom])
        root.clear()	#czyszczenie listy elementow po przegladnieciu wszystkich elementow
    
	#po przeglądnieciu calego powiatu, otworzenie pliku i dopisane do niego wygenerowanego polecenia INSERT
    plik = open(nazwaSQL, 'a')
    for node in nodes:
        if node[1][-1] == "'":
            uzytkownik = node[1][:-1]
        else:
            uzytkownik = node[1]
        insert = 'Insert into Nodes(nodeID, uzytkownik, dataMod, geom) values (' + str(node[0]) + ", '" + uzytkownik.encode('utf-8') + "', '" + str(node[2]) + "', ST_Transform(ST_GeomFromText('POINT(" + str(node[3][1]) + ' ' + str(node[3][0]) + ")', 4326),2180));\n"
        plik.writelines(insert)
    plik.close()
    print 'Zapytania dopisano'
    
    
print 'Koniec :P'

