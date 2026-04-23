### ROBO-ONE_Beginners_VisionAI
# Software
## コンセプト
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
* プレビュー表示: `rpicam-hello -t 0`
* カメラ一覧確認: `rpicam-hello --list-cameras`
* 静止画保存: `rpicam-still -o test.jpg`

### Pythonでの画像処理
OpenCVとPicamera2を組み合わせる際、色の並び（色空間）に注意が必要です。
* 色の変換: Picamera2は RGB形式で画像を取得しますが、OpenCV（cv2）はBGR形式として処理します。
```python
# 変換例
import cv2
img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
```
* フォーマット: メモリ効率を上げるため、`format='RGB888'` を指定してキャプチャすることを推奨します。
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
シミュレーション環境や画像処理のライブラリーをインストールします。mujocoやYoloがRaspi5でも使えます。

```bash
pip install --upgrade pip
pip install ultralytics  # YOLOv26 (物体認識)
pip install mujoco gymnasium stable-baselines3  # 強化学習セット
pip install numpy

```
* Yolo26: `ultralytics` を入れることで、OpenCVも導入されるので、カメラ映像から即座にリアルタイム物体検知や処理が可能になります。
* 起動時自動実行: ロボットとして自律動作させる場合は、`systemd` を使って venv 内の python スクリプトを自動起動する設定を追加すると便利です。
* 電力不足注意: Raspberry Pi 5は 5V/5A の電源を推奨します。AI処理中にカメラやサーボを動かすと電圧降下（低電圧警告）が発生しやすいため、高品質な電源を使用してください。

---

## KRSのコントロール


## IMU I2C取り込み


## ADC PSD取り込み
Raspberry Pi 5（ラズパイ5）で高性能な16bit ADC（アナログ-デジタルコンバータ）である**ADS1115**を使用する方法を解説します。
ラズパイ5では、これまでのモデルと異なりGPIOの制御方式が変更されていますが、Pythonのライブラリ（Adafruit CircuitPython）を使用すれば、従来通り簡単に扱うことができます。

### 1. 配線（接続方法）

ADS1115は**I2C**プロトコルを使用します。ラズパイ5のピン配置に合わせて以下のように接続してください。

| ADS1115 ピン | Raspberry Pi 5 ピン | 役割 |
| :--- | :--- | :--- |
| **VDD** | 3.3V (Pin 1) | 電源 (3.3V推奨) |
| **GND** | GND (Pin 9) | グラウンド |
| **SCL** | SCL (Pin 5) | I2C クロック |
| **SDA** | SDA (Pin 3) | I2C データ |
| **ADDR** | GNDへ接続 | I2Cアドレスを `0x48` に設定 |

### 2. ラズパイの設定

まず、I2Cインターフェースを有効にする必要があります。

1.  ターミナルで `sudo raspi-config` を実行。
2.  **Interface Options** -> **I2C** を選択し、**Yes** を選んで有効化します。
3.  再起動後、正しく認識されているか確認します。
    ```bash
    ls /dev/i2c*
    ```
    `/dev/i2c-1` が表示されればOKです。

### 3. ライブラリのインストール

ラズパイ5では、Python環境の競合を避けるために**仮想環境（venv）**の使用が推奨されています。

```bash
# 仮想環境の作成と有効化
python -m venv env
source env/bin/activate

# 必要なライブラリのインストール
pip install adafruit-circuitpython-ads1x15
```
### 4. Pythonコードの例
以下のコードは、`A0`ピンに入力された電圧を読み取り、コンソールに表示するシンプルな例です。

```python
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# I2Cバスの初期化
i2c = busio.I2C(board.SCL, board.SDA)

# ADS1115オブジェクトの作成
ads = ADS.ADS1115(i2c)

# A0ピンをアナログ入力として設定
chan = AnalogIn(ads, ADS.P0)

print(f"{'電圧(V)':>10} {'数値':>10}")
print("-" * 25)

try:
    while True:
        # chan.value は 0-65535 の範囲 (16bit)
        # chan.voltage は 実際の電圧
        print(f"{chan.voltage:10.4f}V {chan.value:10}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n終了します")
```

