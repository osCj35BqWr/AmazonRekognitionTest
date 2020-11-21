import boto3
import cv2
import pafy # YouTube video capture

inputImgPath = r".\img\input.jpeg"
outputImgPath = r".\img\output.jpeg"

#渋谷スクランブル交差点
#videoURL = "https://www.youtube.com/watch?v=lkIJYc4UH60"
videoURL = "https://www.youtube.com/watch?v=UuTy56M29qs"
video_pafy = pafy.new(videoURL)
video_from_url = video_pafy.getbest().url
cap = cv2.VideoCapture(video_from_url)
ret, frame = cap.read()
cv2.imwrite(inputImgPath, frame)
cap.release()

# Rekognitionのラベル検出を呼び出す
# 【AWS IAM関連情報】
#  IAMユーザーに割り当てたポリシー
#   AmazonRekognitionFullAccess
#  profile名
#   環境編巣にAWS_DEFAULT_PROFILE, AWS_PROFILEとして定義した。
client = boto3.client('rekognition', region_name='ap-northeast-1')
with open(inputImgPath, 'rb') as image:
    response = client.detect_labels(Image={'Bytes': image.read()})

#人数をカウントする
cnt = 0

# 物体が認識されない場合は処理終了
if len(response['Labels'])==0:
    print('物体は認識されませんでした。')
else:
    # 入力された画像ファイルを元に、矩形セット用の画像ファイルを作成
    img = cv2.imread(inputImgPath)
    imgHeight,imgWidth = img.shape[:2]

    # 認識された物体のうち人間に該当するラベルについて、矩形セット処理を行う
    for label in response['Labels']:
        # 人間以外は除外する
        if label['Name'] not in ['People', 'Person', 'Human']:
            continue
        for instance in label["Instances"]:

            cnt += 1

            # BoundingBoxから物体の位置・サイズ情報を取得
            box = instance['BoundingBox']
            x = round(imgWidth * box['Left'])
            y = round(imgHeight * box['Top'])
            w = round(imgWidth * box['Width'])
            h = round(imgHeight * box['Height'])
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 3)

    # 画像ファイルを保存
    cv2.imwrite(outputImgPath, img)

    # 人数を表示する
    print('検出された人数: {} 人'.format(cnt))

    # 画像を表示
    cv2.imshow("output", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()