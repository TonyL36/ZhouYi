# Zhou Yi Digital Project

## Project Structure
- `backend`: Spring Boot application (Java 17+)
- `frontend`: React application (Vite)

## Prerequisites
- Java 17 or higher
- Maven 3.6+
- Node.js 18+

## Setup & Run

### Backend
1. Navigate to `backend` directory.
2. Configure your GLM API Key in `src/main/resources/application.properties` (or set environment variable `GLM_API_KEY`).
   ```properties
   glm.api.key=YOUR_API_KEY_HERE
   ```
3. Run the application:
   ```bash
   mvn spring-boot:run
   ```
   The backend will start on `http://localhost:8080`.

### Frontend
1. Navigate to `frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will start on `http://localhost:5173`.

## Features
- **Home**: View all 64 Hexagrams.
- **Reading**: Read specific Hexagram with original text, explanation, and Yao structure.
- **Search**: Search for hexagrams by name or content.
- **AI Chat**: Ask questions about Zhou Yi using GLM AI.

## Data Source
- Hexagram images are generated as SVGs.
- Text content is stored in `backend/src/main/resources/data/ZhouYi.md`. You can edit this file to add more detailed content.
