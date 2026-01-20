# Train Ticketing System - Hackathon Implementation Plan

## Overview
24-hour hackathon to build a scalable train ticketing system handling high traffic (30M+ hits in 30 minutes during peak Eid season).

**Team Size:** 3 people  
**Tech Stack:** Flask, PostgreSQL, RabbitMQ, Redis, Docker, Nginx  
**Additional Tools:** Prometheus, Grafana, Locust/k6 for load testing

---

## Team Structure & Time Allocation

**Person 1: Backend Services (Core)**
**Person 2: Backend Services (Supporting) + DevOps**
**Person 3: Frontend + Integration + Load Testing**

---

## Detailed Timeline (24 Hours)

### Hours 0-2: Setup & Architecture Design

**All Team Members:**
- Create GitHub repo with branch protection
- Design system architecture diagram
- Define microservices:
  1. **API Gateway** (nginx/traefik)
  2. **Auth Service** (login, OTP)
  3. **Train Service** (train info, search)
  4. **Booking Service** (seat selection, reservation)
  5. **Payment Service** (mock payment)
  6. **Notification Service** (mock OTP/email)

- Design database schemas (keep simple!)
- Set up project structure:
```
/services
  /auth-service
  /train-service
  /booking-service
  /payment-service
  /notification-service
  /api-gateway
/frontend
/infrastructure
/load-testing
docker-compose.yml
```

---

### Hours 2-8: Core Implementation (Sprint 1)

#### Person 1 - Critical Path Services:

**Booking Service** (MOST CRITICAL):
- POST /seats/select (with locking mechanism)
- POST /seats/confirm
- GET /bookings/:id
- Use PostgreSQL row-level locking or Redis for seat reservation
- Implement timeout for seat holds (5 min)
- Write unit tests

**Train Service**:
- GET /trains/search
- GET /trains/:id/seats
- Seed script for train data
- Write unit tests

#### Person 2 - Supporting Services:

**Auth Service**:
- POST /login
- POST /register
- POST /otp/request
- POST /otp/verify
- JWT token generation
- Mock OTP (just return code in response for testing)
- Write unit tests

**Notification Service**:
- POST /send-otp (mock - log to console)
- POST /send-confirmation (mock)
- RabbitMQ consumer setup
- Write unit tests

#### Person 3 - Frontend Foundation:

Simple React/Vue or plain HTML+JS frontend:
- Login page
- Train search page
- Seat selection page (visual seat map)
- Payment page
- Confirmation page
- Focus on functionality, not beauty

---

### Hours 8-10: Integration & Message Queue

#### Person 1:

**Payment Service**:
- POST /payment/initiate (mock)
- POST /payment/verify (mock)
- Publish events to RabbitMQ
- Write unit tests

#### Person 2:

- Set up RabbitMQ
- Implement event-driven communication:
  - Booking confirmed → Payment service
  - Payment success → Notification service
- Create docker-compose.yml with all services

#### Person 3:

- Integrate frontend with backend APIs
- Test end-to-end flow
- Fix integration issues

---

### Hours 10-12: API Gateway & Dockerization

#### Person 1:

- Configure nginx/traefik as API gateway
- Set up routing rules
- Add rate limiting (important for load testing!)
- Test all service communication

#### Person 2:

- Write Dockerfile for each service
- Complete docker-compose.yml:
  - All microservices
  - PostgreSQL instances (or shared with different DBs)
  - RabbitMQ
  - Redis (for caching/locking)
  - API Gateway
- Test docker-compose up

#### Person 3:

- Build frontend Docker image
- Test complete system with docker-compose
- Document API endpoints

---

### Hours 12-14: CI/CD Pipeline

#### Person 2 (Lead):

GitHub Actions workflows:
- `.github/workflows/ci.yml`:
  - Detect changed services
  - Run tests only for changed services
  - Build Docker images
- `.github/workflows/cd.yml`:
  - Deploy to cloud (AWS/GCP/DigitalOcean)
  - Rolling deployment strategy
- Set up branch protection rules

#### Person 1 & 3:

- Help with testing CI/CD
- Fix any failing tests
- Optimize service code

---

### Hours 14-16: Cloud Deployment

#### Person 2:

Provision cloud resources:
- Kubernetes cluster (EKS/GKE) OR Docker Swarm OR simple VMs
- Managed PostgreSQL
- Load balancer
- Deploy services
- Configure auto-scaling

