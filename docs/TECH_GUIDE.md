# 技术方案总览与开发维护指南

## 项目概览

- 后端：Spring Boot（JDK 17），端口 6401。入口：[ZhouYiApplication.java](file:///e:/GitProjects/MyProject/ZhouYi/backend/src/main/java/com/zhouyi/demo/ZhouYiApplication.java)
- 前端：React + Vite，开发端口 6400，生产部署路径 `/book/ZhouYi/`。配置：[vite.config.js](file:///e:/GitProjects/MyProject/ZhouYi/frontend/vite.config.js)
- 数据源：`ZhouYi.md`（规范化 Markdown），默认打包在后端类路径，可通过环境变量外置
- 部署：Docker Compose（前端 Nginx + 后端 Java），一次性部署与增量更新脚本位于 `scripts/`

## 周易文本到 Markdown 的处理流程

### 处理目标与规范

- 每卦独立段落，以 `## 第N卦 卦名 ...` 为标题，其中 N 必须为阿拉伯数字
- 顶部插入卦象图片：`![卦名](/images/XX_卦名.svg)`
- 明确的卦象二进制编码：`**卦象编码**：011101（初爻 -> 上爻）`
- 段落结构按“卦辞、彖曰、象曰、六爻”组织，必要时将“象曰”“子曰”分行并以引用格式强调

### 关键脚本

- 数据抽取与重组：[scripts/fix_zhouyi.py](file:///e:/GitProjects/MyProject/ZhouYi/scripts/fix_zhouyi.py)
  - 解析现有 `ZhouYi.md` 与源文本，提取每卦图片、编码、正文结构
  - 统一标题、补齐编码、写出新的规范化 Markdown（例如 `ZhouYi_fixed.md`）
- 版式优化与排版：[format_zhouyi.py](file:///e:/GitProjects/MyProject/ZhouYi/format_zhouyi.py)
  - 将“象曰”“子曰”从行内拆分为引用
  - 统一列表、空行与段落结构，减少渲染噪声，产出 `ZhouYi_formatted.md`

推荐落地策略：以 `fix_zhouyi.py` 先标准化结构，再用 `format_zhouyi.py` 做版式优化，生成最终投喂后端的 `ZhouYi.md`。

## 后端技术要点

### 数据加载与扩展

- 服务： [HexagramService.java](file:///e:/GitProjects/MyProject/ZhouYi/backend/src/main/java/com/zhouyi/demo/service/HexagramService.java)
  - 启动时读取 Markdown，正则解析出 id、name、imageUrl、binaryCode、fullText 等字段
  - 当缺少爻结构时，依据 `binaryCode` 自动生成六爻数据（阴阳与位次）
  - 环境变量 `ZHOUYI_DATA_PATH` 指定外置 Markdown 路径，不设则读取类路径内置文件

- API： [HexagramController.java](file:///e:/GitProjects/MyProject/ZhouYi/backend/src/main/java/com/zhouyi/demo/controller/HexagramController.java)
  - `GET /api/hexagrams` 返回全量列表
  - `GET /api/hexagrams/{id}` 返回单卦详情
  - `GET /api/hexagrams/search?q=关键词` 进行全文搜索

- AI 对话： [AIController.java](file:///e:/GitProjects/MyProject/ZhouYi/backend/src/main/java/com/zhouyi/demo/controller/AIController.java)
  - 基于 GLM Chat Completions，简易 RAG：从本地周易文本中检索片段拼接为上下文
  - 密钥来源：环境变量 `GLM_API_KEY`（在 [application.properties](file:///e:/GitProjects/MyProject/ZhouYi/backend/src/main/resources/application.properties) 中通过 `${GLM_API_KEY:}` 引用）

### 数据模型

- 实体： [Hexagram.java](file:///e:/GitProjects/MyProject/ZhouYi/backend/src/main/java/com/zhouyi/demo/model/Hexagram.java) 与 [Yao.java](file:///e:/GitProjects/MyProject/ZhouYi/backend/src/main/java/com/zhouyi/demo/model/Yao.java)
  - `Hexagram`：id、name、binaryCode、imageUrl、fullText、yaos
  - `Yao`：id、name、isYang 及文本字段

## 前端功能点

### 列表与搜索

- 列表页： [HexagramList.jsx](file:///e:/GitProjects/MyProject/ZhouYi/frontend/src/components/HexagramList.jsx)
  - 初始化拉取 `/api/hexagrams` 渲染卡片网格
  - 图片路径采用根路径 `/images/...`，开发态通过 Vite 代理转发到后端
  - 搜索弹窗使用 `/api/hexagrams/search?q=...` 展示高亮摘要

- 搜索页： [Search.jsx](file:///e:/GitProjects/MyProject/ZhouYi/frontend/src/components/Search.jsx)
  - 独立页面发起搜索，路由为 `/search`

### 单卦阅读与即时六爻绘制

- 阅读页： [Reading.jsx](file:///e:/GitProjects/MyProject/ZhouYi/frontend/src/components/Reading.jsx)
  - 拉取 `/api/hexagrams/{id}` 展示 Markdown 正文与六爻结构
  - 若服务端未提供完整 `yaos`，则由 `binaryCode` 在前端生成六爻可视化
  - 六爻绘制样式： [Reading.css](file:///e:/GitProjects/MyProject/ZhouYi/frontend/src/components/Reading.css) 中的 `.solid-line` 与 `.broken-line`

#### 本地实现 64 卦图的绘制

核心思路：以六位二进制串表示自下而上的六爻（1=阳、0=阴），前端将其翻转后自上而下渲染。示例组件（传入 `binary` 字符串）可参考阅读页中生成逻辑，样式复用 `Reading.css` 的 `.solid-line` 与 `.broken-line`。

```jsx
import React from 'react'

export default function HexagramFigure({ binary }) {
  const bits = (binary || '').split('').map(b => b === '1')
  const topDown = [...bits].reverse()
  return (
    <div style={{display:'flex',flexDirection:'column',gap:'6px'}}>
      {topDown.map((isYang, i) => (
        <div key={i} className="yao-line">
          {isYang ? <div className="solid-line"></div> : <div className="broken-line"><span></span><span></span></div>}
        </div>
      ))}
    </div>
  )
}
```

你可以在任意页面引入该组件并传入任意六位编码，从而即时绘制本卦卦象。结合服务端提供的 `binaryCode`，即可在本地渲染全部 64 卦。

### AI 问答

- 组件： [Chat.jsx](file:///e:/GitProjects/MyProject/ZhouYi/frontend/src/components/Chat.jsx)
  - 将用户问题 POST 至 `/api/chat`
  - 服务端基于本地检索拼接上下文调用 GLM，前端呈现回答
  - 需要云端正确配置 `GLM_API_KEY`

### 开发代理与生产部署路径

- 开发代理： [vite.config.js](file:///e:/GitProjects/MyProject/ZhouYi/frontend/vite.config.js)
  - `/api` 与 `/images` 转发到 `http://localhost:6401`
- 生产路径：`base: '/book/ZhouYi/'`，Nginx 负责将构建产物挂载到该子路径下

## 部署与维护

### 一次性部署与增量更新

- 一次性部署并重建后端： [scripts/deploy_cloud.ps1](file:///e:/GitProjects/MyProject/ZhouYi/scripts/deploy_cloud.ps1) 携带 `-BuildBackend`
- 仅同步配置/前端/数据：同脚本不加参数，默认不重建后端镜像
- 仅更新前端：构建 `frontend/dist` 后执行 [scripts/update_frontend.ps1](file:///e:/GitProjects/MyProject/ZhouYi/scripts/update_frontend.ps1)
- 仅更新周易文档：执行 [scripts/update_backend_data.ps1](file:///e:/GitProjects/MyProject/ZhouYi/scripts/update_backend_data.ps1)，后端从数据卷读取，无需重建镜像

更多细节见运维文档：[docs/ops.md](file:///e:/GitProjects/MyProject/ZhouYi/docs/ops.md)

### 密钥与安全

- `GLM_API_KEY` 仅在服务器 `ZhouYi_Final/.env` 中维护，不写入仓库
- 建议使用 SSH Key 免密部署，避免在脚本中硬编码密码

## 研发规范与后续维护

- 文档规范：新增加的卦文必须包含图片与二进制编码，标题以阿拉伯数字标注“第N卦”
- 图片规范：统一放置于后端静态目录 [backend/static/images](file:///e:/GitProjects/MyProject/ZhouYi/backend/src/main/resources/static/images/)，命名 `XX_卦名.svg`
- 功能扩展建议：
  - 将搜索改为分词索引，提高召回与排序质量
  - 对 64 卦图增加 SVG 生成器，便于缩放与导出
  - 为 AI 问答引入对话上下文与引用出处标注

## 常见问题

- 图片不显示
  - 检查前端是否向 `/images/...` 发起请求
  - 开发态看 Vite 代理是否指向 `localhost:6401`
  - 生产态由 Nginx 映射到后端容器

- `API Key not configured`
  - 确认云端 `ZhouYi_Final/.env` 写入 `GLM_API_KEY=...`
  - 首次注入需要重新创建后端容器，使用 `docker-compose down && docker-compose up -d`

