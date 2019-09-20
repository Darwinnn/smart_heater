import machine
import usocket as socket
import uasyncio as asyncio
import html2
import time

event = -1 

def init():
    global rel1
    global rel2
    global led
    global buzzer

    rel1 = machine.Pin(12, machine.Pin.OUT)
    rel1.value(0)
    rel2 = machine.Pin(16, machine.Pin.OUT)
    rel2.value(0)
    pin13 = machine.Pin(13, machine.Pin.OUT)
    buzzer = machine.PWM(pin13)
    led = machine.Pin(2, machine.Pin.OUT)
    led.value(1)


def beep(dur): 
    buzzer.freq(1000)
    buzzer.duty(100)
    time.sleep(dur)
    buzzer.duty(0)

def off():
    global state
    print("Turning off the relays:", time.time())
    rel1.off()
    rel2.off()
    beep(0.5)
    led.on()
    state = "Нагревательные элементы выключены"

def on():
    global state
    print("Turning on the relays:", time.time())
    rel1.on()
    rel2.on()
    beep(0.2)
    time.sleep(0.2)
    beep(0.2)
    led.off()
    state = "Нагревательные элементы включены"

async def heater():
    while True:
        if event == 1:
            print("event 1")
            on()
            await asyncio.sleep(180)
            off()
            await asyncio.sleep(900)
        if event == 2:
            print("event 2")
            on()
            await asyncio.sleep(240)
            off()
            await asyncio.sleep(900)
        if event == 3:
            print("Event 3")
            on()
            await asyncio.sleep(240)
            off()
            await asyncio.sleep(600)
        await asyncio.sleep_ms(1) 

async def serve_web():
    s = socket.socket()
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s.bind(addr)
    s.settimeout(0.5)
    s.listen(1)
    cur_mode = "Выключен"
    global state
    state = "Нагревательные елементы выключены"
    global event
    while True:
        await asyncio.sleep_ms(1)
        try:
            # got new connection
            conn, addr = s.accept()
            data = conn.recv(2048)
            print("Connected from:", addr)
            conn.write("HTTP/1.1 200 OK\r\n\r\n")
            conn.write(html2.handle_html(cur_mode, state))
            if "POST /off HTTP/1.1" in data:
                print("Turning off")
                cur_mode = "Выключен"
                event = 0
                off()
            if "POST /low HTTP/1.1" in data:
                print("Setting to low")
                cur_mode = "Минимум"
                event = 1
            if "POST /mid HTTP/1.1" in data:
                print("Setting to mid")
                cur_mode = "Среднее"
                event = 2
            if "POST /high HTTP/1.1" in data:
                print("Setting to high")
                cur_mode = "Максимум"
                event = 3
            conn.close()
        except:
            pass

def main():
    init()
    loop = asyncio.get_event_loop()
    loop.create_task(heater())
    loop.create_task(serve_web())
    loop.run_forever()


main()
