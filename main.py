import cv2
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='漫画風加工プログラム')
    parser.add_argument('--target', '-t', default='./sample1_low.jpg', help='使用する画像ファイルの指定')
    parser.add_argument('--save', '-s', action='store_true', default=False, help='出力結果を保存するするかどうか')
    parser.add_argument('--outname', '-o', default='./ex7_result.png', help='出力結果を保存する際のファイル名の指定')
    parser.add_argument('--debug', default=False, action='store_true', help='結果を出力するかどうか')
    parser.add_argument('--low', default=70, type=int, help='下側しきい値')
    parser.add_argument('--high', default=75, type=int, help='上側しきい値')

    args = parser.parse_args()
    return args

args = get_args()

def output_to_window(img):
    img = cv2.Canny(img,args.low, args.high)
    cv2.namedWindow("pic", cv2.WINDOW_NORMAL)

    cv2.imshow("pic",edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    img = cv2.imread(args.target, 0)
    edges = cv2.Canny(img,args.low, args.high)
    output_to_window(edges)
