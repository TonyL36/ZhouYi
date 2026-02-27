# 全新部署指南 (Fix for Timeout)

鉴于您在服务器构建时遇到 Docker Hub 超时问题，以及本地没有 Maven 环境，我们采用 **“本地准备 + 镜像加速”** 的混合部署策略。

## 方案核心
1.  **本地**：不需要安装 Maven，但需要将代码上传。
2.  **服务器**：配置 **Docker 镜像加速器**（这是解决超时的关键），然后让服务器去构建。

## 步骤 1: 清理旧环境 (可选)
如果之前的尝试导致服务器上留下了很多垃圾文件，可以先登录服务器清理一下：
```bash
rm -rf /root/ZhouYi
docker system prune -f
```

## 步骤 2: 配置服务器镜像加速 (关键!)
**请登录您的阿里云服务器**，执行以下命令（直接复制粘贴）：

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://docker.1panel.live",
    "https://hub.rat.dev"
  ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```
*这一步能解决 `context deadline exceeded` 错误。*

## 步骤 3: 重新上传代码
在您的本地电脑执行：
```bash
scp -r E:\GitProjects\MyProject\ZhouYi root@47.109.193.180:/root/
```

## 步骤 4: 启动部署
登录服务器，进入目录：
```bash
cd /root/ZhouYi
docker-compose up -d --build
```
此时，由于配置了加速器，拉取 `maven` 和 `nginx` 镜像应该会很快成功。

## 步骤 5: 验证
访问：`http://47.109.193.180:6400/book/ZhouYi`

---

## 备选方案：如果还是超时
如果配置了加速器依然拉不动（近期国内 Docker 镜像源非常不稳定），我们需要修改 `backend/Dockerfile` 使用阿里云的 Maven 镜像源，或者使用离线包。

**修改 Maven 镜像源的方法 (在服务器上执行):**
创建 `backend/settings.xml` 文件，填入阿里云镜像配置，然后在 Dockerfile 中通过 `-s settings.xml` 使用它。
但通常配置 Docker Daemon 加速器（步骤 2）就足够了。
