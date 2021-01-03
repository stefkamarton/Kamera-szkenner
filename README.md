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

## Tesztgép hardware:
- Processzor: `AMD Ryzen 5 3600 @ 3.6Ghz`
- RAM: `Kingston HyperX Predator DDR4-3200 16GB Kit2`

## Tesztek - Objektum felismerés
A következő képek a program lépés folyamatait mutatja be az eredeti képtől kezdve a vágottig
#### Teszt No. 1
![Teszt_1](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res1.png?raw=true)
#### Teszt No. 2
![Teszt_2](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res2.png?raw=true)
#### Teszt No. 3
![Teszt_3](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res3.png?raw=true)
#### Teszt No. 4
![Teszt_4](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res4.png?raw=true)
#### Teszt No. 5
![Teszt_5](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res5.png?raw=true)
#### Teszt No. 6
![Teszt_6](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res6.png?raw=true)
#### Teszt No. 7
![Teszt_7](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res7.png?raw=true)
#### Teszt No. 8
![Teszt_8](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res8.png?raw=true)
#### Teszt No. 9
![Teszt_9](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res9.png?raw=true)
#### Teszt No. 10
![Teszt_10](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res10.png?raw=true)
#### Teszt No. 11
![Teszt_11](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res11.png?raw=true)
#### Teszt No. 12
![Teszt_12](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res12.png?raw=true)
#### Teszt No. 13
![Teszt_13](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res13.png?raw=true)
#### Teszt No. 14
![Teszt_14](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res14.png?raw=true)
#### Teszt No. 15
![Teszt_15](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res15.png?raw=true)
#### Teszt No. 16
![Teszt_16](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res16.png?raw=true)
#### Teszt No. 17
![Teszt_17](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res17.png?raw=true)
#### Teszt No. 18
![Teszt_18](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res18.png?raw=true)
#### Teszt No. 19
![Teszt_19](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res19.png?raw=true)
#### Teszt No. 20
![Teszt_20](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res20.png?raw=true)
#### Teszt No. 20
![Teszt_21](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res21.png?raw=true)
#### Teszt No. 22
![Teszt_22](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res22.png?raw=true)

## Felismert objektum filterezés tesztelése
#### Teszt - Blur Filter (Paraméter: `-bl`)
![Teszt_bl](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res-bl.png?raw=true)
#### Teszt - Guassian Blur Filter (Paraméter: `-ga`)
![Teszt_ga](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res-ga.png?raw=true)
#### Teszt - Median Blur Filter (Paraméter: `-me`)
![Teszt_me](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res-me.png?raw=true)
#### Teszt - Bilateral Filter (Paraméter: `-bi`)
![Teszt_bi](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res-bi.png?raw=true)
#### Teszt - Sharpen Filter (Paraméter: `-sh`)
![Teszt_sh](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res-sh.png?raw=true)
#### Teszt - Emboss Filter (Paraméter: `-em`)
![Teszt_em](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res-em.png?raw=true)
#### Teszt - Brightness Control +50 (Paraméter: `-bc 50`)
![Teszt_bc50](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res-bc50.png?raw=true)
#### Teszt - Brightness Control -50 (Paraméter: `-bc "-50"`)
![Teszt_bc-50](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res-bc-50.png?raw=true)
#### Teszt - Invert Filter (Paraméter: `-in`)
![Teszt_in](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res-in.png?raw=true)
#### Teszt - Black and White Filter (Paraméter: `-bw`)
![Teszt_bw](https://github.com/stefkamarton/Kamera-szkenner/blob/master/test-results/res-bw.png?raw=true)

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

## Szerző
Stefka Márton @ 2020-2021