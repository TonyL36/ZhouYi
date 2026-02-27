# ZhouYi
48小时完成的周易电子阅读系统，可以与AI一起聊周易。

## Project Structure
- `backend`: Spring Boot application (Java 17)
- `frontend`: React application (Vite)

## Prerequisites
- Java 17 or higher
- Node.js 18+

## Setup & Run (Local)

### Backend
```powershell
cd backend
powershell -ExecutionPolicy Bypass -File .\run_local.ps1
```

Backend listens on `http://localhost:6401`.

### Frontend
```powershell
cd frontend
npm install
npm run dev
```

Frontend listens on `http://localhost:6400/book/ZhouYi/`.

## Features
- **Home**: View all 64 Hexagrams.
- **Reading**: Read specific Hexagram with original text and Yao structure.
- **Search**: Search by name or content.
- **AI Chat**: Ask questions about Zhou Yi using GLM AI.

## Data Source
- Hexagram images: `backend/src/main/resources/static/images`
- Text content: `backend/src/main/resources/data/ZhouYi.md`

## Docs
- Tech guide: `docs/TECH_GUIDE.md`
- Ops guide: `docs/ops.md`
