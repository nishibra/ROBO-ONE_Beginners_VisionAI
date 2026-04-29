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
### Pythonのインストール手順 (Windows)
* 公式サイトからダウンロード: Python.orgにアクセスし、Windows用の最新版インストーラー（64-bit）をダウンロードします。
* インストール実行: ダウンロードしたファイルを実行します。
* Pathへの追加 (最重要): 最初の画面下部にある「Add Python.exe to PATH」のチェックボックスを必ずチェックします。
* インストール: 「Install Now」をクリックします。
* インストール完了: 完了画面が出たら「Close」を押します。 

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
OS標準のPython環境を汚さないよう、仮想環境（venv）を使用します。

### システムパッケージ（Picamera2など）を共有して作成
python3 -m venv venv 

### 有効化（作業開始時に毎回実行）
```
.\venv\Scripts\activate

必要なライブラリのインストール
python.exe -m pip install --upgrade pip
pip install ultralytics  # YOLOv8 (物体認識)
pip install mujoco gymnasium stable-baselines3  # 強化学習セット
pip install numpy
```

補足: ultralytics を入れることで、カメラ映像から即座にリアルタイム物体検知が可能になります。

[venvについて](https://saas.n-works.link/programming/python/python_virtualenv_how_to_buildavirtualenvironment)
---


## Mujocoについて


[物理エンジンMuJoCoの紹介](https://qiita.com/Yayoi-Habami/items/1bf5a3e05b1516a90381)

URDFとMujoco modelの違い
* 1. 形状指定（size）の違い: URDFの <box size="0.1 0.1 0.5"/> は「全幅」ですが、MuJoCoの <geom size="0.05 0.05 0.25"/> は 中心からの距離（Half-extents） です。そのため、値を半分にする必要があります。

* 2. ジョイントの記述: URDF: parent と child を指定して繋ぐ。
MuJoCo: body タグを 入れ子（階層構造） にすることで親子関係を表現します。

* 3. アクチュエータ（Actuator）:
URDFには「どう動かすか」の記述がありませんが、MuJoCoでシミュレーションを行うには <actuator> セクションが必要です。ここでは、URDFの effort（30）を ctrlrange として設定したモータを定義しました。

* 4. 慣性の自動計算:
MuJoCoは非常に賢いので、<geom> に mass="1" と書くだけで、その形状（box）に基づいた適切な慣性テンソルを自動的に計算してくれます。URDFのように複雑な慣性行列を自分で書く必要はありません（もちろんカスタム設定も可能です）。

###  VS Code のダウンロードとインストール
Windows の場合
* 公式サイトにアクセスし、**「Download for Windows」**をクリックしてインストーラー（.exe）をダウンロードします。

https://code.visualstudio.com/download
 
* ダウンロードしたファイルを実行し、基本的には「次へ」で進めます。
* ポイント: 途中の「追加タスクの選択」画面で、以下の 2 つにチェックを入れるのがおすすめです。
* 「エクスプローラーのファイルコンテキストメニューに [Code で開く] アクションを追加する」
* これを有効にすると、XML ファイルを右クリックしてすぐ VS Code で開けるようになります。

### 2. 重要な 4 つの要素
#### ① <body>（剛体）
ロボットの各パーツ（リンク）です。
* pos: 親の座標系から見た相対位置。
* quat または euler: 回転（クォータニオンまたはオイラー角）。
#### ② <joint>（関節）
その <body> が親に対してどう動くかを定義します。
*type: hinge（回転）, slide（直動）, free（浮遊）など。
* axis: 回転軸（例: 0 0 1 は z 軸まわり）。
* range: 可動範囲（例: -1.57 1.57）。

#### ③ <geom>（形状・物理特性）
見た目、当たり判定、そして質量を定義します。
* type: __box, sphere, cylinder, capsule, mesh（STLファイルなど）__
* size: 形状のサイズ。※注意：URDFと違い、中心からの距離（半径や半分の長さ）で指定します。
* mass: 質量。指定すると慣性モーメントを自動計算してくれます。

#### ④ <actuator>（動力）
ロボットをどう動かすか。worldbody の外に書きます。
* __motor: トルク制御。__
* __position: 位置制御（サーボモータに近い挙動）。__
* __velocity: 速度制御。__

#### <freejoint/>:
 車両全体がワールド内を移動できるようにするために必須です。これがないと、ロボットはその場に固定されてしまいます。

#### quat（クォータニオン）: 
 MuJoCoの円柱（cylinder）はデフォルトでZ軸方向を向いています。タイヤを横に向けるために quat="0.707 0.707 0 0" を使い、X軸まわりに90度回転させています。

#### キャスターの摩擦 (friction="0 0 0"): 
本来ならキャスターも可動パーツにするのが正確ですが、簡易モデルでは球体（sphere）を配置し、摩擦をゼロに設定することで、床の上を滑る「支え」として機能させます。

#### <velocity> アクチュエータ: 
車輪の制御には motor（トルク制御）よりも velocity（速度制御）を使うのが直感的です。data.ctrl[0] に値を入れると、その速度（rad/s）でタイヤが回ります。

### 回転させたい方向
よく使う回転パターン表「とりあえずこれを試す」という値をまとめました。
```
  オイラー角 (euler)  クォータニオン (quat)
X軸まわりに90°  1.57 0 0    0.707 0.707 0 0
X軸まわりに180° 3.14 0 0    0 1 0 0
Y軸まわりに90°  0 1.57 0    0.707 0 0.707 0
Z軸まわりに90°  0 0 1.57    0.707 0 0 0.707
```
### プレビューしながら書く方法
VS CodeでXMLを書いている横で、MuJoCoの simulate アプリを開いておいてください。

__XMLを保存（Ctrl + S）。
simulate アプリの画面上で Ctrl + L（リロード）を押す。__

即座に変更が反映されます。

## Mujoco Modelの作成

| 番号 | 部品名 | 重量 | 個数 | 合計 |
| :--- | :--- | :--- | :--- | :--- |
| 1	| CPU case/cover/ CPU	| 170	| 1	| 170 |
| 2 | Wheel asy	| 15 | 2 | 30 | 
| 3 |	Arm asy	| 50 | 1 | 50 | 
| 4 | head asy	| 26 | 1 | 26 | 
| 5 | stand asy | 12 | 1 | 	12| 
| 6 | Body/chassis/Bat.cover	| 80	| 1| 	80 | 
| 7 | krs3301 | 28 | 4 | 112 | 
| 8 | Battery	| 90	| 1 | 	90 | 
|	| 合計		|    |     |	570 | 

Assyの重心はArmを中段の構えとし、X軸は両車輪の中心、y軸は両車輪の回転中心軸を結ぶ洗浄に、Z軸はCPU case 仮面より5mm位置にあるものとします。
バッテリー位置や構えによって重心位置は異なります。異なる点はモデルに反映してください。
### Beginners Mujoco model
BeginnersのMujoco modelを作成しました。

### PID制御で倒立伸子


### 深層強化学習で倒立伸子



### 強化学習の学習プロセスのむ確認
強化学習の学習プロセス（`ppo_1` フォルダに保存されているログ）を確認するには、**TensorBoard** を使用するのが最も一般的で確実な方法です。
Stable Baselines3（SB3）は、学習中の報酬（reward）やエピソードの長さ、損失関数（loss）などのデータを TensorBoard 形式で書き出します。
以下の手順で表示してください。

#### 1. TensorBoardの起動
ターミナル（またはコマンドプロンプト）を開き、Pythonスクリプトを実行しているディレクトリで以下のコマンドを入力します。
```bash
tensorboard kxr_balance_tb/PPO_1
```
※ `PPO_1` の親ディレクトリにいる場合は、上記コマンドでその中の全てのログを読み込みます。

ライブラリがインストールされているか確認
TensorBoard自体がPython環境に入っているか確認し、入っていなければインストールします。
```bash
pip install tensorboard
```
#### 2. ブラウザでの確認
コマンドを実行すると、以下のようなメッセージが表示されます。
`TensorBoard 2.x.x at http://localhost:6006/ (Press CTRL+C to quit)`

ブラウザ（ChromeやEdgeなど）を開き、アドレスバーに以下を入力してください。
**`http://localhost:6006/`**

---

#### TensorBoardでチェックすべき主な項目
表示されたグラフの中で、今回の倒立振子の学習において特に重要な指標は以下の通りです。

* **`rollout/ep_rew_mean` (平均報酬):**
    * **最重要指標です。** 学習が進むにつれて右肩上がりに数値が増えていれば、AIは「より長く立つ」「より垂直を保つ」方法を学んでいる証拠です。
* **`rollout/ep_len_mean` (平均エピソード長):**
    * エピソードが終了（転倒）するまでのステップ数です。これが最大値（設定したタイムリミット）に張り付くようになれば、安定して立ち続けられていることを意味します。
