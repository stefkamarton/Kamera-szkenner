import numpy as np
import imutils
import cv2
import argparse
import os.path
import pytesseract
import re

from skimage.filters import threshold_local


# Objektum sarkainak megkeresése
def find_edges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Szürkévé tétel
    gray = cv2.GaussianBlur(gray, (5, 5), -6)  # Elmosodás
    edged = cv2.Canny(gray, 75, 200)  # Szélek meghatározása
    return edged


def show_result(title, *imgs):
    for index, i in enumerate(imgs):
        cv2.imshow(title + " No.:" + str(index + 1), i)
    cv2.waitKey(0)
    return


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


def four_point_transform(image, pts):
    # Koordináta rendezés, változókba bontás (top-left, top-right, bottom-right, bottom-left)
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # Kép szélességének meghatározása, legnagyobbat válasszuk
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # Kiszámoljuk magasságát, legnagyobbat válasszuk
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # Kép átalakítása a kiszámolt értékre
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


def blur_filter(image):
    image = cv2.blur(image, (5, 5))
    if args["debug"]:
        show_result("Blurred", imutils.resize(image, height=650))
    return image


def gaussian_blur_filter(image):
    image = cv2.GaussianBlur(warped, (5, 5), 0)
    if args["debug"]:
        show_result("Gaussian blur", imutils.resize(image, height=650))
    return image


def median_blur_filter(image):
    image = cv2.medianBlur(image, 5)
    if args["debug"]:
        show_result("Media blur", imutils.resize(image, height=650))
    return image


def bilateral_filter(image):
    image = cv2.bilateralFilter(image, 9, 75, 75)
    if args["debug"]:
        show_result("Media blur", imutils.resize(image, height=650))
    return image


def sharpen(image):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    image = cv2.filter2D(image, -1, kernel)
    if args["debug"]:
        show_result("Sharpen ", imutils.resize(image, height=650))
    return image


def sepia(image):
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    image = cv2.filter2D(image, -1, kernel)
    if args["debug"]:
        show_result("Sepia ", imutils.resize(image, height=650))
    return image


def emboss(image):
    kernel = np.array([[0, -1, -1],
                       [1, 0, -1],
                       [1, 1, 0]])
    image = cv2.filter2D(image, -1, kernel)
    if args["debug"]:
        show_result("Emboss ", imutils.resize(image, height=650))
    return image


def brightnessControl(image, level):
    image = cv2.convertScaleAbs(image, beta=level)
    if args["debug"]:
        show_result("Brightness control ", imutils.resize(image, height=650))
    return image


def invert_filter(image):
    image = (255 - image)
    if args["debug"]:
        show_result("Invert ", imutils.resize(image, height=650))
    return image


def black_and_white_filter(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    T = threshold_local(image, 11, offset=10, method="gaussian")
    image = (image > T).astype("uint8") * 255
    if args["debug"]:
        show_result("Black and white ", imutils.resize(image, height=650))
    return image


### Argumentumok bekérése
ap = argparse.ArgumentParser()

# Kép elérési út bekérése
ap.add_argument("-i", "--image", required=True, help="[Kötelező] Kép elérését add meg!")
ap.add_argument("-o", "--output", required=True, help="[Kötelező] A kép kimeneti neve!")
ap.add_argument("-d", "--debug", action='store_true', required=False, help="Debug mód - Minden lépést mutat!")
ap.add_argument("-bl", "--blur_filter", action='store_true', required=False, help="Blur filter")
ap.add_argument("-ga", "--gaussian_blur_filter", action='store_true', required=False, help="Gaussian blur filter")
ap.add_argument("-me", "--median_blur_filter", action='store_true', required=False, help="Median blur filter")
ap.add_argument("-bi", "--bilateral_filter", action='store_true', required=False, help="Bilateral filter")
ap.add_argument("-sh", "--sharpen", action='store_true', required=False, help="Sharpen filter")
ap.add_argument("-em", "--emboss", action='store_true', required=False, help="Emboss filter")
ap.add_argument("-bc", "--brightnessControl", required=False, help="Brightness Control")
ap.add_argument("-in", "--invert_filter", action='store_true', required=False, help="Invert filter")
ap.add_argument("-bw", "--black_and_white_filter", action='store_true', required=False, help="Black and White filter filter")


# Tömbe helyezése
args = vars(ap.parse_args())
print(args['image'])

# Image fájl beolvasása

if os.path.isfile(args['image']):

    # Image beolvasása
    image = cv2.imread(args['image'])
    #
    # Kép átméretezésének kiszámolása
    ratio = image.shape[0] / 500.0
    #
    # Original kép mentése
    orig = image.copy()
    #
    # Kép méretezés
    image = imutils.resize(image, height=500)
    #
    ###Kép feljavítások

    ###
    # Objektum sarkainak
    edged = find_edges(image)

    if args["debug"]:
        show_result("Original and Edge", image, edged)

    # Kontúrok keresése
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # Ha 4 pontja van a kontúrnak akkor valószínűleg megtaláltuk
        if len(approx) == 4:
            screenCnt = approx
            break

    # Kontúrok mutatása
    cv2.drawContours(image, [screenCnt], -1, (255, 0, 0), 2)
    if args["debug"]:
        show_result("Outline", image)

    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

    if args["debug"]:
        show_result("Wrapped - Original", imutils.resize(warped, height=650))

#Filterezés
    for key in args:
        if args[key] == True:
            warped = eval(key+"(warped)")
        if key == "brightnessControl" and args[key]!=None:
            print(args[key])
            warped = brightnessControl(warped, int(args[key]))

    if args["debug"]:
        show_result("Wrapped", imutils.resize(warped, height=650))

#Kép mentés
    if args["output"] != None:
        cv2.imwrite(args["output"], warped)
