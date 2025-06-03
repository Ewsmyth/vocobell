# VocoBell
#### Utilizing a Raspberry Pi Zero, a Waveshare PoE Hat and a DAC we can make the physical build of this tool.

## Install Docker for Raspberry Pi Zero
```
sudo apt update && sudo apt upgrade -y
```

```
sudo apt install -y ca-certificates curl gnupg lsb-release
```

```
sudo mkdir -p /etc/apt/keyrings
```

```
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

```
echo \
  "deb [arch=armhf signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

```
sudo apt update
```

```
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
## Install Portainer
```
sudo docker volume create portainer_data
```

```
sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
```

```
https://<serverip>:9443
```
## Install VocoBell
```sudo docker run -d -p 5665:5665 --restart=always ghcr.io/ewsmyth/vocobell:latest