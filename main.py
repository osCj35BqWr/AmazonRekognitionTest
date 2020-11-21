#from boto3.session import Session
import boto3
import cv2
from PIL import Image,ImageDraw
import pafy # YouTube video capture

# inputPath = r".\img\test.jpeg"
inputPath = r".\img\input.jpeg"
outputPath = r".\img\output.jpeg"

#渋谷スクランブル交差点
#videoURL = "https://www.youtube.com/watch?v=lkIJYc4UH60"
videoURL = "https://www.youtube.com/watch?v=UuTy56M29qs"
video_pafy = pafy.new(videoURL)
video_from_url = video_pafy.getbest().url
cap = cv2.VideoCapture(video_from_url)
ret, frame = cap.read()
cv2.imwrite(inputPath,frame)
cap.release()

# Rekognitionのラベル検出を呼び出す
# 【AWS IAM関連情報】
#  IAMユーザーに割り当てたポリシー
#   AmazonRekognitionFullAccess
#  profile名
#   環境編巣にAWS_DEFAULT_PROFILE, AWS_PROFILEとして定義した。
client = boto3.client('rekognition', region_name='ap-northeast-1')
with open(inputPath,'rb') as image:
    response = client.detect_labels(Image={'Bytes': image.read()})

#人数をカウントする
cnt = 0

# 物体が認識されない場合は処理終了
if len(response['Labels'])==0:
    print('物体は認識されませんでした。')
else:
    # 入力された画像ファイルを元に、矩形セット用の画像ファイルを作成
    img = Image.open(inputPath)
    imgWidth,imgHeight = img.size
    draw = ImageDraw.Draw(img)

    # 認識された物体のうち人間に該当するラベルについて、矩形セット処理を行う
    for label in response['Labels']:
        # 人間以外は除外する
        if label['Name'] not in ['People', 'Person', 'Human']:
            continue
        for instance in label["Instances"]:

            cnt += 1

            # BoundingBoxから物体の位置・サイズ情報を取得
            box = instance['BoundingBox']
            left = imgWidth * box['Left']
            top = imgHeight * box['Top']
            width = imgWidth * box['Width']
            height = imgHeight * box['Height']

            # 矩形の位置・サイズ情報をセット
            points = (
                (left,top),
                (left + width,top + height)
            )

            # 物体を矩形で囲む
            draw.rectangle(points,outline='lime')

    # 画像ファイルを保存
    img.save(outputPath)

    # 画像ファイルを表示
    img.show()

    # 人数を表示する
    print('検出された人数: {} 人'.format(cnt))