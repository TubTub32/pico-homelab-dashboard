from machine import I2C, Pin
from i2c_lcd import I2cLcd
import network
import urequests
import time

# ===========================
# === CONFIGURATION BLOCK ===
# ===========================

# Wi-Fi credentials
SSID = "YOUR_WIFI_NAME"
PASSWORD = "YOUR_WIFI_PASSWORD"

# Plex settings
PLEX_IP = "192.168.x.x"
PLEX_TOKEN = "YOUR_PLEX_TOKEN"

# Sonarr settings
SONARR_IP = "192.168.x.x"
SONARR_KEY = "YOUR_SONARR_API_KEY"

# Radarr settings
RADARR_IP = "192.168.x.x"
RADARR_KEY = "YOUR_RADARR_API_KEY"

# SABnzbd settings
SABNZBD_IP = "192.168.x.x"
SABNZBD_KEY = "YOUR_SABNZBD_API_KEY"
SABNZBD_PORT = 8080  # Adjust if different

# ===========================
# === HARDWARE SETUP ========
# ===========================

# I2C LCD (1602) setup
I2C_ADDR = 0x27
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# Button input setup (active low)
button = Pin(15, Pin.IN, Pin.PULL_UP)

# ===========================
# === HELPER FUNCTIONS ======
# ===========================

def write_line(row, text):
    """Write text to a specific row on the LCD, padding/truncating to 16 chars."""
    lcd.move_to(0, row)
    lcd.putstr((text + " " * 16)[:16])

# ===========================
# === SCREEN FUNCTIONS ======
# ===========================

def show_plex():
    """Display number of active Plex streams."""
    lcd.clear()
    try:
        url = f"http://{PLEX_IP}:32400/status/sessions?X-Plex-Token={PLEX_TOKEN}"
        r = urequests.get(url)
        content = r.text
        r.close()
        idx = content.find('size="')
        count = int(content[idx+6:content.find('"', idx+6)]) if idx != -1 else 0
        write_line(0, "Plex Streams:")
        write_line(1, f"{count} Active")
    except:
        write_line(0, "Plex check failed")
        write_line(1, "Err :(")

def show_sonarr():
    """Display current Sonarr queue size."""
    lcd.clear()
    try:
        url = f"http://{SONARR_IP}:8989/api/v3/queue?apikey={SONARR_KEY}"
        r = urequests.get(url)
        data = r.json()
        r.close()
        count = len(data.get("records", []))
        write_line(0, "Sonarr Queue:")
        write_line(1, f"{count} Pending")
    except:
        write_line(0, "Sonarr Error")
        write_line(1, "")

def show_radarr():
    """Display current Radarr queue size."""
    lcd.clear()
    try:
        url = f"http://{RADARR_IP}:7878/api/v3/queue?apikey={RADARR_KEY}"
        r = urequests.get(url)
        data = r.json()
        r.close()
        items = data.get("records", data)
        count = len(items)
        write_line(0, "Radarr Queue:")
        write_line(1, f"{count} Pending")
    except:
        write_line(0, "Radarr Error")
        write_line(1, "")

def show_sabnzbd():
    """Display SABnzbd queue size and download speed."""
    lcd.clear()
    try:
        url = f"http://{SABNZBD_IP}:{SABNZBD_PORT}/api?mode=queue&output=json&apikey={SABNZBD_KEY}"
        r = urequests.get(url)
        data = r.json()
        r.close()
        queue_size = len(data["queue"]["slots"])
        speed = data["queue"]["speed"]
        write_line(0, f"SABnzbd Q: {queue_size}")
        write_line(1, f"Speed: {speed}")
    except:
        write_line(0, "SABnzbd Error")
        write_line(1, "")

def show_storage():
    """Display total free space reported by Sonarr root folders."""
    lcd.clear()
    try:
        url = f"http://{SONARR_IP}:8989/api/v3/rootfolder?apikey={SONARR_KEY}"
        r = urequests.get(url)
        folders = r.json()
        r.close()
        total_free = sum(f.get("freeSpace", 0) for f in folders)
        free_gb = total_free // (1024 ** 3)
        write_line(0, "Free Storage:")
        write_line(1, f"{free_gb} GB")
    except:
        write_line(0, "Storage Error")
        write_line(1, "")

# ===========================
# === SCREEN LIST ===========
# ===========================

screens = [
    show_plex,
    show_sonarr,
    show_radarr,
    show_sabnzbd,
    show_storage,
]

# ===========================
# === STARTUP & LOOP ========
# ===========================

# Connect to Wi-Fi
lcd.clear()
write_line(0, "Connecting WiFi")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Wait for connection with timeout
timeout = 10
while not wlan.isconnected() and timeout > 0:
    write_line(1, f"{timeout}s...")
    time.sleep(1)
    timeout -= 1

# Start on first screen
screen = 0
last = 1
screens[screen]()

# Main loop: button cycles screens
while True:
    curr = button.value()
    if last == 1 and curr == 0:
        screen = (screen + 1) % len(screens)
        screens[screen]()
        time.sleep_ms(300)  # debounce
    last = curr
    time.sleep_ms(50)
