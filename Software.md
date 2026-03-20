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


Raspberry Piをロボットとして運用する場合、電源を入れるだけでプログラムが動き出す**systemd**の設定は必須級のステップですね。

仮想環境（venv）を使用している場合、`ExecStart` に **venv内のPythonパス**を直接指定するのが最もスマートでトラブルの少ない方法です。

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
User=pi
# プログラムがあるディレクトリ
WorkingDirectory=/home/pi/begin
# 仮想環境内のpythonパスを直接指定して実行
ExecStart=/home/pi/begin/venv/bin/python3 main.py
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


---

### PCのsimulation dataの移植
