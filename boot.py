import network
import webrepl

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
sta_if.active(True)
if not sta_if.isconnected():
 print ("Connecting to network")
 sta_if.connect('SSID', 'PASSWORD')
 while not sta_if.isconnected():
  pass
 print("Connected:", sta_if.ifconfig())
 ap_if.active(False)
 webrepl.start()
