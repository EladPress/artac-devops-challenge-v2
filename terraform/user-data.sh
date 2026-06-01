#!/bin/bash
set -euxo pipefail

exec > /var/log/user-data.log 2>&1

echo "=== Installing Docker ==="
apt-get update -y
apt-get install -y ca-certificates curl gnupg

install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin

systemctl enable docker
systemctl start docker

echo "=== Pulling and running application ==="
docker pull ${docker_image}
docker run -d \
  --name sentiment-api \
  --restart unless-stopped \
  -p ${app_port}:${app_port} \
  ${docker_image}

echo "=== User data script completed ==="
