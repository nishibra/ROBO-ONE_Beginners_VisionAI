# Software 解説

このロボットはRaspberry Pi 5を使用した初心者向けのVision AI型ロボットです。最新のAIライブラリを活用し、物体認識などの機械学習や、シミュレーションを用いた強化学習を学ぶことができます。

## ハード / OS / I/O 概要

* **CPU**: Raspberry Pi 5 (Memory 4GB以上推奨)
* **OS**: Raspberry Pi OS Trixie (Debian 13) 64-bit
* **言語**: Python 3.11以降
* **通信プロトコル**:
* **Serial (UART)**: サーボモーター制御用 (KRSサーボ等)
* **I2C**: IMU (慣性計測装置) / ADC (アナログ-デジタル変換) 用



## Install 手順

### 1. SDカードの作成

Raspberry Pi Imagerを使用し、OSを選択します。

* **OS**: Raspberry Pi OS (64-bit) ※Trixieが選択可能な場合
* **設定**: 書き込み時に「OSカスタマイズ」でホスト名、Wi-Fi、SSHを有効にしておくと、その後の作業がスムーズです。

### 2. OSとConfigの設定

Raspberry Pi 5を起動し、ターミナルで以下の設定を行います。

#### インターフェースの有効化

`sudo raspi-config` を実行し、以下の項目を **Enable** にします。

* Interface Options -> **I2C**
* Interface Options -> **Serial Port** (Login shell: No / Hardware: Yes)
* Interface Options -> **VNC** (必要に応じて)

#### Raspberry Pi Connect のセットアップ

ブラウザ経由でリモートデスクトップ操作を可能にします。

```bash
sudo apt update
sudo apt install rpi-connect
# インストール後、画面右上のアイコンまたはコマンドでサインイン

```

#### 冷却ファンの設定

`sudo nano /boot/firmware/config.txt` を開き、末尾に追記します。

```text
[all]
dtoverlay=gpio-fan,gpiopin=19,temp=50000

```

> **Note**: `temp=50000` は50℃でファンが始動することを意味します。AI処理中は発熱が激しいため、この設定は必須です。

### 3. I/O関係の接続確認

接続されたデバイスが認識されているか確認します。

```bash
# I2Cデバイスの確認（アドレスが表示されればOK）
i2cdetect -y 1

# シリアルポートの確認
ls /dev/ttyAMA0

```

---

## カメラ（rpicam-apps / Picamera2）の使い方

Raspberry Pi 5では従来の `raspistill` ではなく `rpicam-apps` を使用します。

### 基本コマンド

* **プレビュー表示**: `rpicam-hello -t 0`
* **カメラ一覧確認**: `rpicam-hello --list-cameras`
* **静止画保存**: `rpicam-still -o test.jpg`

### Pythonでの画像処理（重要）

OpenCVとPicamera2を組み合わせる際、色の並び（色空間）に注意が必要です。

* **色の変換**: Picamera2は **RGB** 形式で画像を取得しますが、OpenCV（cv2）は **BGR** 形式として処理します。
```python
# 変換例
import cv2
img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

```


* **フォーマット**: メモリ効率を上げるため、`format='RGB888'` を指定してキャプチャすることを推奨します。

---

## 開発環境（venv）の構築

OS標準のPython環境を汚さないよう、仮想環境（venv）を使用します。Trixieでは `pip install` を直接行うとエラーになるため、この手順は必須です。

### 仮想環境の作成と有効化

```bash
sudo apt update && sudo apt upgrade -y
mkdir ~/robot_project
cd ~/robot_project

# システムパッケージ（Picamera2など）を共有して作成
python3 -m venv venv --system-site-packages

# 有効化（作業開始時に毎回実行）
source venv/bin/activate

```

### 必要なライブラリのインストール

```bash
pip install --upgrade pip
pip install ultralytics  # YOLOv8 (物体認識)
pip install mujoco gymnasium stable-baselines3  # 強化学習セット
pip install numpy

```

> **補足**: `ultralytics` を入れることで、カメラ映像から即座にリアルタイム物体検知が可能になります。

---

## 運用アドバイス

1. **起動時自動実行**: ロボットとして自律動作させる場合は、`systemd` を使って venv 内の python スクリプトを自動起動する設定を追加すると便利です。
2. **電力不足注意**: Raspberry Pi 5は 5V/5A の電源を推奨します。AI処理中にカメラやサーボを動かすと電圧降下（低電圧警告）が発生しやすいため、高品質な電源を使用してください。

---










### PCのsimulation dataの移植