知っておくと役立つポイント
* ゲイン（増幅率）の設定:
    デフォルトでは最大4.096Vまで測定可能です。これより小さい電圧を精密に測りたい場合は、`ads.gain = 2`（最大2.048V）のように設定変更できます。
* 差動入力:
    2つのピンの電圧差を測る場合は、`AnalogIn(ads, ADS.P0, ADS.P1)` のように指定します。
* サンプリングレート:
    `ads.data_rate = 860` と設定することで、秒間最大860回の高速サンプリングが可能です。
---

## Game controllerの接続
RaspiOSに接続します。




---

## systemd による自動起動の設定手順

### 1. サービスファイルの作成

以下のコマンドで、新しいサービス設定ファイルを作成します（ファイル名は `my_robot.service` とします）。

```bash
sudo nano /etc/systemd/system/my_robot.service

```

### 2. 設定内容の記述

以下の内容をコピー＆ペーストしてください。各パスはご自身の環境に合わせて書き換えてください。

```ini
[Unit]
Description=My Vision AI Robot Service
After=network.target

[Service]
# 実行ユーザー（通常は pi）
User=nishi
# プログラムがあるディレクトリ
WorkingDirectory=/home/nishi/begin
# 仮想環境内のpythonパスを直接指定して実行
ExecStart=/home/nishi/begin/venv/bin/python3 /home/nishi/begin/rf/main.py
# 異常終了した時に5秒後に再起動する設定
Restart=always
RestartSec=5
# 標準出力（ログ）の送り先
StandardOutput=inherit
StandardError=inherit

[Install]
WantedBy=multi-user.target

```

### 3. サービスの有効化と起動

ファイルを保存（`Ctrl+O` -> `Enter`）し、エディタを終了（`Ctrl+X`）したら、以下のコマンドでシステムに反映させます。

```bash
# 設定の再読み込み
sudo systemctl daemon-reload

# 自動起動の有効化
sudo systemctl enable my_robot.service
# 無効化
sudo systemctl disable my_robot.service
# 今すぐ起動（テスト）
sudo systemctl start my_robot.service

```

---

## 運用で役立つコマンド

自動起動を設定した後は、画面に何も表示されないため「本当に動いているか？」を確認する術を知っておく必要があります。

* **状態の確認**:
`systemctl status my_robot.service`
（実行中か、エラーで止まっているかが一目でわかります）
* **ログのリアルタイム確認**:
`journalctl -u my_robot.service -f`
（Pythonの `print()` 内容をリアルタイムで監視できます。デバッグに最適です）
* **停止・再起動**:
`sudo systemctl stop my_robot.service` / `sudo systemctl restart my_robot.service`

---

## 注意点：GUIが必要な場合

もしプログラム内で `cv2.imshow` などの**ウィンドウを表示するコード**が含まれている場合、通常の systemd ではエラーになります。その場合は、プログラム側でウィンドウ表示をオフにするか、デスクトップ環境が立ち上がってから実行される `autostart` 方式に切り替える必要があります。

**次は、「プログラムがエラーで落ちた時のログを保存する方法」や「特定のI/Oデバイスが準備できるまで起動を待機させる設定」などについて詳しく解説しましょうか？**


ご提示いただいた解説文は、手順の全体像は掴めますが、初めて挑戦する方にとっては「どこでその操作をするのか」「具体的な設定画面はどこか」が少し分かりにくいかもしれません。

以下に、初心者の方でも迷わず進められるよう、情報の補足と整理を行った構成案を作成しました。

---

## 【補足版】Raspberry Pi Connect の導入・利用手順

Raspberry Pi Connectを使うと、ブラウザ越しにどこからでもRaspberry Piのデスクトップにアクセスできます。セットアップを以下のステップに分けて解説します。

### 1. 準備：OSのインストール

Raspberry Pi Connectを利用するには、OSのバージョンと種類が重要です。

* **OSの選択:** **Raspberry Pi OS (64-bit)** の最新版（Bookworm以降）をインストールしてください。
* ※Raspberry Pi 4 / 5 / 400 が推奨されています。
* ※デスクトップ版（Desktop）を選択してください（Lite版は非対応です）。


* **書き込み:** 公式の「Raspberry Pi Imager」を使ってmicroSDカード（またはSSD）に書き込み、Raspberry Piを起動します。

### 2. Raspberry Pi ID の作成

