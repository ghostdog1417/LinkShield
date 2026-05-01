# Deployment Configuration for LinkShield

## Production Environment Variables

```bash
# Backend
FLASK_ENV=production
FLASK_DEBUG=False

# Frontend
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_ENVIRONMENT=production
```

## Docker Deployment

### Backend Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "backend/app.py"]
```

### Frontend Dockerfile
```dockerfile
FROM node:18-alpine as builder

WORKDIR /app

COPY frontend/package*.json .
RUN npm install

COPY frontend .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./fake_link_detector:/app/fake_link_detector

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

## Deployment Steps

1. **Build Docker images**
   ```bash
   docker-compose build
   ```

2. **Run containers**
   ```bash
   docker-compose up -d
   ```

3. **Access application**
   - Frontend: http://localhost
   - API: http://localhost:5000

## Performance Optimization

- Use production build for React: `npm run build`
- Enable compression in Flask
- Configure CDN for static assets
- Use environment-specific settings
- Enable caching for model predictions

## Security Considerations

- Use HTTPS in production
- Validate and sanitize URL inputs
- Implement rate limiting on API
- Use environment variables for secrets
- Enable CORS only for trusted domains
- Keep dependencies updated
