import subprocess
import time

class Get_Volt:
    def __init__(self):
        print("start")
        self.status_int=0
    def get_V_status(self):	
        # コマンド実行
        result = subprocess.check_output(['vcgencmd', 'get_throttled']).decode('utf-8')
        # 出力例: throttled=0x50000
        # ビット0: 現在アンダーボルテージが発生しているか
        # ビット16: 起動後に一度でもアンダーボルテージが発生したか
        status_hex = result.split('=')[1].strip()
        self.status_int = int(status_hex, 16)
        return self.status_int
     
    def get_status(self):
        #print(self.get_V_status())
        if self.status_int & 0x1:
            print("現在、電圧が低下しています！")
        if self.status_int & 0x10000:
            print("過去に電圧低下が発生しました。")
        if self.status_int == 0:
            print("電源供給は安定しています。")
    def get_status_nd(self,flag):
        if flag!=0:
            print(self.get_V_status())
        if self.status_int & 0x1:
            print("現在、電圧が低下しています！")
        if self.status_int & 0x10000:
            print("過去に電圧低下が発生しました。")

# main
if __name__ == '__main__':
    gvolt = Get_Volt()
    while(1):
        gvolt.get_status()
        time.sleep(30)
