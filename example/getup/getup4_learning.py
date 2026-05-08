import gymnasium as gym
from gymnasium import spaces
import mujoco
import numpy as np
from stable_baselines3 import PPO
from gymnasium.wrappers import TimeLimit
from stable_baselines3.common.callbacks import BaseCallback
class RobotGetupEnv(gym.Env):
    def __init__(self):
        super(RobotGetupEnv, self).__init__()
        self.model = mujoco.MjModel.from_xml_path('2wheel_ai_krs.xml')
        self.data = mujoco.MjData(self.model)
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(4,), dtype=np.float32)
        # 状態: qpos(11) + qvel(10) + upright(1)  = 22
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(21,), dtype=np.float32)
        self.base_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, "base_link")

    def _get_obs(self):
        qpos = self.data.qpos.flat.copy()
        qvel = self.data.qvel.flat.copy()
        return np.concatenate([qpos, qvel]).astype(np.float32)

    def step(self, action):
      # 物理量適用
        self.data.ctrl[0] = action[0] * 10  # 右輪
        self.data.ctrl[1] = action[1] * 10  # 左輪
        self.data.ctrl[2] = action[2] * 3.14  # pan
        self.data.ctrl[3] = action[3] * 3.14  # tilt

        for _ in range(10):
            mujoco.mj_step(self.model, self.data)

        obs = self._get_obs()
        
        # --- 報酬設計 ---
        height = self.data.xpos[self.base_id][2]
        upright = self.data.xmat[self.base_id][8]     # Z軸の垂直度
        z_vel = self.data.qvel[5] # Z軸角速度

        reward = 0
       # upright
        if upright > 0.95:
            reward +=4.0
       #
        reward +=upright*0.8
       # rotation
        if upright < 0.5:
            reward += abs(z_vel) * 28.0
       # 終了判定
        terminated = bool(upright > 0.995 and height > 0.18)
        truncated = False
        print(reward)
        return obs, reward, terminated, truncated, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        mujoco.mj_resetData(self.model, self.data)
        # 完全ランダムな姿勢で開始（横倒しも含む）
        random_quat = np.random.uniform(-1, 1, size=4)
        self.data.qpos[3:7] = random_quat / np.linalg.norm(random_quat)
        self.data.qpos[2] = 0.01 #0.01 Zaxis
        mujoco.mj_forward(self.model, self.data)
        return self._get_obs(), {}
   
if __name__ == "__main__":
    env = RobotGetupEnv()
    env = TimeLimit(env, max_episode_steps=2000)
    model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.001)
    model.learn(total_timesteps=180000)
    model.save("robot4_getup1")
