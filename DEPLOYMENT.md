# 🚀 ALGSOCH Platform - Complete Build Guide

## 📋 Prerequisites

Ensure you have the following installed:

- **Docker & Docker Compose** (v20+)
- **Node.js** (v18+)
- **Python** (v3.11+)
- **Java JDK** (v17+)
- **Maven** (v3.9+)
- **PostgreSQL** (v15+) - Optional if using Docker

## 🏗️ Quick Start (Docker - Recommended)

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd algsoch
cp .env.example .env
```

### 2. Start All Services

```bash
chmod +x scripts/start.sh
./scripts/start.sh
```

This will:
- Build all Docker images
- Start PostgreSQL, Python API, Java Analytics, Frontend, and Nginx
- Initialize the database
- Create default admin user

### 3. Access the Platform

- **Frontend**: http://localhost:5173
- **Python API**: http://localhost:8000
- **Java Analytics**: http://localhost:8080
- **API Documentation**: http://localhost:8000/docs
- **Nginx Reverse Proxy**: http://localhost

**Default Admin Credentials:**
- Username: `admin`
- Password: `changeme`

### 4. Stop Services

```bash
./scripts/stop.sh
```

---

## 🔧 Manual Setup (Development)

### Backend Python (FastAPI)

```bash
cd backend-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb algsoch  # Or use existing PostgreSQL instance

# Run migrations (if using Alembic)
# alembic upgrade head

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify**: Visit http://localhost:8000/docs

### Backend Java (Spring Boot)

```bash
cd backend-java

# Build project
mvn clean install

# Run application
mvn spring-boot:run
```

**Verify**: Visit http://localhost:8080/api/analytics/health

### Frontend (React + Vite)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Verify**: Visit http://localhost:5173

### Mobile App (React Native + Expo)

```bash
cd mobile-app

# Install dependencies
npm install

# Start Expo
npm start

# Run on device
npm run android  # For Android
npm run ios      # For iOS (Mac only)
```

---

## 🧪 Testing

### Python Backend Tests

```bash
cd backend-python
pytest tests/ -v --cov=app
```

### Java Backend Tests

```bash
cd backend-java
mvn test
```

### Frontend Tests

```bash
cd frontend
npm run test
npm run lint
```

---

## 🐳 Docker Commands Reference

```bash
# Build all images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend-python

# Stop services
docker-compose down

# Remove volumes
docker-compose down -v

# Rebuild and restart
docker-compose up -d --build

# Check service status
docker-compose ps

# Execute command in container
docker-compose exec backend-python bash
```

---

## 🔑 Environment Variables

Create `.env` in the root directory:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/algsoch

# JWT
JWT_SECRET=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=changeme
ADMIN_EMAIL=admin@algsoch.com

# Frontend
VITE_API_URL=http://localhost:8000
VITE_ANALYTICS_API_URL=http://localhost:8080
VITE_WS_URL=ws://localhost:8000

# Spring Boot
SPRING_PROFILES_ACTIVE=dev
SERVER_PORT=8080
```

---

## 🚀 Production Deployment

### Build Production Images

```bash
# Build optimized images
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# Push to registry (optional)
docker tag algsoch-frontend:latest your-registry/algsoch-frontend:latest
docker push your-registry/algsoch-frontend:latest
```

### Deploy to Azure Container Apps

```bash
cd infra/azure

# Login to Azure
az login

# Deploy
az containerapp up \
  --name algsoch \
  --resource-group algsoch-rg \
  --location eastus \
  --environment algsoch-env \
  --image your-registry/algsoch-frontend:latest
```

### Deploy to DigitalOcean

```bash
# Install doctl
brew install doctl  # macOS
# or download from digitalocean.com

# Authenticate
doctl auth init

# Create app
doctl apps create --spec .do/app.yaml
```

### Deploy Frontend to Vercel

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel deploy --prod
```

---

## 📊 Monitoring & Logs

### View Application Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend-python

# Last 100 lines
docker-compose logs --tail=100 backend-python
```

### Database Access

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres -d algsoch

# Run SQL
psql -U postgres -d algsoch -c "SELECT * FROM users;"
```

### Health Checks

```bash
# Python API
curl http://localhost:8000/health

# Java Analytics
curl http://localhost:8080/api/analytics/health

# Nginx
curl http://localhost/health
```

---

## 🛠️ Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Docker Issues

```bash
# Clean up Docker
docker system prune -a

# Remove all containers
docker rm -f $(docker ps -aq)

# Remove all images
docker rmi -f $(docker images -q)
```

### Database Connection Issues

1. Check PostgreSQL is running
2. Verify `DATABASE_URL` in `.env`
3. Ensure database exists: `createdb algsoch`
4. Check firewall/network settings

### Frontend Not Loading

1. Clear browser cache
2. Check API URL in `.env`
3. Verify backend is running
4. Check CORS configuration

---

## 📝 Development Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Make changes and test**
   ```bash
   # Run tests
   pytest  # Python
   mvn test  # Java
   npm test  # Frontend
   ```

3. **Commit and push**
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```

4. **Create Pull Request**
   - GitHub will run CI/CD pipeline
   - Review and merge

---

## 🔐 Security Notes

**CRITICAL**: Change these before production:

1. `JWT_SECRET` - Use strong random string
2. `ADMIN_PASSWORD` - Use strong password
3. `DATABASE_URL` - Use secure credentials
4. Enable HTTPS/TLS
5. Configure proper CORS origins
6. Enable rate limiting
7. Set up monitoring and alerts

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Spring Boot Guide](https://spring.io/guides)
- [React Documentation](https://react.dev/)
- [Docker Compose](https://docs.docker.com/compose/)
- [PostgreSQL Manual](https://www.postgresql.org/docs/)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request
5. Wait for review

---

## 📞 Support

- **Issues**: Create GitHub issue
- **Email**: npdimagine@gmail.com
- **Documentation**: See `/docs` folder

---

**Built with ❤️ by Vicky Kumar**
