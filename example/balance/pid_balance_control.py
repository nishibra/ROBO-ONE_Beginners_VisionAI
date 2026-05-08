import mujoco
import mujoco.viewer
import numpy as np
import time
import random

# モデルの読み込み
model = mujoco.MjModel.from_xml_path('2wheel_balance_KRS3304R2.xml')
data = mujoco.MjData(model)

# --- PIDパラメータの設定 ---
# 車体の傾き(Pitch)に対するゲイン
kp = 60.0   # 比例ゲイン：傾きに比例して速度を出す
ki = 90.0    # 積分ゲイン：定常的な傾きを解消する
kd = 0.5    # 微分ゲイン：振れを抑える（ダンピング）

class SelfBalance():
    def __init__(self):
        # 制御変数の初期化
        self.integral = 0
        self.last_error = 0
        self.target_pitch = 0.035 # 目標角度調整（垂直）

    def get_pitch_angle(self,data):
        # base_linkのクォータニオンからピッチ角(ラジアン)を計算
        quat = data.body('base_link').xquat
        # クォータニオンからピッチ角への変換（簡易計算）
        #    sin(pitch) = 2*(qw*qy - qz*qx)
        sinp = 2 * (quat[0] * quat[2] - quat[3] * quat[1])
        return np.arcsin(np.clip(sinp+random.uniform(-0.01, 0.01), -1, 1))
    
    def servo_ctrl(self,output):
        data.ctrl[0] = -output*14.5  # right_motor
        data.ctrl[1] = -output*14.5  # left_motor
        # アームを固定位置に保持 (position control)
        data.ctrl[2] = 0.0   # roll_motor
        data.ctrl[3] = -0.55  # pitch_motor
        
# シミュレーションとレンダリングの開始
    def run_simu(self):
      with mujoco.viewer.launch_passive(model, data) as viewer:
        start_time = time.time()

        while viewer.is_running():
            step_start = time.time()

        # 1. 現在の傾きを取得
            current_pitch = self.get_pitch_angle(data)
            pitch_ang=current_pitch*180/3.14
            error = self.target_pitch - current_pitch
           # print(pitch_ang,current_pitch,error)

        # 2. PID計算
            dt = model.opt.timestep
            self.integral += error * dt
            derivative = (error - self.last_error) / dt
        
          # 制御入力 (Velocity Control)
          # 傾いている方向に車輪を回転させる
            output = (kp * error) + (ki * self.integral) + (kd * derivative)
            print(output)   
        # 3. アクチュエータに指令値を適用
          # XML内の velocity actuator (right_motor, left_motor) に入力
            self.servo_ctrl(output)
            self.last_error = error

        # シミュレーションを進める
            mujoco.mj_step(model, data)

        # 同期
            viewer.sync()
        
        # リアルタイム制御のための待機
            time_until_next_step = dt - (time.time() - step_start)
            if time_until_next_step > 0:
                time.sleep(time_until_next_step)

#------------------------
if __name__ == '__main__':
    print('Start Mujoco Test')
    sb=SelfBalance()
    sb.run_simu()
