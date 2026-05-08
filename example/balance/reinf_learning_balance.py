import gymnasium as gym
from gymnasium import spaces
from stable_baselines3.common.monitor import Monitor
import mujoco
import mujoco.viewer
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
import time

class KXRConverter:
    """KRS-3304R2のICSプロトコル準拠の物理量変換"""
    RVolt=7.4/7.4 #高電圧化
    MAX_VEL_RAD_S = 9.52*RVolt  # 0.11s/60deg
    RAD_RANGE = np.deg2rad(130.0)

    @classmethod
    def action_to_vel(cls, action):
        return action * cls.MAX_VEL_RAD_S

    @classmethod
    def action_to_pos(cls, action):
        return action * cls.RAD_RANGE

class KXRBalanceEnv(gym.Env):
    def __init__(self, is_eval=False):
        super().__init__()
        self.model = mujoco.MjModel.from_xml_path('2wheel_balance_KRS3304R2.xml')
        self.data = mujoco.MjData(self.model)
        self.is_eval = is_eval
        self.target_pitch = 0.0  # 静止バランス角
        
        # Action: [右輪速度, 左輪速度, アームピッチ]
        self.action_space = spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32)
        # Obs: [sin(誤差), cos(誤差), 角速度, 車輪速度, アーム角度]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(5,), dtype=np.float32)
        self.viewer = None

    def _get_pitch(self):#ピッチ角を求める
        quat = self.data.body('base_link').xquat
        sinp = 2 * (quat[0] * quat[2] - quat[3] * quat[1])
        return np.arcsin(np.clip(sinp, -1, 1))

    def _get_obs(self):#観測データ
        pitch = self._get_pitch()
        error = pitch - self.target_pitch
        return np.array([
            np.sin(error), np.cos(error), 
            self.data.qvel[2],
            self.data.joint('drive_right').qvel[0],
            self.data.joint('drive_pitch').qpos[0]
        ], dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        mujoco.mj_resetData(self.model, self.data)

        # 【ポイント】直立状態付近からスタート
        # バランス角に少しだけランダムな揺らぎを加える
        initial_error = np.random.uniform(-0.1, 0.1) 
        
        # クォータニオンで姿勢を設定
        quat = np.zeros(4)
        mujoco.mju_euler2Quat(quat, [0, self.target_pitch + initial_error, 0], 'xyz')
        self.data.qpos[3:7] = quat
        self.data.qpos[2] = 0.1 # 地面より少し上

        mujoco.mj_forward(self.model, self.data)
        return self._get_obs(), {}

    def step(self, action):
        # 物理限界の適用
        self.data.ctrl[0] =1000*KXRConverter.action_to_vel(action[0])
        self.data.ctrl[1] =1000*KXRConverter.action_to_vel(action[1])
        self.data.ctrl[3] =1000*KXRConverter.action_to_pos(action[2]) # アーム
        
        mujoco.mj_step(self.model, self.data)
        
        if self.is_eval:
            if self.viewer is None:
                self.viewer = mujoco.viewer.launch_passive(self.model, self.data)
            self.viewer.sync()
            time.sleep(0.005)

        obs = self._get_obs()
        pitch = self._get_pitch()
        
        # --- 報酬と終了判定 ---
        error = np.abs(pitch - self.target_pitch)
        
        # 1. 生存報酬: 立っているだけでプラス
        reward = 1.0 
        # 2. 姿勢報酬: 垂直に近いほど高得点
        reward += np.exp(-20 * error**2)
        
        # 3. 終了判定 (Fall detection)
        # 45度(約0.8rad)以上傾いたら「転倒」とみなしてエピソード終了
        terminated = error > 0.5
        
        return obs, reward, terminated, self.data.time > 8.0, {}

if __name__ == "__main__":
    train_env = Monitor(KXRBalanceEnv(is_eval=False))
    eval_env = Monitor(KXRBalanceEnv(is_eval=True))

    eval_callback = EvalCallback(eval_env, eval_freq=10000, deterministic=True)

    # 倒立振子は比較的簡単なタスクなので、学習率は標準的でOK
    model = PPO("MlpPolicy", train_env, verbose=1, tensorboard_log="./kxr_balance_tb/")

    print("倒立維持の学習を開始します...")
    model.learn(total_timesteps=300000, callback=eval_callback)
    model.save("t2_kxrR2_balance_model")
