# ✅ Auth System Setup Checklist

## Pre-requisites
- [ ] Docker Desktop installed and running
- [ ] Node.js installed (v16+)
- [ ] npm installed

---

## Step 1: Start Auth Service

### Commands
```bash
cd services/auth-service
docker-compose up --build
```

### Verify
- [ ] See "Database tables created successfully!"
- [ ] No error messages in logs
- [ ] Containers running: `docker ps`

### Expected Output
```
auth-service    | Database tables created successfully!
auth-service    | [INFO] Starting gunicorn 21.2.0
auth-service    | [INFO] Listening at: http://0.0.0.0:5001
```

---

## Step 2: Test Auth Service

### Health Check
```bash
curl http://localhost:5001/health
```

**Expected:** `{"status":"healthy"}`

- [ ] Health check returns success

### Register User
```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Masum Ahmed","email":"masum@example.com","phone":"01712345678","password":"password123"}'
```

**Expected:** Returns user object with token

- [ ] Registration successful
- [ ] Received JWT token
- [ ] User ID returned

### Login User
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"masum@example.com","password":"password123"}'
```

**Expected:** Returns user object with token

- [ ] Login successful
- [ ] Received JWT token
- [ ] User details returned

---

## Step 3: Start Frontend

### Commands
```bash
cd frontend
npm install
npm run dev
```

### Verify
- [ ] No npm errors
- [ ] Server starts on port 3000
- [ ] Browser opens automatically

### Expected Output
```
VITE v5.0.8  ready in 500 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

---

## Step 4: Test Frontend

### Open Browser
- [ ] Navigate to http://localhost:3000
- [ ] Page loads without errors
- [ ] See login page

### Register New User
1. [ ] Click "Register here"
2. [ ] Fill form:
   - Name: Test User
   - Email: test@example.com
   - Phone: 01712345678
   - Password: password123
   - Confirm: password123
3. [ ] Click "Create Account"
4. [ ] See success toast
5. [ ] Redirected to dashboard
6. [ ] See "Welcome, Test User!"

### Logout and Login
1. [ ] Click "Logout" button
2. [ ] Redirected to login page
3. [ ] Enter credentials:
   - Email: test@example.com
   - Password: password123
4. [ ] Click "Login"
5. [ ] See success toast
6. [ ] Redirected to dashboard

### Test Navigation
- [ ] Dashboard loads
- [ ] Can search trains
- [ ] Can view search results (mock data)
- [ ] Can select seats (mock data)
- [ ] Can complete booking (mock data)

---

## Step 5: Verify Integration

### Check Browser Console
- [ ] Open DevTools (F12)
- [ ] Go to Console tab
- [ ] No error messages
- [ ] See successful API calls

### Check Network Tab
1. [ ] Open DevTools → Network tab
2. [ ] Login again
3. [ ] See POST request to `http://localhost:5001/api/auth/login`
4. [ ] Status: 200 OK
5. [ ] Response contains token and user

### Check Local Storage
1. [ ] Open DevTools → Application tab
2. [ ] Go to Local Storage → http://localhost:3000
3. [ ] See `token` key with JWT value
4. [ ] See `user` key with user JSON

---

## Troubleshooting

### Issue: Port 5001 in use
```bash
# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5001 | xargs kill -9
```
- [ ] Port freed
- [ ] Restart auth service

### Issue: Docker not starting
- [ ] Docker Desktop is running
- [ ] No other containers using ports
- [ ] Try: `docker-compose down -v` then `docker-compose up --build`

### Issue: Frontend can't connect
- [ ] Check `frontend/.env` has `VITE_API_URL=http://localhost:5001`
- [ ] Auth service is running
- [ ] No CORS errors in console
- [ ] Restart frontend: `npm run dev`

### Issue: Login fails
- [ ] User is registered first
- [ ] Password is correct
- [ ] Check auth service logs: `docker-compose logs auth-service`
- [ ] Try registering a new user

### Issue: Database errors
```bash
cd services/auth-service
docker-compose down -v
docker-compose up --build
```
- [ ] Database reset
- [ ] Tables created
- [ ] Register user again

---

## Success Criteria

### Backend
- [x] Auth service running on port 5001
- [x] PostgreSQL running on port 5432
- [x] Health check passes
- [x] Can register users
- [x] Can login users
- [x] JWT tokens generated
- [x] Passwords hashed

### Frontend
- [x] Frontend running on port 3000
- [x] Can register via UI
- [x] Can login via UI
- [x] Token stored in localStorage
- [x] Protected routes work
- [x] User name displayed
- [x] Can logout

### Integration
- [x] Frontend connects to backend
- [x] API calls successful
- [x] CORS working
- [x] Authentication flow complete
- [x] Session persists on refresh

---

## Final Verification

Run all tests:
```bash
# Test auth service
curl http://localhost:5001/health

# Test registration
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Final Test","email":"final@test.com","phone":"01712345678","password":"test123"}'

# Test login
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"final@test.com","password":"test123"}'
```

- [ ] All API tests pass
- [ ] Frontend works end-to-end
- [ ] No errors in logs
- [ ] Ready for next service

---

## 🎉 Completion

If all checkboxes are checked, your authentication system is:
- ✅ Fully operational
- ✅ Dockerized
- ✅ Connected to frontend
- ✅ Production-ready
- ✅ Ready for integration with other services

**Congratulations! Time to build the Train Service!** 🚂
