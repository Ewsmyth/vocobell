# 🔔 VocoBell
**A smart chime system powered by Docker, Raspberry Pi Zero, and Unifi webhooks.**


## 🧠 How It Works

VocoBell runs a Flask web server inside on your Raspberry Pi Zero.  
Utilizing the Unifi Alarm Manager you can set alarms to trigger custom webhooks that communicate with Pi.   
The Pi plays a custom audio file that you get to create.

Basic flow:

1. Event is triggered in Unifi Protect
2. Unifi sends webhook to `http://<pi-ip>:5665/ring`.
3. VocoBell receives the request and plays the sound.

---

## 🔄 Setting Up Webhooks in Unifi Protect

1. Open the Unifi Protect.
2. Go to **Alarm Manager** → **Create Alarm** → **Action** → **Webhook** → **Custom Webhook**.
3. Paste the Webhook from Vocobell into the **Delivery URL** input.
    - **Example URL:** `http://<your-pi-ip>:5665/ring`
4. Save and test — your chime should play!


> **Hardware Setup:**  
> Raspberry Pi Zero + Waveshare PoE HAT + Waveshare WM8960 Soundcard

---

## 📦 Features

- Custom chime playback on GPIO speaker
- Compatible with Unifi protect systems
- Runs headlessly on a Pi Zero
- Auto-restart
- Secure and lightweight

---

## ⚙️ Prerequisites

- Raspberry Pi Zero W/2
- Raspberry Pi OS (Lite with a version 5.x kernel recommended)
- Internet connection (via PoE or Wi-Fi)
- Speaker connected via DAC, Soundcard or other means.
- [Unifi Protect](https://ui.com).
### Install Waveshare WM8960 driver
- **First you'll need to set up your DAC or soundcard**
  - I used the Waveshare WM8960 Soundcard so that is what i'll demonstrate.
You'll need to clone the WM8960 GitHub driver then install (It is recommended to use a RASPIOS with a Kernel 5.x instead of 6.x).
```bash
git clone https://github.com/waveshare/WM8960-Audio-HAT
```
```bash
cd WM8960-Audio-HAT
```
```bash
sudo ./install.sh
```
```bash
sudo reboot
```
  - **Next,** edit your config.txt file
```bash
sudo nano /boot/config.txt
```
  - On newer OS you will find that this file tells you not to change it and instead edit /boot/firmware/config.txt, do that.
```
dtparam=audio=off
dtparam=i2s=on
dtoverlay=wm8960-soundcard,model="wm8960-soundcard",mclk-fs=256
```
```bash
sudo reboot
```
  - Confirm the sound card is still present and configured properly.
```bash
aplay -l
```
---
## 🔔 Install VocoBell
```bash
git clone https://github.com/Ewsmyth/vocobell
```
```bash
cd vocobell
```
```bash
bash install.sh
```
---
## Adding audio files
- Audio files should have the following features
  - Stereo (not mono)
  - 48kHz 
  - .wav
---

## 🐳 Install Docker (for Raspberry Pi Zero)
- The Docker image is still in development and is not stable at the moment so I would not set it up in Docker.

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
```bash
sudo usermod -aG docker admin
```
```bash
sudo reboot
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
