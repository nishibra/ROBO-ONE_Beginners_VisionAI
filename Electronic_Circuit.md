# Electronic_Circuit
## 概要
- cpu: Raspi5 16M csi
- Hat:電源 serial i2c fan rtc

### Raspi5
![VisionAI](pics_elec/raspi5.png)

https://www.amazon.co.jp/dp/B0CPDJ8FNK?ref=ppx_yo2ov_dt_b_fed_asin_title

### Hat
#### BTE100B DXHAT
![VisionAI](pics_elec/hat.png)

https://www.besttechnology.co.jp/modules/knowledge/?BTE100B%20DXHAT

#### HeatSink
https://www.amazon.co.jp/dp/B0F8V6TK9M?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1

#### 電源SW
![VisionAI](pics_elec/bno055.png)

### CSI camera
![VisionAI](pics_elec/raspi_camera.jpg)

#### camera: csi

#### Flexible cable
https://www.amazon.co.jp/dp/B0DNFP5QJR?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1

### 入出力
#### bno055
![VisionAI](pics_elec/bno055.png)

#### push sw
![VisionAI](pics_elec/bno055.png)

https://www.amazon.co.jp/dp/B0D4PX1V4Q?ref=ppx_yo2ov_dt_b_fed_asin_title

#### LED

#### ADC

### battery

:1000mAH

## servo:KRS3304-R2


---
#### config.txtに追記する情報
```
[all]
dtoverlay=gpio-shutdown,gpio_pin=17
dtoverlay=gpio-poweroff,gpiopin=4,active_low=1
```
ubuntuをGUIで起動している場合は、プッシュスイッチを押下するとログアウトのプロンプトが表示され、タイムアウトするかダイアログのpower offを選択するまでシャットダウンが行われません。プッシュスイッチ操作によってシンプルにシャットダウン処理を行わせるには、GNOMEの設定を変更する必要があります。なおログインしていない状態ではこの設定は効果がありません。

```
gsettings set org.gnome.SessionManager logout-prompt false
```

#### config.txtに追記する情報
```
[all]
dtoverlay=gpio-fan,gpiopin=19,temp=50000
temp=50000は50℃で冷却ファンをONする意味で、摂氏度の1000倍の値を指定
設定温度を10℃下回るとファンはOFFする
```

### config.txtに追記する情報

```
[pi5]
dtparam=rtc=off
[all]
dtparam=i2c_arm=on
dtoverlay=i2c-rtc,ds3231
```

#### config.txtに追記する情報
```
[pi3]
init_uart_clock=64000000
dtoverlay=uart0=on
dtoverlay=pi3-miniuart-bt
 
[pi4]
init_uart_clock=64000000
#UART1を活性化
dtoverlay=uart1,txd1_pin=14,rxd1_pin=15
#UART2を活性化
dtoverlay=uart2,txd2_pin=0,rxd2_pin=1
#UART4を活性化
dtoverlay=uart4,txd4_pin=8,rxd4_pin=9
使用するポートのみを活性化する事を推奨。Linux上でのデバイス名は概ねttyAMAのプレフィクスで始まる。
またRaspberry Pi 3/Zeroの場合はcmdline.txtに記述されている「console=serial0,115200」を削除する事
```
