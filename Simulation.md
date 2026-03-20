# Simulation
環境
-Windows11

## Mujoco シミュレーション
- Mujoco model
- 画像処理と追従
- Yolo11
- 相手の認識　物体認識
- リングの認識　セグメンテーション
## Baseline　深層強化学習

## Yolo11 深層機械学習

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
