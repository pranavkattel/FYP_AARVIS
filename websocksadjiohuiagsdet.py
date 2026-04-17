import websocket
import json
import serial
import time

# ========================
# CONFIG
# ========================
WS_URL = "ws://192.168.137.82:8000/ws/communication/test/?user_id=2"

# CHANGE THIS PORT 👇
ARDUINO_PORT = "/dev/ttyACM0"   # Windows example
BAUD_RATE = 115200

# ========================
# SERIAL SETUP
# ========================
arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # wait for Arduino reset


# ========================
# SEND TO ARDUINO
# ========================
def send_to_arduino(cmd):
    print("➡️ Sending to Arduino:", cmd)
    arduino.write((cmd + "\n").encode())


# ========================
# WEBSOCKET HANDLERS
# ========================
def on_message(ws, message):
    print("Received WebSocket:", message)

    try:
        data = json.loads(message)

        if data.get("type") == "robot-control":

            direction = data.get("direction")
            action = data.get("action")

            # START MOVEMENT
            if action == "start":
                if direction == "F":
                    send_to_arduino("F")
                elif direction == "B":
                    send_to_arduino("B")
                elif direction == "L":
                    send_to_arduino("L")
                elif direction == "R":
                    send_to_arduino("R")

            # STOP MOVEMENT
            elif action == "stop":
                send_to_arduino("STOP")

    except Exception as e:
        print("Parse error:", e)


def on_open(ws):
    print("✅ WebSocket Connected")

    ws.send(json.dumps({
        "type": "client-hello",
        "user_id": 2
    }))


def on_close(ws, *args):
    print("❌ WebSocket Closed")


def on_error(ws, error):
    print("⚠️ Error:", error)


# ========================
# RUN CLIENT
# ========================
if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,
        on_error=on_error
    )

    ws.run_forever()