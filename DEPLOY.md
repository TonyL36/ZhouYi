# 部署指南 (Deployment Guide)

本项目前端基于 React (Vite)，后端基于 Spring Boot。
虽然在开发阶段前后端是分离的（分别运行在 6400 和 6401 端口），但在部署到云端时，您可以选择**合并部署**或**分离部署**。

## 选项一：分离部署 (推荐 - 符合生产环境标准)
这种方式使用 Nginx 作为反向代理服务器，前端静态资源由 Nginx 直接提供，API 请求转发给后端 Java 服务。

### 1. 准备后端
确保后端在端口 `6401` 运行。
```bash
cd backend
mvn package
java -jar target/zhouyi-backend-0.0.1-SNAPSHOT.jar
```

### 2. 准备前端
您已经构建了前端（位于 `frontend/dist` 目录）。
将 `frontend/dist` 目录上传到服务器，例如 `/var/www/zhouyi/dist`。

### 3. 配置 Nginx
使用 Nginx 监听 80 端口，并配置路径映射。

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 1. 前端页面 (访问 /book/ZhouYi)
    location /book/ZhouYi {
        alias /var/www/zhouyi/dist; # 指向前端构建目录
        try_files $uri $uri/ /book/ZhouYi/index.html; # 支持 React 路由
    }

    # 2. 后端 API (访问 /api)
    location /api {
        proxy_pass http://localhost:6401; # 转发给后端
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 3. 静态图片资源 (访问 /images)
    location /images {
        proxy_pass http://localhost:6401; # 由后端提供图片，或者直接 alias 到后端的 static/images 目录
    }
}
```

## 选项二：合并部署 (最简单 - 单一服务)
如果您不想安装 Nginx，可以将前端构建产物放入后端 Jar 包中，由 Spring Boot 直接服务。

### 1. 移动前端文件
将 `frontend/dist` 文件夹内的所有内容复制到 `backend/src/main/resources/static/book/ZhouYi/` 目录下。
*(注意：需要先创建该目录)*

### 2. 打包并运行后端
```bash
cd backend
mvn package
java -jar target/zhouyi-backend-0.0.1-SNAPSHOT.jar
```

此时，访问 `http://your-server-ip:6401/book/ZhouYi/` 即可看到网站。

## 注意事项
1. **API 地址**: 前端代码已修改为使用相对路径 `/api`，因此无论哪种部署方式，只要 `/api` 能正确转发到后端即可。
2. **路由**: 前端路由基础路径已设置为 `/book/ZhouYi`，请确保访问地址包含此路径。
