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


