# Deployment Guide

Complete guide for deploying Stock Prediction application to production.

## Table of Contents
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
  - [Azure](#azure)
  - [AWS](#aws)
  - [Heroku](#heroku)

## Local Development

### Quick Start

1. **Clone and setup project**
   ```bash
   cd StockPrediction
   ```

2. **Backend setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

3. **ML Model training**
   ```bash
   cd ../ml_model
   pip install -r requirements.txt
   python train.py --ticker AAPL
   ```

4. **Frontend setup**
   ```bash
   cd ../frontend
   npm install
   cp .env.example .env
   ```

5. **Run development servers**
   ```bash
   # Terminal 1: Backend
   cd backend
   python -m uvicorn main:app --reload

   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

Access application at:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Docker Deployment

### Using Docker Compose

1. **Build and start services**
   ```bash
   docker-compose up -d
   ```

2. **View status**
   ```bash
   docker-compose ps
   ```

3. **View logs**
   ```bash
   docker-compose logs -f service_name
   ```

4. **Stop services**
   ```bash
   docker-compose down
   ```

### Manual Docker Build

**Backend**
```bash
docker build -f docker/Dockerfile.backend -t stockpred-backend:latest .
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./stock_prediction.db \
  -e SECRET_KEY=your-secret-key \
  stockpred-backend:latest
```

**Frontend**
```bash
docker build -f docker/Dockerfile.frontend -t stockpred-frontend:latest .
docker run -p 3000:3000 \
  -e VITE_API_URL=http://localhost:8000/api \
  stockpred-frontend:latest
```

## Cloud Deployment

### Azure Deployment

#### Prerequisites
- Azure account
- Azure CLI installed
- Docker images built

#### Step 1: Create Azure Resources

```bash
# Login to Azure
az login

# Create resource group
az group create --name stock-prediction-rg --location eastus

# Create Container Registry
az acr create --resource-group stock-prediction-rg \
  --name stockpredregistry --sku Basic

# Login to registry
az acr login --name stockpredregistry
```

#### Step 2: Push Docker Images

```bash
# Build backend image
docker build -f docker/Dockerfile.backend \
  -t stockpredregistry.azurecr.io/stockpred-backend:latest .

# Push backend
docker push stockpredregistry.azurecr.io/stockpred-backend:latest

# Build and push frontend
docker build -f docker/Dockerfile.frontend \
  -t stockpredregistry.azurecr.io/stockpred-frontend:latest .

docker push stockpredregistry.azurecr.io/stockpred-frontend:latest
```

#### Step 3: Deploy Backend to Container Instances

```bash
# Create PostgreSQL server
az postgres server create \
  --resource-group stock-prediction-rg \
  --name stock-prediction-db \
  --admin-user dbadmin \
  --admin-password <strong-password> \
  --sku-name B_Gen5_1 \
  --storage-size 51200

# Deploy backend container
az container create \
  --resource-group stock-prediction-rg \
  --name stock-prediction-backend \
  --image stockpredregistry.azurecr.io/stockpred-backend:latest \
  --cpu 2 \
  --memory 3 \
  --registry-login-server stockpredregistry.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --port 8000 \
  --environment-variables \
    DATABASE_URL="postgresql://..." \
    SECRET_KEY="<your-secret-key>" \
    MODEL_DIR="/app/models"
```

#### Step 4: Deploy Frontend to Static Web Apps

```bash
# Create static web app
az staticwebapp create \
  --resource-group stock-prediction-rg \
  --name stock-prediction-frontend \
  --source https://github.com/<your-repo> \
  --location eastus \
  --branch main \
  --api-location api
```

#### Step 5: Configure Environment Variables

Update your Azure resources with:
```
VITE_API_URL=https://your-backend-url/api
VITE_WS_URL=wss://your-backend-url/ws
```

### AWS Deployment

#### Prerequisites
- AWS account
- AWS CLI configured
- Docker images ready

#### Step 1: Push to ECR

```bash
# Create ECR repositories
aws ecr create-repository --repository-name stockpred-backend --region us-east-1
aws ecr create-repository --repository-name stockpred-frontend --region us-east-1

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push images
docker tag stockpred-backend:latest \
  <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/stockpred-backend:latest

docker push <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/stockpred-backend:latest
```

#### Step 2: Create RDS Database

```bash
aws rds create-db-instance \
  --db-instance-identifier stock-prediction-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username dbadmin \
  --master-user-password <strong-password> \
  --allocated-storage 20
```

#### Step 3: Deploy on ECS

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name stock-prediction

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster stock-prediction \
  --service-name stock-prediction-backend \
  --task-definition stock-prediction-backend \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx]}"
```

#### Step 4: Deploy Frontend to S3 + CloudFront

```bash
# Create S3 bucket
aws s3 mb s3://stock-prediction-frontend --region us-east-1

# Build frontend
cd frontend
npm run build

# Upload to S3
aws s3 cp dist/ s3://stock-prediction-frontend/ --recursive

# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name stock-prediction-frontend.s3.amazonaws.com \
  --default-root-object index.html
```

### Heroku Deployment

#### Backend

1. **Create Procfile**
   ```
   web: gunicorn main:app
   ```

2. **Update requirements.txt**
   ```bash
   pip freeze > requirements.txt
   echo "gunicorn==20.1.0" >> requirements.txt
   ```

3. **Deploy**
   ```bash
   heroku create stock-prediction-api
   heroku addons:create heroku-postgresql:hobby-dev
   git push heroku main
   ```

#### Frontend

1. **Using Vercel (Recommended)**
   ```bash
   npm i -g vercel
   vercel
   ```

2. **Set environment variables in Vercel dashboard**

## Production Checklist

### Security
- [ ] Change SECRET_KEY to strong, random value
- [ ] Enable HTTPS/SSL
- [ ] Set secure headers (CORS, CSP, etc.)
- [ ] Use environment variables for secrets
- [ ] Enable database backups
- [ ] Set up rate limiting

### Monitoring
- [ ] Configure logging (CloudWatch, ELK, etc.)
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Monitor resource usage (CPU, memory)
- [ ] Set up uptime monitoring
- [ ] Create alerts for critical issues

### Performance
- [ ] Configure CDN for frontend
- [ ] Enable caching (Redis)
- [ ] Optimize database queries
- [ ] Use compression for assets
- [ ] Enable pagination for API responses

### Maintenance
- [ ] Set up automated backups
- [ ] Plan model retraining schedule
- [ ] Monitor model performance
- [ ] Update dependencies regularly
- [ ] Document deployment procedures

## Database Migrations

```bash
# For PostgreSQL setup
psql -U dbadmin -d stock_prediction \
  -f database/init.sql
```

## Model Management

```bash
# Train new model
python ml_model/train.py --ticker AAPL --epochs 100

# Retrain via API
curl -X POST http://localhost:8000/api/retrain \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "GOOGL",
    "epochs": 50,
    "batch_size": 32,
    "lstm_units": 128
  }'
```

## Troubleshooting

### Database Connection Issues
```bash
# Test connection
psql -h localhost -U user -d database

# Check logs
docker-compose logs postgres
```

### Model Not Found
```bash
# List available models
curl http://localhost:8000/api/models

# Train if missing
python ml_model/train.py --ticker AAPL
```

### Memory Issues
```bash
# Increase container memory
docker run --memory=2g stockpred-backend:latest

# Or in docker-compose.yml
services:
  backend:
    mem_limit: 2g
```

## Scaling Considerations

1. **Horizontal Scaling**: Use load balancer (nginx, AWS ALB)
2. **Database**: Consider read replicas for high traffic
3. **Caching**: Implement Redis for frequently accessed data
4. **Async Tasks**: Use Celery for model training
5. **CDN**: Distribute frontend assets globally

## Support

For deployment issues:
1. Check logs: `docker-compose logs service_name`
2. Review deployment guide
3. Check firewall and network settings
4. Verify environment variables

---

Happy deploying! 🚀
