# 🚀 Phase II - Quick Start Guide

## ⚡ 30-Second Start (Docker)

```bash
# Clone/navigate to project
cd "D:\zainab\hackathon II"

# Start all services
docker-compose up -d

# Wait for services
sleep 30

# Open in browser
# Frontend:  http://localhost:3000
# API Docs:  http://localhost:8000/docs
```

## 📋 What's Running

| Service | URL | Status |
|---------|-----|--------|
| Frontend (Next.js) | http://localhost:3000 | ✅ |
| Backend API (FastAPI) | http://localhost:8000 | ✅ |
| API Documentation | http://localhost:8000/docs | ✅ |
| Database (PostgreSQL) | localhost:5432 | ✅ |

## 🎯 Try It Out

### In Browser
1. Open http://localhost:3000
2. Type task title: "Buy groceries"
3. Click Create
4. Check the checkbox to mark complete
5. Click Delete to remove

### Via API

```bash
# Create task
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","priority":"MEDIUM"}'

# List tasks
curl http://localhost:8000/api/tasks

# Get documentation
open http://localhost:8000/docs
```

## 🛠️ Development Setup

### Backend Development
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env

# Run with hot-reload
uvicorn src.main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Configure
cp .env.example .env.local

# Run dev server (hot reload)
npm run dev

# Tests
npm test                    # Jest unit tests
npm run test:e2e           # Cypress E2E tests
```

## 📦 Project Files

### Important Directories
```
backend/src/
├── models/       # SQLModel schemas
├── services/     # Business logic
├── api/          # REST endpoints
└── core/         # Config & errors

frontend/src/
├── pages/        # Next.js routes
├── components/   # React components
├── hooks/        # Data fetching (SWR)
├── services/     # API client
└── types/        # TypeScript types
```

## 🧪 Running Tests

```bash
# Backend tests
cd backend
pytest                  # Run all
pytest -v              # Verbose
pytest --cov           # Coverage

# Frontend tests
cd frontend
npm test                # Jest
npm run test:e2e       # Cypress
```

## 🔧 Common Commands

### Docker Commands
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Rebuild images
docker-compose build --no-cache
```

### Backend Commands
```bash
# Run server
uvicorn src.main:app --reload

# Run tests
pytest -v

# Format code
black src/

# Lint code
pylint src/
```

### Frontend Commands
```bash
# Dev server
npm run dev

# Build
npm run build

# Start production
npm start

# Tests
npm test
npm run test:e2e
```

## 📚 API Reference

### Task Endpoints
| Method | URL | Purpose |
|--------|-----|---------|
| GET | `/api/tasks` | List tasks |
| POST | `/api/tasks` | Create task |
| GET | `/api/tasks/{id}` | Get task |
| PUT | `/api/tasks/{id}` | Update task |
| PATCH | `/api/tasks/{id}/status` | Mark complete |
| DELETE | `/api/tasks/{id}` | Delete task |

### Query Examples
```bash
# All pending tasks
/api/tasks?status=pending

# High priority
/api/tasks?priority=HIGH

# Search for "urgent"
/api/tasks?search=urgent

# Page 2 (50 per page)
/api/tasks?skip=50&limit=50

# Sort by due date
/api/tasks?sort_by=due_date&sort_order=asc
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9

# Windows: Use Task Manager to kill Node/Python
```

### Database Connection Error
```bash
# Check if PostgreSQL is running
psql -U todo_user -d todo_db -c "SELECT 1"

# Check DATABASE_URL in backend/.env
# Should be: postgresql://todo_user:todo_password@localhost:5432/todo_db
```

### Docker Issues
```bash
# Clean up all containers and volumes
docker-compose down -v

# Rebuild everything
docker-compose build --no-cache

# Start fresh
docker-compose up -d
```

## 📖 Full Documentation

- **[README_PHASE_II.md](./README_PHASE_II.md)** - Complete user guide
- **[IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)** - Detailed setup
- **[PHASE_II_IMPLEMENTATION_SUMMARY.md](./PHASE_II_IMPLEMENTATION_SUMMARY.md)** - What was built

## 🔐 Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://todo_user:todo_password@localhost:5432/todo_db
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=info
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_DEBUG=false
```

## ✅ Verification

### Check Backend is Running
```bash
curl http://localhost:8000/docs
# Should show Swagger UI
```

### Check Frontend is Running
```bash
curl http://localhost:3000
# Should return HTML
```

### Check Database Connection
```bash
# Backend logs should show:
# INFO: PostgreSQL connected successfully
```

## 🚀 Production Deployment

### Docker Build
```bash
# Build images
docker-compose build

# Push to registry (optional)
docker tag phase-ii-backend:latest myregistry/backend:latest
docker push myregistry/backend:latest
```

### Environment for Production
```
# Backend .env
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=<production-db-url>
CORS_ORIGINS=https://yourdomain.com

# Frontend .env.production
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_DEBUG=false
```

## 📞 Need Help?

1. **API Documentation**: http://localhost:8000/docs (interactive)
2. **Read Logs**: `docker-compose logs -f [service]`
3. **Check Status**: `docker-compose ps`
4. **Review Guides**:
   - IMPLEMENTATION_GUIDE.md for detailed setup
   - README_PHASE_II.md for complete reference

## 🎓 Learning Path

1. **First Time?** → Try the 30-second Docker start above
2. **Want to Develop?** → Follow the Development Setup section
3. **Need Details?** → Read IMPLEMENTATION_GUIDE.md
4. **Curious About Code?** → Review PHASE_II_IMPLEMENTATION_SUMMARY.md

## ✨ What You Can Do

- ✅ Create, update, and delete tasks
- ✅ Mark tasks as complete
- ✅ Search for tasks
- ✅ Filter by status and priority
- ✅ Sort by various fields
- ✅ Paginate through large lists
- ✅ View API documentation
- ✅ Run automated tests
- ✅ Deploy with Docker

## 🎉 Phase II is Complete!

All backend APIs, frontend components, tests, and documentation are ready.

**Next**: Phase III - AI Chatbot Integration

---

**Last Updated**: 2024-12-30 | **Status**: ✅ Ready for Use
