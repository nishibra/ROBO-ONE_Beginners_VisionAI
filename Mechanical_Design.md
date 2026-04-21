### ROBO-ONE_Beginners_VisionAI
# Mechanical_Design

## 1.コンセプト
このロボットはRaspberry Pi 5を使った画像処理やAIの学習向けのロボットです。
外形寸法はROBO-ONE Beginners auto型と同じですがCPUはRaspi picoからRaspi-5に替わり、カメラが搭載されます。足回りとアーム部は部品点数の低減と組み立て性の改善を図りました。Raspi5を使用し深層学習を実行することから電力消費増と発熱への対応とバッテリの容量アップ品の搭載が可能なものとしました。
#### 全体写真
![VisionAI](pics_mech/VisionAI.png)
#### 全体図
![VisionAI](pics_mech/pi5_Vision_Asy_3D.png)

## 2.CPU case
外形寸法はROBO-ONE Beginners autoのpico CPU caseと同じサイズに収めました。後部のPSD用ブラケットはCPU caseと一体化、前方は分離型のままでTofセンサーは廃止しカメラを使った画像処理で対応することとします。
#### CPU case
CPU case cover締め付けボスにM2.5のインサートを挿入しておきます。挿入方法はROBO-ONE Beginners autoと同じですのでそちらをご参照ください。
CPUはM2.5-8mmのねじでケース下より締め付けます。

![VisionAI](pics_mech/CPU_case.png)
![VisionAI](pics_mech/allParts.png)

下の写真のように事前にヒートシンクを取り付けたCPUボードとハットをマウント用ディスタンスにねじM2.5-4mmをハット上部にねじで締め付けておきます。この時カメラ用フラットケーブルを接続しておきます。詳細は電子回路編でご確認ください。

![VisionAI](pics_mech/distance.png)

### PSD BKT
PSD BKTはCPU caseにM2-5mmのスクリューねじでねじ止めします。

![VisionAI](pics_mech/psd2_bkt.png)

### CPU case cover
CPU case coverはCPU caseに4本のM2.5-8mmねじで締め付けます。更にアームまわりを搭載します。

![VisionAI](pics_mech/CPU_cover.png)

## 3.アーム廻り
アーム廻りは写真のように組み立てます。

![VisionAI](pics_mech/arm_head_asy.png)

#### Pan servo bkt
Pan servo bktにはPan用サーボモーターを4本のM2-5mmで締め付けます。CPU case coverとPan servo bktは4本のM2-10mmスクリューねじで締め付けます。

![VisionAI](pics_mech/Pan_stand.png)
![VisionAI](pics_mech/panAsy.png)

Pan_standを3dプリンターで製作する場合はBrimをつけ、横方向からプリントするようにします。

#### Tilt_bkt and Head
Tiltサーボモーターの固定とヘッドを一体化しました。サーボホーンとの締め付けはM2-8mmのねじで、サーボとの締め付けはM3-8mmで締め付けます。渋りが無いことを確認します。渋りがある場合はペーパーやすりなどで渋り面を仕上げます。

![VisionAI](pics_mech/head.png)

#### Arm
アームとBKTを一体化しました。サーボホーンは両軸とし、いずれもM2-5mmのねじで締め付けます。

![VisionAI](pics_mech/arm_asy.png)

### Head と Armの保護

Head部とArm部には安全や器物保護のためスポンジのドアノブカバーを使用します。
ピンクと紫は半分に切ってHead部に使用します。赤コーナーの場合はピンク、青コーナーは紫です。Headおよびアームはそれぞれスポンジを交換しやすくするためにスリットを入れています。

![donb](pics_mech/doorn.png)  

[購入先](https://amzn.asia/d/89CXsD9) 

購入にあたっては似たようないくつかの製品があり、内径寸法が多少異なる場合がありますので注意してください。

### カメラの取り付け
カメラの取り付けは4本のM2-5mmのスクリューねじで締め付けます。CPUカバーのスリット部からカメラ用フラットケーブルを引き出し接続します。裏表がありますので間違えないようにしてください。

![VisionAI](pics_mech/cameraWOcover.png)

#### camera cover
Camera coverはパチッというまで押し込むと固定されます。

![VisionAI](pics_mech/cameraWcover.png)

### 4.足回り

ロボットのセンサー、電子回路、ソフトウェアは自由に変更できるものとします。またKRS-3300シリーズのすべてのサーボモーターを使用できると同時にバッテリー(Lipoバッテリー2セル/7.4Vなど)は自由に自己責任で使用できます。

### Wheel
wheelは1partsとしました。O-ringを入れることで完成です。

![VisionAI](pics_mech/Wheel_V.png)
![VisionAI](pics_mech/wheel.jpg)

O-ringは以下より購入可能です。

[5個入り Oリング ニトリルゴム 50mm x 60mm x 5mm ブラック](https://www.amazon.co.jp/dp/B07W3BR9TY?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)

サーボモータにはサーボホーンに直接取り付けることができます。ねじはM2-12mmを使用してください。

![VisionAI](pics_mech/ServoTire.jpg) 
  
### シャーシ
キャスタ部にはスライダーを採用しました。滑りやすくなり走行抵抗や走行音が少なくなりました。スライダーはシャーシの取り付け部丸い部分のセンターに取り付けてます。このピッチが90mm,70mm,50mmとあり、昇段昇級の審査に使われます。ボディとの取り付けはM2-10mmのスクリューねじで取り付けます。

![VisionAI](pics_mech/Chassis_V_70.png)
![VisionAI](pics_mech/set_slider.png)

[スライダー購入先](https://www.amazon.co.jp/dp/B0DFGZZ4GH?ref=ppx_yo2ov_dt_b_fed_asin_title)

### body
モノコックとし、サーボモータを90度毎に自由にセットできるようにしました。これにより容量の大きなバッテリーの搭載が可能となります。
リチウムポリマーの7.4V2000mAH程度のバッテリーの搭載が工夫次第で可能です。
CPUケースの取り付けボス部にはインサートを埋め込みます。
M2.5のインサートを使用しています。

![VisionAI](pics_mech/Body_V.png)
![VisionAI](pics_mech/body.jpg)

上の写真のようにサーボモーターを配置するとしたの写真のようにバッテリーが搭載でき、重量バランスがとりやくなります。またCPU caseをくみ上げる前にサーボモーターの設定は行っておきます。ボーレイト125000、IDは右側を1、左側を2と設定するとサンプルプログラムがそのまま使えます。

![VisionAI](pics_mech/set_battery2body.png)

### Battery cover
バッテリの交換性向上のため、Battery coverのねじ止めはやめ、パッチンと挿入できるようにしました。バッテリーを交換したらカバーの片側を挿入し反対側を押し込んでください。外すときは上部の半円の部分に爪で出ているのでこれを引っ張り外してください。3Dプリンターで製作する場合はBrimを付けてください。

![VisionAI](pics_mech/Battery_cover.png)
![VisionAI](pics_mech/set_bat_cover.png)

### stlデータ
3dprinterで使用できるstlファイルはstlフォルダーにありますのでご利用ください。セット面をサポートなしでプリントできるよう考えて見てください。すべてサポートなしでプリント可能です。
