# Mechanical_Design

## 全体デザイン

外形はauto型と同じですがCPUはRaspi5に替わり、カメラが搭載されます。シャーシとアームサーボ受け部は部品点数の低減と組み立て整備性の改善を図りました。

![VisionAI](pics_mech/VisionAI.png)

![VisionAI](pics_mech/pi5_Vision_Asy_3D.jpg)


### CPU case

Raspi5を使用し深層学習を走らせることから冷却系の考慮とバッテリへの容量アップが搭載可能なものとしました。


![VisionAI](pics_mech/CPU_case.png)
![VisionAI](pics_mech/CPU_cover.png)


![VisionAI](pics_mech/psd1_bkt.png)
![VisionAI](pics_mech/psd2_bkt.png)

### Wheel
wheelは1partsとしました。O-ringを入れることで完成です。

![VisionAI](pics_mech/Wheel_V.png)
![VisionAI](pics_mech/wheel.jpg)

O-ringは以下より購入可能です。

[O-ring](https://www.amazon.co.jp/dp/B07W3BR9TY?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)

サーボモータにはサーボホーンに直接取り付けることができます。ねじはM2-12mmを使用してください。
![VisionAI](pics_mech/ServoTire.jpg) 
  
### シャーシ
キャスタにはカグスベールを採用しました。滑りやすくなり走行抵抗や走行音が少なくなりました。カグスベールはシャーシのキャスター取り付け部の丸い部分のセンターに取り付けてください。ボディとの取り付けは2mのスクリューねじで取り付けます。

![VisionAI](pics_mech/chassis.jpg)
![VisionAI](pics_mech/Chassis_V_90.png)

### body
モノコックとし、サーボモータを90度毎に自由にセットできるようにしました。これにより容量の大きなバッテリーの搭載が可能となります。
リチウムポリマーの7.4V2000mAH程度のバッテリーの搭載が工夫次第で可能です。
CPUケースの取り付けボス部はねじを埋め込みます。

![VisionAI](pics_mech/Body_V.png)

バッテリの交換性向上のためねじ取り付けはやめ、パッチンと挿入できるようにしました。バッテリーを取り際したらカバーを下部より押し込んでください。外すときは上部の半円の切り欠き部に指を入れ引っ張り外してください。

![VisionAI](pics_mech/BatteryCover.jpg)
![VisionAI](pics_mech/Battery_cover.png)



 Amazon
### CPU cover
### yhoo servo bkt
![VisionAI](pics_mech/Pan_stand.png)


![VisionAI](pics_mech/How2set.jpg)



### tilt bkt
![VisionAI](pics_mech/Tilt_bkt.png)

### arm bkt
![VisionAI](pics_mech/kote_v1.png)

### PSDセンサーBKT

### armとHeadは同じ

![VisionAI](pics_mech/SetCamera.jpg)
![VisionAI](pics_mech/SetCamera2.jpg)

![VisionAI](pics_mech/arm_bkt.png)
![VisionAI](pics_mech/camera_cover.png)



![VisionAI](pics_mech/doorn.png)
![VisionAI](pics_mech/head.png)

---
![VisionAI](pics_mech/ins.png)
![VisionAI](pics_mech/insert.png)
---





  
### stlデータ
