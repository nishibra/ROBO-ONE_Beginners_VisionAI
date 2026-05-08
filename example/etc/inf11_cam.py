from ultralytics import YOLO
import cv2
from picamera2 import Picamera2

# 1. モデルの読み込み (ラズパイなら ncnn モデル推奨)
model = YOLO("yolo11n.pt") 
#model = YOLO("yolo11n_ncnn_model") 
# 2. Picamera2 の初期設定
picam2 = Picamera2()
# XRGB8888よりRGB888の方が扱いやすいです
config = picam2.create_preview_configuration(main={"format": 'BGR888', "size": (320, 240)})
picam2.configure(config)
picam2.start()

print("開始します。Escキーで終了。")

try:
    while True:
        # フレーム取得
        frame = picam2.capture_array()

        # YOLO推論 (persist=Trueで追跡を継続)
        # imgsz=320にするとラズパイ5では高速になります
        results = model.track(frame, persist=True, conf=0.3, imgsz=320, verbose=False)
        
        # 表示用にBGRへ変換
        annotated_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            clss = results[0].boxes.cls.cpu().numpy().astype(int)
            names = results[0].names

            for box, id_value, cls in zip(boxes, ids, clss):
                x1, y1, x2, y2 = box
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                
                # 物体の中心に印をつける
                cv2.circle(annotated_frame, (cx, cy), 5, (255, 0, 255), -1)
                # バウンディングボックスとIDを描画
                cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(annotated_frame, f"ID:{id_value} {names[cls]}", (int(x1), int(y1)-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("YOLO11 Tracking", annotated_frame)

        if cv2.waitKey(1) == 27: # Esc
            break

finally:
    print("終了処理中...")
    picam2.stop()
    cv2.destroyAllWindows()
