import numpy as np
import imutils
import cv2
import argparse
import os.path

from skimage.filters import threshold_local


# Objektum sarkainak megkeresése
def find_edges(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Szürkévé tétel
    ed = cv2.Canny(gray, 75, 200)  # Szélek meghatározása
    return ed


def show_result(title, *imgs):
    for index, i in enumerate(imgs):
        cv2.imshow(title + " No.:" + str(index + 1), i)
    cv2.waitKey(0)
    return


def order_points(pts):
    #Pontok inicializálása és sorba rendezése
    rect = np.zeros((4, 2), dtype="float32")

    # Bal-felső lesz a legkisebb értékű
    # Jobb alsó lesz a legnagyobb értékű
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # Jobb felső lesz a legkisebb különbségű
    # Bal alsó lesz a legnagyobb különbségű
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # Visszatérés a rendezett koordinátákkal
    return rect


def four_point_transform(img, pts):
    # Koordináta rendezés, változókba bontás (top-left, top-right, bottom-right, bottom-left)
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # Kép szélességének meghatározása, legnagyobbat válasszuk
    width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_width = max(int(width_a), int(width_b))

    # Kiszámoljuk magasságát, legnagyobbat válasszuk
    height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(height_a), int(height_b))

    # Kép átalakítása a kiszámolt értékre
    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32")

    m = cv2.getPerspectiveTransform(rect, dst)
    warp = cv2.warpPerspective(img, m, (max_width, max_height))

    return warp


def blur_filter(img):
    img = cv2.blur(img, (5, 5))
    if args["debug"]:
        show_result("Blurred", imutils.resize(img, height=500))
    return img


def gaussian_blur_filter(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    if args["debug"]:
        show_result("Gaussian blur", imutils.resize(img, height=500))
    return img


def median_blur_filter(img):
    img = cv2.medianBlur(img, 5)
    if args["debug"]:
        show_result("Media blur", imutils.resize(img, height=500))
    return img


def bilateral_filter(img):
    img = cv2.bilateralFilter(img, 9, 75, 75)
    if args["debug"]:
        show_result("Bilateral blur", imutils.resize(img, height=500))
    return img


def sharpen(img):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img = cv2.filter2D(img, -1, kernel)
    if args["debug"]:
        show_result("Sharpen ", imutils.resize(img, height=500))
    return img


def sepia(img):
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    img = cv2.filter2D(img, -1, kernel)
    if args["debug"]:
        show_result("Sepia ", imutils.resize(img, height=500))
    return img


def emboss(img):
    kernel = np.array([[0, -1, -1],
                       [1, 0, -1],
                       [1, 1, 0]])
    img = cv2.filter2D(img, -1, kernel)
    if args["debug"]:
        show_result("Emboss ", imutils.resize(img, height=500))
    return img


def brightnesscontrol(img, level):
    img = cv2.convertScaleAbs(img, beta=level)
    if args["debug"]:
        show_result("Brightness control ", imutils.resize(img, height=500))
    return img


def invert_filter(img):
    img = (255 - img)
    if args["debug"]:
        show_result("Invert ", imutils.resize(img, height=500))
    return img


def black_and_white_filter(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    t = threshold_local(img, 11, offset=10, method="gaussian")
    img = (img > t).astype("uint8") * 255
    if args["debug"]:
        show_result("Black and white ", imutils.resize(img, height=500))
    return img


# Argumentumok bekérése
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
ap.add_argument("-bc", "--brightnesscontrol", required=False, help="Brightness Control")
ap.add_argument("-in", "--invert_filter", action='store_true', required=False, help="Invert filter")
ap.add_argument("-bw", "--black_and_white_filter", action='store_true', required=False, help="B&W filter")


# Tömbe helyezése
args = vars(ap.parse_args())

# Image fájl beolvasása

if os.path.isfile(args['image']):

    # Image beolvasása
    image = cv2.imread(args['image'])

    # Kép átméretezésének kiszámolása
    ratio = image.shape[0] / 500.0
    #
    # Original kép mentése
    orig = image.copy()
    #
    # Kép méretezés
    image = imutils.resize(image, height=500)
    #
    # Objektum sarkainak
    edged = find_edges(image)

    if args["debug"]:
        show_result("Original and Edge", image, edged)

    # Kontúrok keresése
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    screenCnt = 0

    for c in cnts:
        # Kontúrok megközelítése
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # Ha 4 pontja van a kontúrnak akkor valószínűleg megtaláltuk
        if len(approx) == 4:
            screenCnt = approx
            break

    # Kontúrok mutatása
    try:
        cv2.drawContours(image, [screenCnt], -1, (255, 0, 0), 2)
    except NameError:
        print("A bemeneti képen nem lehet kontúrt elkülöníteni")
        exit()

    if args["debug"]:
        show_result("Outline", image)

    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

    if args["debug"]:
        show_result("Wrapped - Original", imutils.resize(warped, height=500))

    # Filterezés
    for key in args:
        # print(key+"(warped)")
        if key!="image" and key!="output" and key!="debug" and key!="brightnesscontrol":
            if args[key]:
                warped = eval(key+"(warped)")
        if key == "brightnesscontrol" and args[key] is not None:
            # print(args[key])
            warped = brightnesscontrol(warped, int(args[key]))

    if args["debug"]:
        show_result("Wrapped", imutils.resize(warped, height=500))
    # Kép mentés
    if args["output"] is not None:
        cv2.imwrite(args["output"], warped)
