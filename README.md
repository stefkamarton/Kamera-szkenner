# Kamera-szkenner
Képen található papír alapú dokumentum felismerése és szkennelése (vágás, transzformáció, javítás/filterezés).  
A script csak olyan képeket tud scannelni amik jól elkülöníthető kontúrokkat tartalmaz.

## Előkövetelmények

### Szoftveres
`Python == 3.6`  
`pip == 20.0.2`  
`Opencv == 4.2.0`  
`numpy == 1.19.4`  
`imutils == 0.5.3`  
`argparse == 1.1`  
`scipy == 1.6.0`
### Hardwares
- Processzor: `min. 700Mhz`
- RAM: `min. 256MB`
- Operációs rendszer: `Bármely operációs rendszer amik az alábbi szoftveres előkövetelményeket tudják teljesíteni`  
  `(Ajánlott: Ubuntu 20.04, Windows 10)`
  
### Bemeneti kép
- Kép formátuma: `jpeg, jpg, png`
- Kép tartalma:
    - A teljes objektumot tartalmaznia kell.
    - A kép nem lehet túl homályos.
    - A kép nem lehet túl pixeles.
    - A képen nem lehet árnyék, és a fényviszonyoknak egységesnek kell lennie.
    - A kép megfelelő tájolásban van fotózva.


## Program futtatása
### Alap
`scan.py -i <image_file_name> -o <output_image_file_name>`
### Kötelező paraméterek
`-i <image_file_name>` - A kép pontos helyét kell megadni a futtató mappából  
`-o <output_image_file_name>` - A kimeneti kép helyét és nevét kell megadni a futtató mappához képest
### Debug parameter
`-d` - A program minden lépése után megmutatja a kép állapotát
### Filter paraméterek
`-bl` - Blur Filter  
`-ga` - Guassian Blur Filter  
`-me` - Median Blur Filter  
`-bi` - Bilateral Filter  
`-sh` - Sharpen Filter  
`-em` - Emboss Filter  
`-bc <+/-number>` - Brightness Control [-255,255]  
`-in` - Invert Filter
`-bw` - Black and White Filter

## Tesztelt operációs rendszerek:  
`Ubuntu 20.04` - Terminálban és PyCharm programban tesztelve és 
`Windows 10` - PyCharm programban tesztelve.

##Tesztgép hardware:
- Processzor: `AMD Ryzen 5 3600 @ 3.6Ghz`
- RAM: `Kingston HyperX Predator DDR4-3200 16GB Kit2`

## Tesztek
![Teszt1]("test-images/test1.jpg")

## Források
- https://docs.python.org/3/howto/argparse.html
- https://github.com/andrewdcampbell/OpenCV-Document-Scanner
- http://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/
- https://www.blog.pythonlibrary.org/2020/02/09/how-to-check-if-a-file-is-a-valid-image-with-python/
- https://docs.python.org/3/library/os.path.html#os.path.isfile
- https://stackoverflow.com/questions/59363298/argparse-expected-one-argument
- https://docs.opencv.org/master/d4/d13/tutorial_py_filtering.html
- https://towardsdatascience.com/python-opencv-building-instagram-like-image-filters-5c482c1c5079
- https://stackoverflow.com/questions/56812505/image-restoration-to-enhance-details-with-opencv
- https://docs.opencv.org/master/d4/d86/group__imgproc__filter.html