#### Person 1:

Add monitoring setup:
- Prometheus for metrics
- Grafana dashboards
- Key metrics: request rate, error rate, latency, seat booking success rate

#### Person 3:

- Deploy frontend
- Update API endpoints to production URLs
- Smoke testing

---

### Hours 16-20: Load Testing

#### Person 3 (Lead):

Set up load testing with Locust/JMeter/k6:

```python
# Example locust scenario
from locust import HttpUser, task, between

class TrainBookingUser(HttpUser):
    wait_time = between(1, 2)
    
    @task(3)
    def select_seat(self):
        # Login
        # Search trains
        # Select seat (CRITICAL ENDPOINT)
        # Verify OTP
        # Make payment
```

- Run breakpoint testing on seat selection
- Document results: requests/sec, failure rate, response times
- Create graphs/charts

#### Person 1 & 2:

Monitor system during load tests and optimize:
- Add database indexes
- Implement caching (Redis)
- Tune connection pools
- Add more replicas for booking service

---

### Hours 20-22: Bonus Tasks (If Time Permits)

**Priority order:**
1. **Monitoring** (Prometheus + Grafana) - Person 1
2. **Better load testing scenarios** - Person 3
3. **Infrastructure as Code** (Terraform/Pulumi) - Person 2
4. **Orchestration** (Kubernetes manifests) - Person 2

---

### Hours 22-24: Presentation & Documentation

#### All Team Members:

Create presentation slides:
- Problem statement
- Architecture diagram
- Technology choices
- Key features (seat locking, event-driven, scalability)
- Load testing results
- CI/CD pipeline diagram
- Demo video/screenshots
- Challenges faced

Update README.md:
- Setup instructions
- How to run with docker-compose
- API documentation
- Load testing instructions

Final tasks:
- Final testing
- Record demo video (backup if live demo fails)
- Practice presentation

---

## Key Technical Decisions

### 1. Seat Locking Strategy (CRITICAL!)

**Option A: PostgreSQL row-level locking**
```python
# In booking service
SELECT * FROM seats WHERE id = ? FOR UPDATE NOWAIT;
```

**Option B: Redis distributed lock**
```python
import redis
r = redis.Redis()
lock = r.lock(f"seat:{seat_id}", timeout=300)
if lock.acquire(blocking=False):
    # Reserve seat
    lock.release()
```

**Recommendation:** Use Redis for better performance under high load.

---

### 2. Database Design (Simple!)

```sql
-- trains table
CREATE TABLE trains (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    route VARCHAR(200),
    departure_time TIMESTAMP,
    arrival_time TIMESTAMP
);

-- coaches table
CREATE TABLE coaches (
    id SERIAL PRIMARY KEY,
    train_id INTEGER REFERENCES trains(id),
    coach_number VARCHAR(10),
    total_seats INTEGER
);

-- seats table
CREATE TABLE seats (
    id SERIAL PRIMARY KEY,
    coach_id INTEGER REFERENCES coaches(id),
    seat_number VARCHAR(10),
    status VARCHAR(20), -- available/locked/booked
    locked_until TIMESTAMP,
    locked_by INTEGER,
    price DECIMAL(10,2)
);

-- bookings table
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    seat_id INTEGER REFERENCES seats(id),
    status VARCHAR(20),
    created_at TIMESTAMP,
    payment_status VARCHAR(20),
    booking_reference VARCHAR(50)
);

-- users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    phone VARCHAR(20),
    name VARCHAR(100)
);
```

---

### 3. Service Communication

**Synchronous:** REST APIs (for user-facing operations)
- Frontend → API Gateway → Services
- Service-to-service calls for critical operations

**Asynchronous:** RabbitMQ (for notifications, confirmations)
- Booking confirmed → Payment service
- Payment success → Notification service
- Reduces coupling and improves resilience

---

### 4. Scalability Features

- **Horizontal scaling** for booking service (most critical)
- **Database connection pooling** (SQLAlchemy with pool size tuning)
- **Redis caching** for train/seat data (reduce DB load)
- **Rate limiting** at API gateway (prevent abuse)
- **Stateless services** (JWT tokens, no session storage)
- **Load balancing** across service instances
- **Database indexing** on frequently queried columns

---

### 5. API Gateway Configuration

