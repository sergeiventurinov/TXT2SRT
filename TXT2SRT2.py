# -*- coding: UTF-8 -*-
import xml.etree.ElementTree as ET

inpfile = 'Sequence.xml' #Here your xml file
outfile = 'Sequence.srt' #here your srt file

def textretriever():

    nu = 0  # File effectid Counter
    subtitle = [] #lista de tres elementos: in, out y texto

    # Cambio de Caracteres Especiales

    xml_file_handle = open(inpfile, 'r')
    xml_as_string = xml_file_handle.read()
    xml_file_handle.close()

    xml_cleaned = xml_as_string.replace('&#13;', '*') #cambio de special characters

    root = ET.fromstring(xml_cleaned)

    print ('XML2SRT por SERGIO VENTURINI')

    #Get Text Content and Timebase

    for sequenceTimebase in root.findall(".//sequence/rate"):
        timebase = (sequenceTimebase.find('timebase').text)

    for cliplist in root.findall('.//clipitem'):

        inp= timecoder(int(cliplist.find('start').text), int(timebase))
        outp = timecoder(int(cliplist.find('end').text), int(timebase))

        for textlist in cliplist.findall('./filter/effect'):
            if (textlist.find('effectid').text) == 'GraphicAndType':
                txt = textlist.find('name').text

        subtitle.insert (nu, [inp,outp,txt])
        #print (subtitle[nu])
        nu=nu+1

    srtcreator(subtitle)

def timecoder(frames,timebase):
    h = int(frames / (timebase *3600))
    m = int(frames / (timebase * 60)) % 60
    s = int((frames % (timebase *60)) / timebase)
    f = int(frames % (timebase * 60) % timebase)
    mseg = 1000 * f / timebase
    return ("%02d:%02d:%02d,%03d" % (h, m, s, mseg))

def srtcreator(subtitle):

    f = open(outfile, "a")
    n = 1

    for x in subtitle:
        timeIn = x[0]
        timeOut = x[1]
        text = x[2]
        f.write(str(n) + '\n')
        f.write (timeIn + ' --> ' + timeOut+ '\n')

        #detectar line breaks
        lbrk = '*' #Caracter que marca el salto de linea

        brks = ([pos for pos, char in enumerate(text) if char == lbrk]) #lista con ubicacion de saltos en el str, posicion
        print ('quiebre en posicion ', brks)
        text = text.replace('*', ' ')  # cambio de special characters
        text = text.encode("utf-8")
        print ('texto: ', text)

        cantBrks = len(brks)
        #print ('cant de quiebres', cantBrks)
        bk = 0

        if cantBrks > 0:
            for i in range(cantBrks):
                #print ('quiebre nro', i)
                if i == 0 and i != (cantBrks-1): #primera de muchas lineas
                    f.write(text[0:(brks[i])] + '\n')                      #imprime porcion de texto hasta el caracter del salto de linea
                elif i == 0 and i == (cantBrks-1): # solo dos lineas
                    f.write(text[0:(brks[i]+1)] + '\n')
                    f.write(text[(brks[i]+1):len(text)+1] + '\n') #linea final
                elif 0 < i < (cantBrks - 1): # entrelinea
                    f.write(text[(brks[i-1]+1):(brks[i]+1)] + '\n')
                elif i == (cantBrks-1): #anteultima y ultima linea de muchas
                    f.write(text[(brks[i - 1]+1):(brks[i]+1)] + '\n')
                    f.write(text[(brks[i]+1):(len(text)+1)] + '\n') # +(i -1)
                bk += 1
        else:
            f.write(text + '\n')

        f.write('\n')
        n = n + 1
    f.close()

textretriever()

