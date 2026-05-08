import gymnasium as gym
import mujoco
import mujoco.viewer
import numpy as np
from stable_baselines3 import PPO
import time

# 学習時と同じ物理量変換クラス
class KXRConverter:
    RVolt=7.4/7.4 #高電圧化
    MAX_VEL_RAD_S = 9.52*RVolt
    RAD_RANGE = np.deg2rad(130.0)

    @classmethod
    def action_to_vel(cls, action):
        return action * cls.MAX_VEL_RAD_S

    @classmethod
    def action_to_pos(cls, action):
        return action * cls.RAD_RANGE

def run_inference(model_path):
    # 1. モデルとMuJoCo環境の準備
    model = mujoco.MjModel.from_xml_path('2wheel_balance_KRS3304R2.xml')
    data = mujoco.MjData(model)
    
    # 学習済みポリシーの読み込み
    rl_agent = PPO.load(model_path)
    
    target_pitch = 0.0# 静止バランス角

    # 2. 推論ループ
    with mujoco.viewer.launch_passive(model, data) as viewer:
        # 初期状態：少し傾けてスタート（復帰能力を確認するため）
        mujoco.mj_resetData(model, data)
        initial_error = 0.0  # 0.2ラジアン（約11度）あえて傾ける
        quat = np.zeros(4)
        mujoco.mju_euler2Quat(quat, [0, target_pitch + initial_error, 0], 'xyz')
        data.qpos[3:7] = quat
        data.qpos[2] = 0.05 #初期高さ
        #
        #data.qpos[0]: X座標（前後）
        #data.qpos[1]: Y座標（左右）
        #data.qpos[2]: Z座標（高さ)
        #qpos[3:7] : クォータニオン（回転・姿勢を表す4つの数値）
        #qpos[7] : 右車輪の回転角（drive_right）
        #qpos[8] : 左車輪の回転角（drive_left）
        #qpos[9] : アームの回転角（drive_roll）
        #qpos[10] : アームのピッチ角（drive_pitch） ※配列の順番はXMLに記述された順序に基づきます。
        #base_linkが空間をどう移動しているかを表します。
        #qvel[0:3]: 直進速度（X, Y, Z軸方向の m/s）
        #qvel[3:6]: 回転速度（X, Y, Z軸まわりの rad/s）
        #倒立振子において、qvel[5]（または軸の設定によってはqvel[4]や[3]）が「車体の倒れる速さ」として非常に重要な観測データになります。
        
        print("推論を開始します。ロボットがバランスを取る様子を確認してください。")
        
        while viewer.is_running():
            step_start = time.time()

            # --- A. 状態（Observation）の作成 ---
            # クォータニオンから現在のピッチ角を取得
            quat_current = data.body('base_link').xquat
            sinp = 2 * (quat_current[0] * quat_current[2] - quat_current[3] * quat_current[1])
            current_pitch = np.arcsin(np.clip(sinp, -1, 1))
            
            error = current_pitch - target_pitch
            
            # 学習時と同じ5つの観測値を入力
            obs = np.array([
                np.sin(error), 
                np.cos(error), 
                data.qvel[2],                             # 胴体角速度
                data.joint('drive_right').qvel[0],        # 右輪速度
                data.joint('drive_pitch').qpos[0]         # アーム角度
            ], dtype=np.float32)

            # --- B. モデルによる行動決定 ---
            action, _states = rl_agent.predict(obs, deterministic=True)
            print(obs[0])
            if obs[0]>0.5:
                data.qpos[2] = 0
            # --- C. 物理限界を考慮した適用 ---
            data.ctrl[0] = 1000*KXRConverter.action_to_vel(action[0])
            data.ctrl[1] = 1000*KXRConverter.action_to_vel(action[1])
            data.ctrl[3] = 1000*KXRConverter.action_to_pos(action[2])

            # シミュレーションを進める
            mujoco.mj_step(model, data)
            viewer.sync()
            time.sleep(0.002)
            # リアルタイム調整
            time_until_next_step = model.opt.timestep - (time.time() - step_start)
            if time_until_next_step > 0:
                time.sleep(time_until_next_step)

if __name__ == "__main__":
    # 保存したモデルのファイル名を指定してください
    MODEL_FILENAME = "t2_kxrR2_balance_model.zip"
    run_inference(MODEL_FILENAME)
