# Software
## ハード OS I/O 概要
- cpu : raspi5
- os :raspi OS 
- 使用言語:python3
- serial: servo controll
- i2c: imu / adc

## install
### 1.SDカードを作成
os:
raspi connect

### osとconfigの設定
起動
config.sysの設定
- camera
- i2c
- tty

sudo nano /boot/firmware/config.txt

- fanの設定

### I/O関係の接続確認
- i2c
- imu
- adc
- tty serial servo
- ICS CAMERA
  
rpicam-hello -t 0

rpicam-vid：動画を撮影する

rpicam-hello --list-cameras

rpicam-hello --width 1920 --height 1080

【rpicam-hello編】ラズパイのカメラコマンドまとめたぞ！

https://note.com/wise_boar6814/n/nc1193d2f075b

- 色の変換 (RGB vs BGR):
picamera2で取得した画像はRGBですが、cv2.imshowやcv2.rectangleはBGRとして処理します。変換しないと、画面の青と赤が逆転して表示されます。

- フォーマットの最適化:
XRGB8888 よりも、OpenCVと相性の良い RGB888 を使う方が無駄がありません。

## venv環境
### update

sudo apt update && sudo apt upgrade -y

### 仮想環境をシステムパッケージ共有モードで作る

mkdir begin

cd begin

python3 -m venv venv --system-site-packages

### 再起動してインストール

source venv/bin/activate

pip install --upgrade pip

ipip install ultralytics

pip install mujoco gymnasium stable-baselines3 numpy 

### picamera2はシステム側にあるものを使うので、再インストール不要です

### 仮想環境を抜ける

deactivate


### PCのsimulation dataの移植
