# 运维与维护（本地/云端）

## 本地开发运行

### 后端（Spring Boot）

- 入口类：[ZhouYiApplication.java](file:///e:/GitProjects/MyProject/ZhouYi/backend/src/main/java/com/zhouyi/demo/ZhouYiApplication.java)
- 端口：`6401`（见 [application.properties](file:///e:/GitProjects/MyProject/ZhouYi/backend/src/main/resources/application.properties)）

推荐用脚本启动（无需本机预装 Maven）：

```powershell
cd backend
powershell -ExecutionPolicy Bypass -File .\run_local.ps1
```

验证：

```powershell
curl -I http://localhost:6401/api/hexagrams
curl -I http://localhost:6401/images/01_%E4%B9%BE.svg
```

环境变量：

- `GLM_API_KEY`：AI 问答所需（未设置时 `/api/chat` 会返回 “API Key not configured”）
- `ZHOUYI_DATA_PATH`：可选，指定外部 `ZhouYi.md` 路径；不设置则读取 classpath `data/ZhouYi.md`。

### 前端（React + Vite）

- 端口：`6400`（见 [vite.config.js](file:///e:/GitProjects/MyProject/ZhouYi/frontend/vite.config.js)）
- 路由基址：`/book/ZhouYi/`（见 [vite.config.js](file:///e:/GitProjects/MyProject/ZhouYi/frontend/vite.config.js) 与 [App.jsx](file:///e:/GitProjects/MyProject/ZhouYi/frontend/src/App.jsx)）

启动：

```powershell
cd frontend
npm install
npm run dev
```

访问：

- `http://localhost:6400/book/ZhouYi/`

前端与后端联调方式：

- 通过 Vite 代理转发 `/api` 与 `/images` 到 `http://localhost:6401`
- 相关配置在 [vite.config.js](file:///e:/GitProjects/MyProject/ZhouYi/frontend/vite.config.js)

## 周易文档（ZhouYi.md）处理与格式约束

后端解析依赖的关键格式（见 [HexagramService.java](file:///e:/GitProjects/MyProject/ZhouYi/backend/src/main/java/com/zhouyi/demo/service/HexagramService.java)）：

- 每一卦必须以标题行开头，且标题使用阿拉伯数字：
  - `## 第50卦 鼎 ...`
- 卦象编码必须包含：
  - `**卦象编码**：011101（初爻 -> 上爻）`
- 图片使用 Markdown 图片语法：
  - `![鼎](/images/50_鼎.svg)` 或 `![鼎](images/50_鼎.svg)`

推荐处理脚本：

- [fix_zhouyi.py](file:///e:/GitProjects/MyProject/ZhouYi/scripts/fix_zhouyi.py)
  - 统一标题为 `## 第N卦 ...`（N 为阿拉伯数字）
  - 补全 64 卦的二进制编码（Bottom->Top，1=阳，0=阴）
  - 统一图片路径为 `/images/XX_卦名.svg`，避免在子路径部署时出现相对路径错误

产物：

- 后端使用的原始数据： [ZhouYi.md](file:///e:/GitProjects/MyProject/ZhouYi/backend/src/main/resources/data/ZhouYi.md)

## 云端部署（ZhouYi_Final）

### 一次性部署

执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\deploy_cloud.ps1 -BuildBackend
```

脚本会同步：

- [docker-compose.yml](file:///e:/GitProjects/MyProject/ZhouYi/docker-compose.yml)
- [nginx.conf](file:///e:/GitProjects/MyProject/ZhouYi/deployment/nginx/nginx.conf)
- 后端关键文件与数据
- 前端 `frontend/dist`

并在云端构建一次后端镜像并启动服务。

### 后续仅更新文档（不重建镜像）

执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\update_backend_data.ps1
```

原因：

- 现已支持从挂载卷读取 `ZhouYi.md`：
  - compose 会把云端 `backend/src/main/resources/data` 挂载到容器 `/data`
  - 并设置 `ZHOUYI_DATA_PATH=/data/ZhouYi.md`
  - 所以更新 md 后只需重启后端即可，无需重新构建 jar/镜像

### 后续仅更新前端（不重建镜像）

构建：

```powershell
cd frontend
npm run build
```

上传并重启：

```powershell
cd ..
powershell -ExecutionPolicy Bypass -File .\scripts\update_frontend.ps1
```

### 云端可用性验证（从本机）

当前容器 nginx 暴露在 `6400`，外部可直接验证（无需 ssh）：

```powershell
curl -I http://47.109.193.180:6400/book/ZhouYi/
curl -I http://47.109.193.180:6400/api/hexagrams
curl -I http://47.109.193.180:6400/images/01_%E4%B9%BE.svg
```

## 仅同步配置/前端/数据（不重建后端）

当只改动了 compose/nginx/前端 dist/周易 md 时，执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\deploy_cloud.ps1
```

## 密钥与密码（重要）

- 不要把云端密码写进仓库、脚本或文档。
- 推荐用 SSH Key（免密）+ 服务器侧禁用密码登录来替代密码。
- `GLM_API_KEY` 推荐放在云端 `ZhouYi_Final/.env`（仅保存在服务器，不提交到仓库），由 compose 自动读取。