あらかじめ、管理用の公式アカウントを作成しておくとスムーズです。

* [Raspberry Pi ID 登録ページ](https://id.raspberrypi.com/) にアクセスし、メールアドレスでアカウントを作成・サインインしておきます。

### 3. Connect サービスの有効化（本体側の操作）

Raspberry Piが起動したら、機能をオンにします。

1. **インストール（必要な場合）:**
ターミナルを開き、念のため最新の状態に更新してインストールを確認します。
```bash
sudo apt update
sudo apt install rpi-connect

```


2. **機能を有効化:**
メニューの「設定」→「Raspberry Pi Configuration」→「Interfaces」タブの中に「Raspberry Pi Connect」という項目があれば **ON** にします。
（または、ターミナルで `systemctl --user enable rpi-connect` を実行します）

### 4. デバイスの紐付け（リンク）

ここが最も重要なステップです。

1. Raspberry Piのデスクトップ右上（タスクバー）に、Connectのアイコン（雲のようなマーク）が表示されます。
2. アイコンをクリックし、**[Sign In]** を選択します。
3. ブラウザが立ち上がり、「このRaspberry Piをあなたのアカウントに登録しますか？」という画面（Link Device）が表示されます。
4. **デバイス名を入力:** 自分が管理しやすい名前（例: `My-RasPi5` など）を付けて、[Link Device] ボタンを押します。

### 5. 外部から接続する

設定が完了したら、別のPCやスマホのブラウザから操作可能です。

1. 接続元PCのブラウザで [https://connect.raspberrypi.com/devices](https://connect.raspberrypi.com/devices) にアクセスします。
2. 自分のRaspberry Pi IDでサインインします。
3. 登録したデバイスの一覧が表示されるので、右側にある **[Connect]** ボタンをクリックします。
4. これでブラウザ内にRaspberry Piのデスクトップが表示されます！


---

### 「ボタンを押した瞬間に、別のPythonスクリプトやシステムコマンド（プログラム）を起動したい」

Python標準ライブラリの `subprocess` を組み合わせるのが一般的です。

### 1. 別のPythonスクリプトを起動する場合
例えば、ボタンを押すと `web_server.py` という別のプログラムをバックグラウンドで起動する例です。

```python
from gpiozero import Button
from signal import pause
import subprocess

def start_program():
    print("プログラムを起動します...")
    # 別のPythonスクリプトを非同期で実行
    subprocess.Popen(["python3", "web_server.py"])

button = Button(13)

# 割り込みで関数を呼び出す
button.when_pressed = start_program

pause()
```

---

### 2. シェルコマンドやアプリを起動する場合
システムコマンド（例えば、カメラの録画開始や音楽再生など）を動かす場合も同様です。

```python
import subprocess
from gpiozero import Button

def run_command():
    # 例：システムをシャットダウンする、または特定のアプリを開く
    # subprocess.run(["ls", "-l"]) # テスト用にファイル一覧を表示
    subprocess.Popen(["vlc", "music.mp3"]) # 音楽プレーヤーを起動

button = Button(13)
button.when_pressed = run_command
```

---

### 重要なポイント：`run` と `Popen` の違い
プログラムを「起動」させる際、用途によって使い分ける必要があります。

* **`subprocess.run()`**: そのプログラムが**終わるまで、メインのPythonスクリプトが止まります**（同期処理）。
* **`subprocess.Popen()`**: そのプログラムを**裏で起動し、メインのスクリプトはすぐに次の処理へ進みます**（非同期処理）。「ボタンを押してアプリを立ち上げる」なら、こちらがスムーズです。

---

### 注意点：多重起動の防止
今のコードだと、ボタンを連打するとプログラムが何個も立ち上がってしまい、ラズパイのメモリを圧迫する可能性があります。

もし「既に起動していたら何もしない」という風にしたい場合は、以下のようにフラグ管理をするのがスマートです。

```python
process = None

def start_program():
    global process
    # プロセスがまだ動いていない（または終了している）かチェック
    if process is None or process.poll() is not None:
        print("新規起動します")
        process = subprocess.Popen(["python3", "target_script.py"])
    else:
        print("既に実行中です")
```
`systemd` はバックグラウンド（画面なし）で動くのが得意ですが、**OpenCVの `cv2.imshow` でプレビュー画面を出したい**場合や、デスクトップが立ち上がってからGUIアプリとして起動したい場合は、**Wayland/Wayfire の Autostart** 方式を使います。

Raspberry Pi 5（Raspberry Pi OS 64-bit）はデフォルトの表示サーバーが **Wayland** になっているため、従来の `~/.config/lxsession/...` 方式ではなく、以下の手順で行うのが最も確実です。

---

## 1. 自動起動用ディレクトリの作成
まず、自動起動設定ファイルを置くためのディレクトリを作成します（既にある場合は飛ばしてOKです）。

```bash
mkdir -p ~/.config/autostart
```

## 2. デスクトップエントリーファイルの作成
次に、起動したいプログラムの情報を記した `.desktop` ファイルを作成します。

```bash
nano ~/.config/autostart/robot_gui.desktop
```

中身を以下のように記述してください。

```ini
[Desktop Entry]
Type=Application
Name=Robot Vision AI
# 仮想環境のpythonパス + 実行するスクリプトのフルパス
Exec=/home/pi/begin/venv/bin/python3 /home/pi/begin/main.py
# 起動時のカレントディレクトリ
Path=/home/pi/begin
# ターミナルを表示させたい場合は true
Terminal=false
# 自動起動を有効にする
X-GNOME-Autostart-enabled=true
```

## 3. 実行権限の付与
作成したファイルに実行権限を与えます。

```bash
chmod +x ~/.config/autostart/robot_gui.desktop
```

これで、次回再起動した際に**デスクトップ画面が表示された直後**にプログラムが動き出します。

---

## 注意点とデバッグのコツ

### ① パスは必ず「フルパス」で
`python3` や `main.py` とだけ書くと、システムが場所を見つけられず起動に失敗します。必ず `/home/pi/...` から始まるフルパスで記述してください。

### ② ネットワーク待ち（重要）
もしプログラム内で「ネットからAIモデルをダウンロードする」や「特定のIPに通信する」処理がある場合、デスクトップ起動直後はまだWi-Fiがつながっていないことがあります。その場合は、Pythonコードの冒頭に数秒の待機を入れるのが簡単で確実です。

```python
import time
time.sleep(10)  # 起動後10秒待ってからメイン処理を開始
```

### ③ ログの確認方法
Autostart方式は `systemctl status` のような便利な確認コマンドがありません。エラーで動かない場合は、以下のように記述してログをファイルに書き出すようにすると原因が特定しやすくなります。

```ini
# Execの行を以下のように書き換えてログを保存
Exec=/bin/bash -c '/home/pi/begin/venv/bin/python3 /home/pi/begin/main.py > /home/pi/robot_debug.log 2>&1'
```

---

**次は、この自動起動を「特定のスイッチを押したときだけ解除する」ような、現場で役立つ運用テクニックについて解説しましょうか？**

---

### PCのsimulation dataの移植
高精度な9軸センサーである**BNO055**は、内部で姿勢計算（クォータニオン出力）を行ってくれるため、実機展開には非常に適したセンサーです。

実機にセットアップし、MuJoCoの学習済みモデル（25次元や26次元の観測データ）に適合させるための手順を解説します。

---

### 1. 物理的なセットアップ（ハードウェア）

BNO055は一般的にI2Cで通信します。Raspberry PiやArduino等と接続します。

* **配置**: ロボットの「重心」かつ「ベースリンク（車軸の中央など）」に、基板が水平になるように固定してください。
* **向き**: BNO055の基板に印字されている **X/Y/Z軸の方向**を、MuJoCo上の `base_link` の軸方向と一致させることが非常に重要です。



---

### 2. ソフトウェアの準備（Raspberry Piの場合）

Adafruitのライブラリを使用するのが最も簡単です。

```bash
pip install adafruit-circuitpython-bno055
```

---

### 3. 実機用推論サンプルスクリプト

このスクリプトは、シミュレーション（MuJoCo）での観測値の並び順に合わせて、実機のセンサーデータを整形してAI（PPO）に入力する流れを示しています。

```python
import time
import board
import busio
import adafruit_bno055
import numpy as np
from stable_baselines3 import PPO

# --- 1. センサーと通信の初期化 ---
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

# --- 2. モデルのロード ---
# 学習済みの「起き上がり・バトル用モデル」を指定
model = PPO.load("ppo_robot_opencv_v2.zip")

def get_real_obs():
    """実機からMuJoCoの観測形式(25次元など)を作成する"""
    
    # A. 自己状態（qpos/qvel相当）の取得
    # 実機では関節角度(エンコーダ)やジャイロから取得
    # ここでは例としてダミーまたは現在のサーボ角度を使用
    joint_angles = [0.0] * 7  # qpos[0:7]相当
    joint_velocities = [0.0] * 6  # qvel[0:6]相当
    
    # B. 直立判定（upright）の取得
    # BNO055のクォータニオンから上向きベクトル(Z軸成分)を計算
    quat = sensor.quaternion  # (w, x, y, z)
    # 簡易的には、重力ベクトルのZ成分を使用
    # 直立時に 1.0, 転倒時に 0.0 になるようスケーリング
    gravity = sensor.gravity # (x, y, z)
    upright = gravity[2] / 9.8 

    # C. OpenCV特徴量（cx, cy, area）の取得
    # 実機カメラ(Webcam/PiCam)で赤色抽出を行う関数（前述のOpenCV処理）
    # cv_features = get_real_camera_features() 
    cv_features = [0.0, 0.0, 0.0] # ターゲットが見えない場合は0

    # 学習時の観測ベクトル（25次元）に結合
    # [qpos(7), qvel(14), upright(1), cv(3)] のような並び順を維持
    obs = np.concatenate([
        joint_angles, 
        joint_velocities, 
        [upright], 
        cv_features
    ]).astype(np.float32)
    
    return obs

def apply_action(action):
    """AIの出力を実機のサーボ命令に変換"""
    # 不感帯補正 (学習時と同じロジック)
    a_s = np.sign(action) * (0.25 + 0.75 * np.abs(action))
    
    # サーボ角度への変換（スケーリング）
    # 例: action=1.0 -> 1500μs, action=-1.0 -> 500μs など
    target_pwms = [
        int(1500 + a_s[0] * 500), # 右タイヤ
        int(1500 + a_s[1] * 500), # 左タイヤ
        # アーム類も同様に変換
    ]
    # hw.send_pwm(target_pwms) # 実機へ送信

# --- メインループ ---
print("BNO055キャリブレーション待ち...")
while not sensor.calibrated:
    pass

print("推論ループ開始")
while True:
    start_t = time.time()
    
    # 状態取得
    obs = get_real_obs()
    
    # 推論 (決定論的 = deterministic=True)
    action, _ = model.predict(obs, deterministic=True)
    
    # モーター駆動
    apply_action(action)
    
    # 制御周期の同期 (シミュレーションに合わせる: 例 50Hz)
    elapsed = time.time() - start_t
    time.sleep(max(0, 0.02 - elapsed))
```

---

### 4. 実機展開を成功させるコツ

1.  **キャリブレーション**:
    BNO055は電源投入直後は精度が低いです。ロボットを「8の字」に動かすなどして、`sensor.calibrated` が True になるのを確認してから推論を開始してください。
    

2.  **座標系の変換 (重要)**:
    MuJoCoの座標系は **右手系 (Zが上)** です。BNO055が返す重力ベクトルや方位の軸が、MuJoCoのシミュレーション空間と矛盾していないか、事前に値を表示して確認してください（逆方向に傾くとAIがパニックになります）。

3.  **ノイズ対策**:
    実機のBNO055は振動に敏感です。モーターが回るとデータが跳ねるため、`sensor.gravity`（重力補正済み加速度）を使用するか、単純な移動平均フィルタを通してAIに渡すと安定します。
    

4.  **不感帯の再設定**:
    実物の床の摩擦は MuJoCo と異なります。実機が「震えるだけで動かない」場合は、`DEADZONE` の値を `0.25` から少しずつ上げ下げして、動き出しがスムーズなポイントを探してください。

まずは **「BNO055の傾き値（Z成分）を表示させて、ロボットを倒すと0に近づき、立てると1に近づくか」** を確認することから始めるのが確実です。

### yolo26
https://docs.ultralytics.com/ja/models/yolo26/