**Nginx example:**
```nginx
upstream auth_service {
    server auth-service:5001;
}

upstream booking_service {
    server booking-service-1:5002;
    server booking-service-2:5002;
    server booking-service-3:5002;
}

server {
    listen 80;
    
    location /api/auth/ {
        proxy_pass http://auth_service/;
    }
    
    location /api/bookings/ {
        proxy_pass http://booking_service/;
        limit_req zone=booking_limit burst=10;
    }
}
```

---

## Microservices Architecture

```
┌─────────────┐
│   Frontend  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  API Gateway    │
│  (Nginx/Traefik)│
└────────┬────────┘
         │
    ┌────┴────┬────────┬──────────┬──────────┐
    ▼         ▼        ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│  Auth  │ │ Train  │ │Booking │ │Payment │ │ Notify │
│Service │ │Service │ │Service │ │Service │ │Service │
└───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘
    │          │          │          │          │
    └──────────┴──────────┴──────────┴──────────┘
                         │
                    ┌────┴────┐
                    │         │
                ┌───▼───┐ ┌──▼──┐
                │ Redis │ │ MQ  │
                └───────┘ └─────┘
                    │
                ┌───▼────┐
                │Postgres│
                └────────┘
```

---

## Docker Compose Structure

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"

  auth-service:
    build: ./services/auth-service
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/auth_db
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis

  train-service:
    build: ./services/train-service
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/train_db
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis

  booking-service:
    build: ./services/booking-service
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/booking_db
      REDIS_URL: redis://redis:6379
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672
    depends_on:
      - postgres
      - redis
      - rabbitmq
    deploy:
      replicas: 3

  payment-service:
    build: ./services/payment-service
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/payment_db
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672
    depends_on:
      - postgres
      - rabbitmq

  notification-service:
    build: ./services/notification-service
    environment:
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672
    depends_on:
      - rabbitmq

  api-gateway:
    image: nginx:alpine
    volumes:
      - ./services/api-gateway/nginx.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"
    depends_on:
      - auth-service
      - train-service
      - booking-service
      - payment-service

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - api-gateway

volumes:
  postgres_data:
```

---

## CI/CD Pipeline

### GitHub Actions - CI Workflow

```yaml
name: CI Pipeline

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      auth: ${{ steps.changes.outputs.auth }}
      train: ${{ steps.changes.outputs.train }}
      booking: ${{ steps.changes.outputs.booking }}
      payment: ${{ steps.changes.outputs.payment }}
      notification: ${{ steps.changes.outputs.notification }}
    steps:
      - uses: actions/checkout@v3
      - uses: dorny/paths-filter@v2
        id: changes
        with:
          filters: |
            auth:
              - 'services/auth-service/**'
            train:
              - 'services/train-service/**'
            booking:
              - 'services/booking-service/**'
            payment:
              - 'services/payment-service/**'
            notification:
              - 'services/notification-service/**'

  test-auth:
    needs: detect-changes
    if: needs.detect-changes.outputs.auth == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          cd services/auth-service
          pip install -r requirements.txt
          pytest

  test-booking:
    needs: detect-changes
    if: needs.detect-changes.outputs.booking == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          cd services/booking-service
          pip install -r requirements.txt
          pytest

  # Similar jobs for other services...
```

### GitHub Actions - CD Workflow

```yaml
name: CD Pipeline

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build and push Docker images
        run: |
          docker build -t registry/auth-service:${{ github.sha }} ./services/auth-service
          docker push registry/auth-service:${{ github.sha }}
      
      - name: Deploy to cloud
        run: |
          # kubectl apply or docker-compose commands
          # Rolling update strategy
```

---

## Load Testing Strategy

### Test Scenario

**System Configuration:**
- Number of trains: 5
- Number of coaches per train: 5
- Number of seats per coach: 55
- Total seats: 1,375

**Load Test Parameters:**
- Concurrent users: Start at 100, increase to 10,000
- Test duration: 5 minutes per level
- Ramp-up time: 30 seconds

### Critical Endpoints to Test

1. **Seat Selection** (MANDATORY - Breakpoint Testing)
   - POST /api/bookings/seats/select
   - Expected: Handle 1000+ concurrent requests per seat

2. **Train Search** (Bonus)
   - GET /api/trains/search
   
3. **Login/Auth** (Bonus)
   - POST /api/auth/login

### Locust Test Script

```python
from locust import HttpUser, task, between
import random

class TrainBookingUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login
        response = self.client.post("/api/auth/login", json={
            "email": f"user{random.randint(1, 10000)}@test.com",
            "password": "password123"
        })
        self.token = response.json().get("token")
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(5)
    def search_trains(self):
        self.client.get("/api/trains/search?from=Dhaka&to=Chittagong", 
                       headers=self.headers)
    
    @task(10)
    def select_seat(self):
        train_id = random.randint(1, 5)
        coach_id = random.randint(1, 25)
        seat_id = random.randint(1, 1375)
        
        response = self.client.post("/api/bookings/seats/select", 
            json={
                "seat_id": seat_id,
                "train_id": train_id
            },
            headers=self.headers,
            name="/api/bookings/seats/select"
        )
        
        if response.status_code == 200:
            booking_id = response.json().get("booking_id")
            # Simulate OTP verification
            self.client.post(f"/api/bookings/{booking_id}/verify-otp",
                json={"otp": "123456"},
                headers=self.headers
            )
    
    @task(3)
    def view_booking(self):
        booking_id = random.randint(1, 1000)
        self.client.get(f"/api/bookings/{booking_id}", 
                       headers=self.headers)
```

### Metrics to Collect

- **Throughput:** Requests per second
- **Response Time:** p50, p95, p99 latency
- **Error Rate:** Percentage of failed requests
- **Concurrent Users:** Maximum supported
- **Seat Booking Success Rate:** Critical metric
- **Database Connection Pool Usage**
- **CPU and Memory Usage**

---

## Risk Mitigation

### Biggest Risks

1. **Seat double-booking**
   - **Solution:** Implement proper locking mechanism from the start (Redis locks)
   - **Test:** Write specific tests for concurrent seat selection

2. **CI/CD taking too long**
   - **Solution:** Keep it simple, test locally first
   - **Fallback:** Manual deployment if CI/CD fails

3. **Load testing infrastructure**
   - **Solution:** Use cloud-based load testing tools (Locust on separate VMs)
   - **Fallback:** Reduce concurrent users if infrastructure can't handle

4. **Integration issues**
   - **Solution:** Start integration early (hour 8)
   - **Strategy:** Test each service independently first

5. **Time management**
   - **Solution:** Stick to timeline, skip bonus features if needed
   - **Priority:** Core booking flow > Everything else

---

## What to Skip if Running Out of Time

**Priority order (skip from bottom):**

1. ✅ Core booking flow (NEVER SKIP)
2. ✅ Basic frontend (NEVER SKIP)
3. ✅ Docker compose (NEVER SKIP)
4. ✅ Load testing on seat selection (NEVER SKIP)
5. ⚠️ CI/CD pipeline (simplify if needed)
6. ⚠️ Cloud deployment (can demo locally)
7. ❌ Beautiful frontend (use basic HTML forms)
8. ❌ Integration tests (focus on unit tests)
9. ❌ Infrastructure as Code
10. ❌ Advanced monitoring (Prometheus/Grafana)
11. ❌ Payment service complexity (just mock it)
12. ❌ Notification service (just log to console)

---

## Final Checklist

### Must Have (Core Requirements)
- [ ] All services dockerized
- [ ] docker-compose.yml works on fresh machine
- [ ] Seat selection with proper locking mechanism
- [ ] Basic frontend demonstrating full flow
- [ ] Load testing on seat selection endpoint
- [ ] Load testing results documented
- [ ] Architecture diagram complete
- [ ] Unit tests for critical services
- [ ] README with setup instructions

### Should Have (Important)
- [ ] CI/CD pipeline functional
- [ ] At least one service deployed to cloud
- [ ] API Gateway with rate limiting
- [ ] Event-driven communication (RabbitMQ)
- [ ] Redis caching implemented
- [ ] Presentation slides ready
- [ ] Demo video recorded

### Nice to Have (Bonus)
- [ ] Prometheus + Grafana monitoring
- [ ] Infrastructure as Code (Terraform)
- [ ] Kubernetes orchestration
- [ ] Load testing on multiple endpoints
- [ ] Integration tests
- [ ] Zero-downtime deployment strategy

---

## Presentation Structure

### Slide Breakdown (10-15 slides)

1. **Title Slide**
   - Team name, members, hackathon details

2. **Problem Statement**
   - Eid ticket rush statistics
   - Current system failures
   - User pain points

3. **Solution Overview**
   - Microservices architecture
   - Key technologies
   - Scalability approach

4. **Architecture Diagram**
   - Visual representation of all services
   - Data flow
   - Communication patterns

5. **Key Technical Decisions**
   - Seat locking mechanism
   - Event-driven architecture
   - Caching strategy

6. **Microservices Breakdown**
   - Brief description of each service
   - API endpoints
   - Responsibilities

7. **Database Design**
   - ER diagram or schema
   - Indexing strategy

8. **DevOps Pipeline**
   - CI/CD workflow diagram
   - Deployment strategy
   - Auto-scaling configuration

9. **Load Testing Setup**
   - Test scenarios
   - Infrastructure used
   - Methodology

10. **Load Testing Results**
    - Graphs and charts
    - Throughput metrics
    - Response times
    - Breakpoint analysis

11. **Monitoring & Observability**
    - Prometheus metrics
    - Grafana dashboards
    - Key performance indicators

12. **Challenges Faced**
    - Technical challenges
    - How they were solved
    - Lessons learned

13. **Demo**
    - Live demo or video
    - Show complete booking flow
    - Highlight scalability features

14. **Future Improvements**
    - What could be added
    - Scalability enhancements
    - Additional features

15. **Q&A**
    - Thank you slide
    - GitHub repo link

---

## Quick Reference Commands

### Docker Commands
```bash
# Build all services
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f booking-service

