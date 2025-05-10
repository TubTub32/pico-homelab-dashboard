# pico-homelab-dashboard
A tiny MicroPython-powered LCD dashboard for your homelab. Runs on a Pi Pico W and shows stats from Plex, Sonarr, Radarr, SABnzbd, and more—no server changes needed.
---

## Features

- Shows:
  - Plex: active stream count
  - Sonarr: queue size
  - Radarr: queue size
  - SABnzbd: queue + download speed
  - Storage: free space (from Sonarr root folders)
  - Single-button interface to switch screens
  - Wi-Fi enabled (connects once at startup)
  -  MicroPython, ~150 lines of code
  - Doesn’t require any changes on your server

---

## Hardware

- Raspberry Pi Pico W
- 1602 I²C LCD display
- Momentary push button (wired to GPIO 15)
- A few jumper wires
- Breadboard or hot glue depending on your vibe

---

## Setup

1. Flash your Pico W with MicroPython (if it isn’t already)
2. Have display drivers on pico (included mine if needed)
3. Copy `main.py` to the board (I used Thonny)
4. Open the file and edit your:
   - Wi-Fi SSID/password
   - IPs and API keys for your services
5. Save, reboot, and it should start cycling through screens

---

## Screens Included

- **Plex** – how many active streams
- **Sonarr** – current queue size
- **Radarr** – same, for movies
- **SABnzbd** – queue length + download speed
- **Free storage** – pulled from Sonarr’s root folder API

---

## Ideas for Expansion

- Add qBittorrent stats (login session required)
- Show Proxmox CPU/RAM or VM status


---

## License

MIT. Feel free to fork, modify, and improve. If you build your own version, tag me—I'd love to see it.
