import cv2
import argparse
import numpy as np
from PIL import Image


def get_args():
    parser = argparse.ArgumentParser(description='漫画風加工プログラム')
    parser.add_argument('--target', '-t', default='./sample1_low.jpg', help='使用する画像ファイルの指定')
    parser.add_argument('--save', '-s', action='store_true', default=False, help='出力結果を保存するするかどうか')
    parser.add_argument('--outname', '-o', default='./result.png', help='出力結果を保存する際のファイル名の指定')
    parser.add_argument('--debug', default=False, action='store_true', help='結果を出力するかどうか')
    parser.add_argument('--low', default=70, type=int, help='下側しきい値')
    parser.add_argument('--high', default=75, type=int, help='上側しきい値')

    args = parser.parse_args()
    return args

args = get_args()

def output_to_window(img):
    img_result = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_result.astype(np.uint8))
    pil_img.show()

def main():
    th1 = 90
    th2 = 80
    img = cv2.imread(args.target, 0)
    tone = cv2.imread('./tone.png', 0)
    tone = cv2.resize(tone, (img.shape[1], img.shape[0]))
    edges = 255 - cv2.Canny(img, args.low, args.high)
    blur = cv2.GaussianBlur(img,(5,5),0)
    edges = cv2.Canny(blur, args.low, args.high)
    #ret, th = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
    img[img > th1] = 255
    img[img < th2] = 0
    img[np.where((th2 <= img) & (img <= th1))] = 128
    img[img == 128] = tone[img == 128]
    result = img - edges
    if args.debug:
        pass
    elif args.save:
        cv2.imwrite(args.outname, result)
    else:
        output_to_window(result)
    
if __name__ == '__main__':
    main()