# Scale a service
docker-compose up -d --scale booking-service=5

# Stop all services
docker-compose down
```

### Database Setup
```bash
# Create databases
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE auth_db;"
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE train_db;"
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE booking_db;"

# Run migrations
docker-compose exec booking-service flask db upgrade
```

### Load Testing
```bash
# Install Locust
pip install locust

# Run load test
locust -f load-testing/locustfile.py --host=http://localhost:80

# Headless mode
locust -f load-testing/locustfile.py --host=http://localhost:80 \
  --users 1000 --spawn-rate 100 --run-time 5m --headless
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/booking-service

# Commit and push
git add .
git commit -m "feat: implement seat locking mechanism"
git push origin feature/booking-service

# Create PR (triggers CI)
# Merge to main (triggers CD)
```

---

## Success Criteria

### Minimum Viable Product (MVP)
- User can search for trains
- User can select a seat (with proper locking)
- User can complete booking flow
- System handles at least 500 concurrent seat selections
- All services run via docker-compose
- Basic CI pipeline exists

### Good Implementation
- All of MVP +
- System handles 2000+ concurrent seat selections
- Services deployed to cloud
- CD pipeline with rolling updates
- Monitoring dashboard
- Comprehensive load testing results

### Excellent Implementation
- All of Good +
- System handles 5000+ concurrent seat selections
- Infrastructure as Code
- Kubernetes orchestration
- Multiple load testing scenarios
- Zero-downtime deployment
- Creative optimizations

---

## Emergency Contacts & Resources

### Documentation Links
- Flask: https://flask.palletsprojects.com/
- PostgreSQL: https://www.postgresql.org/docs/
- Redis: https://redis.io/docs/
- RabbitMQ: https://www.rabbitmq.com/documentation.html
- Docker: https://docs.docker.com/
- Locust: https://docs.locust.io/

### Quick Troubleshooting
- **Services can't connect:** Check docker-compose network configuration
- **Database connection errors:** Verify DATABASE_URL and wait for postgres to be ready
- **OOM errors during load test:** Reduce concurrent users or increase resources
- **CI pipeline failing:** Check test dependencies and environment variables
- **Seat double-booking:** Verify Redis locks are working correctly

---

## Final Tips

1. **Start with the hardest part first:** Seat locking mechanism
2. **Test early, test often:** Don't wait until the end
3. **Keep it simple:** KISS principle applies everywhere
4. **Document as you go:** Update README continuously
5. **Communication is key:** Regular sync-ups between team members
6. **Have a backup plan:** Record demo video in case live demo fails
7. **Time management:** Set alarms for each milestone
8. **Don't over-engineer:** Focus on working solution first
9. **Sleep is optional:** But coffee is mandatory ☕
10. **Have fun:** It's a hackathon, enjoy the process!

---

**Good luck with your hackathon! 🚂🎉**
