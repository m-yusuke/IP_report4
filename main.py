import cv2
import argparse
import numpy as np
from PIL import Image


def get_args():
    # 使用可能なオプションの指定
    parser = argparse.ArgumentParser(description='漫画風加工プログラム')
    parser.add_argument('--target', '-t', default='./sample1_low.jpg', help='使用する画像ファイルの指定')
    parser.add_argument('--save', '-s', action='store_true', default=False, help='出力結果を保存するするかどうか')
    parser.add_argument('--outname', '-o', default='./result.png', help='出力結果を保存する際のファイル名の指定')
    parser.add_argument('--debug', default=False, action='store_true', help='結果を出力するかどうか')
    parser.add_argument('--low', default=70, type=int, help='エッジ下側しきい値(defauls:70)')
    parser.add_argument('--high', default=75, type=int, help='エッジ上側しきい値(default:75)')
    parser.add_argument('--bright', default=20, type=int, help='出力の明るさ(defaule:20)')

    args = parser.parse_args()
    return args

args = get_args()

def output_to_window(img):
    # opencvのBGR形式からPillowでの出力用にRGBへ変換
    img_result = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # numpy.ndarray形式からPillowのImageオブジェクトへ変換
    pil_img = Image.fromarray(img_result.astype(np.uint8))
    # プレビューへ出力(macの場合)
    pil_img.show()

def ternarization(img):
    # 大津の二値化によりしきい値を計算
    ret, _ = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
    # トーン貼り付け用に三値化するためにしきい値を分割
    th1 = ret - args.bright
    th2 = ret - (args.bright - 10)
    # 白, 黒, グレーへ三値化
    img[img > th1] = 255
    img[img < th2] = 0
    img[np.where((th2 <= img) & (img <= th1))] = 128
    return img

def edge_detect(img):
    # ノイズ低減のために平滑化
    blur = cv2.GaussianBlur(img,(5,5),0)
    # Canny法によりエッジ検出
    edges = cv2.Canny(blur, args.low, args.high)
    return edges

def paste_tone(img):
    # 使用するトーン画像
    tone = cv2.imread('./tone.png', 0)
    # 画像に貼り付けるためにトーン画像のサイズを加工画像と揃える
    tone = cv2.resize(tone, (img.shape[1], img.shape[0]))
    # 三値化によりグレーになっている箇所をトーン画像で置換
    img[img == 128] = tone[img == 128]
    return img

def main():
    # 画像読み込み
    img = cv2.imread(args.target, 0)
    # エッジ検出
    edges = edge_detect(img)
    # 三値化
    img = ternarization(img)
    # トーン貼り付け
    img = paste_tone(img)
    # トーン貼り付けした画像とエッジを合成
    result = img - edges
    if args.debug:
        # debugオプションが有効の場合は何も出力しない
        pass
    elif args.save:
        # saveオプションが有効の場合は画像として出力
        cv2.imwrite(args.outname, result)
    else:
        # プレビューへ出力(macの場合)
        output_to_window(result)
    
if __name__ == '__main__':
    main()
