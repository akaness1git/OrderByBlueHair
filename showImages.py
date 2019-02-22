# coding: utf-8
import cv2 
import glob

ESC_key = 27 # ESC
next_key_list = [100,115] # D,S
prev_key_list = [119,97] # A,W

gui = "Order By BlueHair"
test_data = "./testdata/*"

def showImage(files):
    i = 0
    max = len(files) - 1
    img = cv2.imread(files[i])
    cv2.namedWindow(gui, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(gui, img)
    k = cv2.waitKey(0)

    # ESCキーが押されるまでループ
    while k != ESC_key:
        # SかDで次の画像を表示。ただし最後の場合は最後のまま
        if k in next_key_list:
            i = i + 1
            if i > max:
                i = max
        # AかWで前の画像を表示。ただし最初の場合は最初のまま
        elif k in prev_key_list:
            i = i - 1
            if i < 0:
                i = 0
            
        img = cv2.imread(files[i])
        cv2.imshow(gui, img)
        k = cv2.waitKey(0)

    cv2.destroyAllWindows()

def main():
    files = glob.glob(test_data)
    showImage(files)

if __name__ == "__main__":
    main()