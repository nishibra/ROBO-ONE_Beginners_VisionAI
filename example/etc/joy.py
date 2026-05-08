import pygame
import time
import serial
from krs_driver_rp5 import * 
#servo id
id_r=1
id_l=2
id_pan=3
id_tilt=4
#
ct=7500
ct_pan=6128
ct_tilt=7500
#
krs=KRSdriver()
#
def arm(pan,tilt):
    krs.set_position_ret(id_pan,ct_pan+pan)
    krs.set_position_ret(id_tilt,ct_tilt-tilt)
#
def drive(r_sp,l_sp):
    krs.set_position_ret(2,ct-l_sp)
    krs.set_position_ret(1,ct+r_sp)
#
def free_all():
    krs.read_position_set_free(1)
    krs.read_position_set_free(2)
    krs.read_position_set_free(3)
    krs.read_position_set_free(4)  
#
def main():
	# Pygameの初期化（コントローラー用）
    pygame.init()
    pygame.joystick.init()
    while pygame.joystick.get_count() == 0:
        pygame.event.pump() # イベントキューを更新
        time.sleep(0.1)     # CPU負荷を抑えるための待機
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Using: {joystick.get_name()}")
    #
    try:
        while(True) :
            pygame.event.pump()
            bu=joystick.get_button(0) # A
            bu2=joystick.get_button(1)# B
            bu3=joystick.get_button(3)# Y
            bu4=joystick.get_button(4)# Y
            bu6=joystick.get_button(6)# L1
            bu8=joystick.get_button(8)# L1
            if bu!=0: 
                drive(0,0)
            elif bu2!=0:
                free_all()
            elif bu6!=0:
                arm(int(5000*joystick.get_axis(2)),2800)
            elif bu8!=0:
                arm(int(5000*joystick.get_axis(2)),-3800)                
            else:
                fr=int(-300*joystick.get_axis(1))
                rf=int(100*joystick.get_axis(0))
                arm(int(5000*joystick.get_axis(2)),int(-5000*joystick.get_axis(3)))
                drive(fr-rf,fr+rf)
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\n終了します")
        pygame.quit()
        free_all()
#
if __name__ == "__main__":
    main()
