### ROBO-ONE_Beginners_VisionAI
# Simulation

## 環境
-Windows11
---
## Python 

## Mujoco シミュレーション
- Mujoco model
- 画像処理と追従
- Yolo11
- 相手の認識　物体認識
- リングの認識　セグメンテーション
## Baseline　深層強化学習

## Yolo11 深層機械学習
---

## Pythonのインストール
Windows 11へのPythonインストールは、公式サイトのインストーラー（.exe）を使用するのが最適です。Python公式サイトの「Downloads」から最新版（3.13〜）をダウンロードし、インストール画面で必ず「Add Python.exe to PATH」にチェックを入れてインストールしてください。これにより、コマンドプロンプトやターミナルで python コマンドが使用可能になります。 

### Pythonのインストール手順 (Windows 11)
公式サイトからダウンロード: Python.orgにアクセスし、Windows用の最新版インストーラー（64-bit）をダウンロードします。
インストール実行: ダウンロードしたファイルを実行します。
Pathへの追加 (最重要): 最初の画面下部にある「Add Python.exe to PATH」のチェックボックスを必ずチェックします。
インストール: 「Install Now」をクリックします。
インストール完了: 完了画面が出たら「Close」を押します。 

### インストールの確認
Windowsターミナル（またはコマンドプロンプト/PowerShell）を開き、以下のコマンドを入力してバージョンが表示されれば成功です。 

```bash
python --version
```

### おすすめの設定と環境
* 推奨ツール: VS Code（Visual Studio Code）をインストールし、Python拡張機能を追加すると開発がスムーズに行えます。
* WSL2の利用: Linux環境で開発したい場合は、Windowsターミナルから wsl --install を実行し、WSL2（Ubuntuなど）を導入する手法も推奨されます。
* 注意点: Microsoft Store版は、pipでのパッケージインストール時にパスのトラブルが起きる可能性があるため、公式サイト版が推奨されることが多いです。 

### アンインストール方法
* もしバージョンを入れ直したい場合は、Windowsの「設定」>「アプリ」>「インストールされているアプリ」からPythonを選択し、アンインストールできます。 


## 開発環境（venv）の構築
OS標準のPython環境を汚さないよう、仮想環境（venv）を使用します。Trixieでは pip install を直接行うとエラーになるため、この手順は必須です。

仮想環境の作成と有効化
sudo apt update && sudo apt upgrade -y
mkdir ~/robot_project
cd ~/robot_project

### システムパッケージ（Picamera2など）を共有して作成
python3 -m venv venv --system-site-packages

### 有効化（作業開始時に毎回実行）
source venv/bin/activate
必要なライブラリのインストール
pip install --upgrade pip
pip install ultralytics  # YOLOv8 (物体認識)
pip install mujoco gymnasium stable-baselines3  # 強化学習セット
pip install numpy
補足: ultralytics を入れることで、カメラ映像から即座にリアルタイム物体検知が可能になります。

[venvについて](https://saas.n-works.link/programming/python/python_virtualenv_how_to_buildavirtualenvironment)

## Mujoco Modelの作成

|番号	|部品名	|重量	|個数 |合計
| :--- | :--- | :--- | :--- |
|1	|CPU case CPU	|170	|1	|170|
|2	Wheel asy	15	2	30
|3	アーム	        50	1	50
|4	head	        26	1	26
|5	stand	        12	1	12
|6	Body/S/B.cover	80	1	80
|7	krs3301	        28	4	112
|8	バッテリー	90	1	90
|	|合計		|    |     |	570



