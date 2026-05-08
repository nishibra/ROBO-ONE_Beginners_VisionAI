#!/usr/bin/env python
# Beginners KRS-servo Joy MuJoCo program
# 2026.5.1
# by T.Nishimura of AiRRC
#--------------------------------
import mujoco
import mujoco.viewer
import numpy as np
import serial
import math
import time
from stable_baselines3 import PPO
from krs_driver_rp5 import * 
from bno055 import *
import pygame
#---------------
#set servo para
id_r=1
id_l=2
id_pan=3
id_tilt=4
#
ct=7500
ct_pan=6078
ct_tilt=7500
max_tilt=9600
min_tilt=5870
last_time = time.time()
tilt_p_pos=0
pan_p_pos=0
#
krs=KRSdriver()
#----------------
bno = BNO055()
if bno.begin() is not True:
	print("Error initializing BNO055")
	exit()
time.sleep(1)
bno.setExternalCrystalUse(True)
# ---------------
def free_all():
    for i in range(4):
        krs.read_position_set_free(i+1)
#----------------------------------------
def main():
    global last_time,tilt_p_pos,pan_p_pos
    free_all()
    # モデルのロード
    model_path = "robot4_getup1.zip"
    try:
        model = PPO.load(model_path)
        print(f"Loaded: {model_path}")
    except:
        print("モデルファイルが見つかりません。")
        return    
  # Pygameの初期化（コントローラー用）
    pygame.init()
    pygame.joystick.init()
    free_all()
    while pygame.joystick.get_count() == 0:
        pygame.event.pump() # イベントキューを更新
        time.sleep(0.1)     # CPU負荷を抑えるための待機
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Using: {joystick.get_name()}")

   # MuJoCoの準備
    model_mj = mujoco.MjModel.from_xml_path('2wheel_im_krs.xml')
    data_mj = mujoco.MjData(model_mj)
    
   # IDのキャッシュ (Observation作成用)
    base_id = mujoco.mj_name2id(model_mj, mujoco.mjtObj.mjOBJ_BODY, "base_link")

    def get_obs():
        """学習時と完全に同じObservation(21次元)を作成"""
        qpos = data_mj.qpos.flat.copy()
        qvel = data_mj.qvel.flat.copy()
        return np.concatenate([qpos, qvel]).astype(np.float32)
    def side_d():
        # 状態: qpos(11) + qvel(10) = 21
        qpos = data_mj.qpos.flat.copy()
        qvel = data_mj.qvel.flat.copy()
        data_mj.qpos[3:7] =[ -0.707, 0 ,0.707, 0]
        return np.concatenate([qpos, qvel]).astype(np.float32)
  #-----------------------------------
    def get_real_obs():
        global last_time,tilt_p_pos,pan_p_pos
        """学習時と完全に同じObservation(21次元)を作成"""
      # 状態: qpos(11) + qvel(10) = 21
        qpos = data_mj.qpos.flat.copy()
        qvel = data_mj.qvel.flat.copy()
      # 直立時に 1.0, 転倒時に 0.0重力ベクトルのZ成分を使用
      #  gravity = bno.getVector(BNO055.VECTOR_GRAVITY) # g(x,y,z)
      #  upright = gravity[2] / 9.8 
      #  side_tilt =  gravity[1] / 9.8
      #  front_tilt =  gravity[0] / 9.8
      #print(upright,side_tilt,front_tilt)
      # -----------------
      # positionq  pos(11)
        pan_pos=(krs.read_position(3)-ct_pan-1000)/3500
        if pan_pos>1.0:
            pan_pos=1.0
        if pan_pos<-1.0:
            pan_pos=-1.0
        #print(pan_pos)
        tilt_pos=(krs.read_position(4)-min_tilt)*2.0/(max_tilt-min_tilt)-1.0 
        if tilt_pos>1.0:
            tilt_pos=1.0
        if tilt_pos<-1.0:
            tilt_pos=-1.0
        #print(tilt_pos)
      # ------------
      # velocity
        now = time.time()
        dt = now-last_time
        tilt_vel=(tilt_pos-tilt_p_pos)/dt
        pan_vel=(pan_pos-pan_p_pos)/dt
        tilt_p_pos=tilt_pos
        pan_p_pos=pan_pos
        if dt <= 0:
            dt=0.1
        last_time = now
    ## 状態: qpos(11) + qvel(10) + upright(1) + side_tilt(1) = 23
     #
     ## qpos には、具体的に以下のような順番で数字が並んでいます：
     # インデックス意味
      # 0, 1, 2 本体の位置 (x, y, z)
        qpos[0]=0
        qpos[1]=0
        qpos[2]=0
      # 3, 4, 5, 6 本体の向き（クォータニオン）
        quat=bno.getQuat()
        qpos[3]=quat[0]
        qpos[4]=quat[1]
        qpos[5]=quat[2]
        qpos[6]=quat[3]
      # 7 右車輪の回転角
        qpos[7]=0
      # 8 左車輪の回転角
        qpos[8]=0
      # 9 アームのRoll角
        qpos[9]=pan_pos
      #10 アームのPitch角
        qpos[10]=-tilt_pos
    # qvel (対応する qpos よりも1つ要素が少なくなります)
          #（向きがクォータニオンではなく3軸の回転速度になるため）
      # 0, 1, 2 本体の移動速度 (vx, vy, vz)m/s
        qvel[0]=0
        qvel[1]=0
        qvel[2]=0
      # 3, 4, 5 本体の回転速度 (ロール, ピッチ, ヨー)rad/s
        qvel[3]=0
        qvel[4]=0
        qvel[5]=0    
      # 6 右車輪の回転速度rad/s
        qvel[6]=0   
      # 7 左車輪の回転速度rad/s
        qvel[7]=0   
      # 8 アームのRoll回転速度rad/s
        qvel[8]=pan_vel  
      # 9 アームのPitch回転速度rad/s
        qvel[9]=tilt_vel
        #return np.concatenate([qpos, qvel, [upright], [side_tilt]]).astype(np.float32)
        return np.concatenate([qpos, qvel]).astype(np.float32)
    # 鑑賞ループ
    with mujoco.viewer.launch_passive(model_mj, data_mj) as viewer:
        while viewer.is_running():
            step_start = time.time()
          # Joy stick
            pygame.event.pump()
            fr=joystick.get_axis(1)
            rl=joystick.get_axis(0)
            pan=joystick.get_axis(2)
            tilt=joystick.get_axis(3)
            bu=joystick.get_button(0) # A
            bu2=joystick.get_button(1)# B
            bu3=joystick.get_button(3)# X
            bu4=joystick.get_button(4)# Y
            bu6=joystick.get_button(6)# L1
            bu7=joystick.get_button(7)# R1
            bu8=joystick.get_button(8)# L2
            bu9=joystick.get_button(9)# R2
            bu10=joystick.get_button(10)# -
            #print(joystick.get_button(10))
            if bu!=0: #A
            # Mujoco obs
                obs = get_obs()
                action, _ = model.predict(obs, deterministic=True)
                data_mj.ctrl[:] = [action[0]*7.8,action[1]*7.8,action[2]*3.14,action[3]*3.14]
            elif bu2!=0:#B
            # get obserbation data
                obs = get_real_obs()
                action, _ = model.predict(obs, deterministic=True)
              # 実機仕様のスケーリング適用
                krs.set_position_ret(1,int(350*action[0]+ct))
                krs.set_position_ret(2,int(-350*action[1]+ct))
                krs.set_position_ret(3,int(-3500*action[2]*1.57+ct_pan))
                krs.set_position_ret(4,int(-3500*action[3]*1.57+ct_tilt))
            elif bu3!=0:#Y
              # MuJoCoに適用
                obs = get_obs()
              # get quatanion
                quat=bno.getQuat()
              # set data
                data_mj.qpos[3:7] =quat
                data_mj.ctrl[:] = [action[0]*7.8,action[1]*7.8,action[2]*3.14,action[3]*3.14]
            elif bu8!=0: #L2
                obs = get_real_obs()
                print(obs)
            # set action data from joy stick
                action=[-fr-rl,-fr+rl,-pan,tilt]
                #print(fr,rl,pan,tilt)
                data_mj.ctrl[:] = [action[0]*7.8,action[1]*7.8,action[2]*3.14,action[3]*3.14]
              # 実機仕様のスケーリング適用
                krs.set_position_ret(1,int(350*action[0]+ct))
                krs.set_position_ret(2,int(-350*action[1]+ct))
                krs.set_position_ret(3,int(-3500*action[2]*1.57+ct_pan))
                krs.set_position_ret(4,int(-3500*action[3]*1.57+ct_tilt))
            elif bu6!=0: #L1
                free_all()
            elif bu7!=0: #R1
                side_d()
            else:
                obs = get_obs()
              # set action data from joy stick
                action=[-fr-rl,-fr+rl,-pan,tilt]
                #print(fr,rl,pan,tilt)
                #
                data_mj.ctrl[:] = [action[0]*7.8,action[1]*7.8,action[2]*3.14,action[3]*3.14]
        # 
         # 物理シミュレーション
            for _ in range(10):
                mujoco.mj_step(model_mj, data_mj)
            viewer.sync()
          # リアルタイム同期
            elapsed = time.time() - step_start
            if elapsed < model_mj.opt.timestep * 10:
                time.sleep(model_mj.opt.timestep * 10 - elapsed)
#
if __name__ == "__main__":
    main()
    free_all()
