import mujoco
import mujoco.viewer
import numpy as np
import time
from stable_baselines3 import PPO
import cv2
#
def main():
    #モデルのロード 
    model_path ="robot4_getup1"  
    #model_path ="robot4_getup1_render"
    try:
        model = PPO.load(model_path)
        print(f"Loaded: {model_path}")
    except:
        print("モデルファイルが見つかりません。")
        return

    # 2. MuJoCoの準備
    model_mj = mujoco.MjModel.from_xml_path('2wheel_ai_krs.xml')
    data_mj = mujoco.MjData(model_mj)
    
    # IDのキャッシュ (Observation作成用)
    base_id = mujoco.mj_name2id(model_mj, mujoco.mjtObj.mjOBJ_BODY, "base_link")

    def get_obs():
        """学習時と完全に同じObservation(21次元)を作成"""
        qpos = data_mj.qpos.flat.copy()
        qvel = data_mj.qvel.flat.copy()
        return np.concatenate([qpos, qvel]).astype(np.float32)

    # 3. 鑑賞ループ
    with mujoco.viewer.launch_passive(model_mj, data_mj) as viewer:
        print("Ctrl + マウスドラッグで横倒しにしてみてください。")
        while viewer.is_running():
            step_start = time.time()

            # AIによる推論
            obs = get_obs()
            action, _ = model.predict(obs, deterministic=True)
            
            # 実機仕様のスケーリング適用
            data_mj.ctrl[0] = action[0] * 10  # 右輪
            data_mj.ctrl[1] = action[1] * 10  # 左輪
            data_mj.ctrl[2] = action[2] * 3.14 # pan
            data_mj.ctrl[3] = action[3] * 3.14 # tilt
            
            # 物理シミュレーション (学習時と同じフレームスキップ数)
            for _ in range(10):
                mujoco.mj_step(model_mj, data_mj)

            viewer.sync()

            # リアルタイム同期
            elapsed = time.time() - step_start
            if elapsed < model_mj.opt.timestep * 10:
                time.sleep(model_mj.opt.timestep * 10 - elapsed)

if __name__ == "__main__":
    main()
