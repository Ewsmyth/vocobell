# 🔔 VocoBell
**A smart chime system powered by Docker, Raspberry Pi Zero, and Unifi webhooks.**


## 🧠 How It Works

VocoBell runs a Flask web server inside a Docker container on your Raspberry Pi Zero.  
When a Unifi Protect doorbell is pressed, it sends a POST request to your Pi's `/ring` endpoint.  
The Pi plays a custom chime through a connected DAC and speaker.

Basic flow:

1. Doorbell is pressed.
2. Unifi sends webhook to `http://<pi-ip>:5665/ring`.
3. VocoBell receives the request and plays the sound.

## 🎵 Customizing the Chime

By default, VocoBell plays `chime.wav`.  
To override it with your own audio file, mount your WAV file into the container:

```bash
sudo docker run -d -p 5665:5665 \
  -v /home/pi/my-sound.wav:/app/chime.wav \
  --restart=always \
  ghcr.io/ewsmyth/vocobell:latest
```


---

#### 🌐 Improve Webhook Setup Section

Currently, it’s missing from your latest version. Re-add it for completeness:


## 🔄 Setting Up Webhooks in Unifi Protect

1. Open the Unifi Protect web UI.
2. Go to **Settings** → **Advanced** → **Webhooks**.
3. Add a new webhook with:
    - **Event Type:** Doorbell Ring
    - **URL:** `http://<your-pi-ip>:5665/ring`
4. Save and test — your chime should play!


> **Hardware Setup:**  
> Raspberry Pi Zero + Waveshare PoE HAT + I2S DAC  
> **Software:** Dockerized Flask app triggered via Unifi Protect webhooks

---

## 📦 Features

- Custom chime playback on GPIO speaker
- Compatible with Unifi doorbell systems
- Runs headlessly on a Pi Zero
- Auto-restart and containerized deployment
- Secure and lightweight

---

## ⚙️ Prerequisites

- Raspberry Pi Zero W/2
- Raspberry Pi OS (Lite recommended)
- Internet connection (via PoE or Wi-Fi)
- Speaker connected via DAC (e.g., I2S PCM5102)
- [Unifi Protect](https://ui.com) system with webhook support

---

## 🐳 Install Docker (for Raspberry Pi Zero)

```bash
sudo apt update && sudo apt upgrade -y
```
```bash
sudo apt install -y ca-certificates curl gnupg lsb-release
```
```bash
sudo mkdir -p /etc/apt/keyrings
```
```bash
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
```bash
echo "deb [arch=armhf signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
```bash
sudo apt update
```
```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
## Install Portainer
```bash
sudo docker volume create portainer_data
```
```bash
sudo docker run -d -p 8000:8000 -p 9443:9443 \
  --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```
#### Access Portainer
```
https://<serverip>:9443
```
## Install VocoBell
```
sudo docker run -d -p 5665:5665 --restart=always ghcr.io/ewsmyth/vocobell:latest
```

## 🧯 Troubleshooting

- 🔇 **No sound?**
  - Check wiring between DAC and speaker.
  - Confirm the `.wav` file is supported and not corrupted.

- 🔁 **Container not running?**
  - Run `docker ps -a` to see if it crashed.
  - Check logs with `docker logs <container_id>`.

- 🌐 **Webhook not working?**
  - Make sure your Pi IP is static or reserved via DHCP.
  - Use `curl http://<pi-ip>:5665/ring` to test manually.
