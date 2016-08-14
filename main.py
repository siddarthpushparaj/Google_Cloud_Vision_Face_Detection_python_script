#! /usr/bin/python
# -*- coding: utf-8 -*-
'''指定ディレクトリ内の画像全部Google APIに投げて顔検出するやつ'''

import cv2
import os
import os.path
import shutil
import sys
from face_detector import facedetector_gcv
import json

# --------------------------------------------
# param
# Google APIキーはface_detector.pyで設定してね
# 入力ディレクトリへのPath (./name/の形式だと嬉しい)
input_dir_path = './dataset/'
# 出力ディレクトリの名前 (作るので名前だけで良い)
output_dir_name = 'output_dataset'
# 検出する顔の数の最大数 (多いほどレスポンスが返ってくるのが遅い)
max_results = 4
# --------------------------------------------



def main():
    # ディレクトリpathからファイル名取得
    file_list = os.listdir(input_dir_path)
    file_list.sort()
    # 顔画像ありの矩形情報
    in_face = []
    # ディレクトリ内の全てのファイルに対して実行
    for i, img_path in enumerate(file_list):

        # ファイル読み込み
        img_path = input_dir_path + img_path
        img = cv2.imread(img_path)

        if(img is None):
            # 画像ファイルじゃない場合の処理
            # よしなに
            print 'not_img'
        else:
            img, s, response = facedetector_gcv(img, img_path, max_results)

            if s != '':
                # 顔画像ありと判断された場合
                img_name = os.path.basename(img_path)
                name, ext = os.path.splitext(img_name)
                img_path = './' + output_dir_name + '/True/' + img_name
                cv2.imwrite(img_path, img)
                in_face.append(s)
                with open('./' + output_dir_name + "/True/json/" + name + '.json', 'w') as f:
                    json.dump(response, f)
            else:
                # 顔画像なしと判断された場合
                img_name = os.path.basename(img_path)
                name, ext = os.path.splitext(img_name)
                img_path = './' + output_dir_name + '/False/' + img_name
                cv2.imwrite(img_path, img)
                with open('./' + output_dir_name + "/False/json/" + name + '.json', 'w') as f:
                    json.dump(response, f)

    # 矩形情報出力
    f = open('./' + output_dir_name + '/True/rect.txt', 'w')
    for x in in_face:
        f.write(x+"\n")
    f.close()


def make_dir(input_dir_path):
    # ディレクトリを削除してから作成
    try:
        output_dir_path = './' + output_dir_name + '/'
        if os.path.isdir(output_dir_path):
            shutil.rmtree(output_dir_path)
        os.mkdir(output_dir_path)
        os.mkdir(output_dir_path+'True/')
        os.mkdir(output_dir_path+'True/json/')
        os.mkdir(output_dir_path+'False/')
        os.mkdir(output_dir_path+'False/json/')
    except:
        print('Falt : directory make \n')
        sys.exit()

if __name__ == '__main__':
    # 例外処理
    if input_dir_path == output_dir_name:
        print '[Error]:input_dir equal output_dir'
        sys.exit(1)

    # 出力用ディレクトリを作成
    make_dir(output_dir_name)

    # ディレクトリ内を処理
    main()
