from qgis.core import *
powiaty = QgsVectorLayer('D:\projekt\shp\powiaty.shp', 'Powiaty', 'ogr')

crsSrc = QgsCoordinateReferenceSystem(2180)
crsDest = QgsCoordinateReferenceSystem(4326)
transform = QgsCoordinateTransform(crsSrc, crsDest)
inverse = QgsCoordinateTransform(crsDest, crsSrc)

folder = 'D:\projekt\osm\PlikiOsm/'
iter = powiaty.getFeatures()

for powiat in iter:
    atrybutyPowiatu = powiat.attributes()
    if atrybutyPowiatu[2] == 'nie':
        
        geom = powiat.geometry() #obieeanie geometrii do zmiennej geo
        bbox = transform.transform(geom.boundingBox())
        bigGeom = geom.buffer(500.0, 20) #strefa buforowa po to, że jak jest bounding box na granicy powiatu i może się nie załapać
        print atrybutyPowiatu[1]
        
        bboxText = ' <bounds minlat="' + str(bbox.yMinimum()) + '" minlon="' + str(bbox.xMinimum())  + '" maxlat="' + str(bbox.yMaximum()) + '" maxlon="' + str(bbox.xMaximum()) + '"/>'
        naglowek = []
        naglowek.append('<?xml version="1.0" encoding="UTF-8"?>')
        naglowek.append('<osm version="0.6" generator="CGImap 0.4.0 (5201 thorn-01.openstreetmap.org)" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">')
        naglowek.append(bboxText)
        
        stopka = []
        stopka.append('</osm>')
        
        nodes = []
        ways = []
        relations = []

        nodesID = []
        waysID = []
        relationsID = []

        licznik = 0
        
        for i in xrange(0,18001):
            nazwaPliku = folder + str(i) + ".osm"
            plik = open(nazwaPliku,"r")
            text = plik.readlines( )
            plik.close()
            
            if licznik == 500:
                print atrybutyPowiatu[1] + ' ' + str(i)
                licznik = 0

            licznik += 1
            
            minlat = ''
            n = 17
            while text[2][n] != '"':
                minlat = minlat + text[2][n]
                n+= 1
            
            minlon = ''
            n = 37
            while text[2][n] != '"':
                minlon = minlon + text[2][n]
                n += 1
            
            maxlat = ''
            n = 57
            while text[2][n] != '"':
                maxlat = maxlat + text[2][n]
                n += 1
            
            maxlon = ''
            n = 77
            while text[2][n] != '"':
                maxlon = maxlon + text[2][n]
                n += 1
            
            bboxPliku = QgsRectangle(QgsPoint(float(minlon), float(minlat)), QgsPoint(float(maxlon), float(maxlat)))
            invbboxPliku= inverse.transform(bboxPliku)
            
            if bigGeom.contains(invbboxPliku.center()):
                print atrybutyPowiatu[1] + ' ' + str(i)
                for j in xrange(0,len(text)):
                    if text[j][0:6] == ' <node':
                        idNode = ''
                        k = 11
                        while text[j][k] != '"':
                            idNode = idNode + text[j][k]
                            k += 1
                        try:
                            nodesID.index(int(idNode))
                        except ValueError:
                            nodesID.append(int(idNode))
                            nodes.append(text[j])
                            
                            if text[j][-4:] != '/>\r\n':
                                m = j + 1
                                while text[m] != ' </node>\r\n':
                                    nodes.append(text[m])
                                    m += 1
                                nodes.append(' </node>\r\n')
            
                    if text[j][0:6] == ' <way ':
                        idWay = ''
                        k = 10
                        while text[j][k] != '"':
                            idWay = idWay + text[j][k]
                            k += 1

                        try:
                            waysID.index(int(idWay))
                        except ValueError:
                            waysID.append(int(idWay))
                            ways.append(text[j])
                            
                            if text[j][-4:] != '/>\r\n':
                                m = j + 1
                                while text[m] != ' </way>\r\n':
                                    ways.append(text[m])
                                    m += 1
                                ways.append(' </way>\r\n')
            
                    if text[j][0:6] == ' <rela':
                        idRelation = ''
                        k = 15
                        while text[j][k] != '"':
                            idRelation = idRelation + text[j][k]
                            k += 1

                        try:
                            relationsID.index(int(idRelation))
                        except ValueError:
                            relationsID.append(int(idRelation))
                            relations.append(text[j])

                            if text[j][-4:] != '/>\r\n':
                                m = j + 1
                                while text[m] != ' </relation>\r\n':
                                    relations.append(text[m])
                                    m += 1
                                relations.append(' </relation>\r\n')
                        
                        
        osm = []
        for i in xrange(0, len(naglowek)):
            osm.append(naglowek[i] + '\n')
            
        for i in xrange(0, len(nodes)):
            osm.append(nodes[i])
        
        for i in xrange(0, len(ways)):
            osm.append(ways[i])
        
        for i in xrange(0, len(relations)):
            osm.append(relations[i])
        
        for i in xrange(0, len(stopka)):
            osm.append(stopka[i])
            
        nazwaPliku = 'D:\projekt\osm\Powiaty/' + atrybutyPowiatu[1] + ".osm"
        plik = open(nazwaPliku,"w")
        for i in xrange(0, len(osm)):
            plik.writelines(osm[i])
        
        plik.close()

print 'koniec :P'
    

    

