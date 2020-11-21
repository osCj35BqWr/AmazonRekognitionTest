#from boto3.session import Session
import boto3
from PIL import Image,ImageDraw

inputPath = r".\img\test.jpeg"
outputPath = r".\img\test_output.jpeg"

# Rekognitionのクライアントを作成
# IAMユーザーに割り当てたポリシー
# AmazonRekognitionFullAccess
# profile名は環境編巣にAWS_DEFAULT_PROFILE, AWS_PROFILEとして定義した。
#session = Session(profile_name='XXX_profileName_XXX', region_name='ap-northeast-1')
#client = session.client('rekognition')
client = boto3.client('rekognition', region_name='ap-northeast-1')

# 画像ファイルを引数としてdetect_facesを実行
with open(inputPath,'rb') as image:
    #response = client.detect_faces(Image={'Bytes':image.read()},Attributes=['ALL'])
    # MaxLabels=20はなくても良い
    response = client.detect_labels(Image={'Bytes': image.read()}, MaxLabels=20)
# 物体が認識されない場合は処理終了
if len(response['Labels'])==0:
    print('物体は認識されませんでした。')
else:
    # 入力された画像ファイルを元に、矩形セット用の画像ファイルを作成
    img = Image.open(inputPath)
    imgWidth,imgHeight = img.size
    draw = ImageDraw.Draw(img)

    # 認識された物体の数分、矩形セット処理を行う
    for labels in response['Labels']:
        print("Label: " + labels["Name"])
        print("Confidence: " + str(labels["Confidence"]))
        for instance in labels["Instances"]:
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