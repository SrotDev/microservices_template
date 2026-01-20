# Train Ticketing Frontend

Modern, minimal React frontend for Bangladesh Railway online ticketing system.

## 🎯 Demo Mode (No Backend Required)

The frontend is currently running in **demo mode** with mock data. You can explore all pages without needing any backend services!

### Quick Start

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 and:
- **Login**: Enter any email/password to login
- **Register**: Fill the form with any data
- Navigate through all pages with dummy data

## Features

✨ Clean, modern UI with Tailwind CSS
🎨 Smooth animations and transitions
📱 Fully responsive design
🔐 JWT authentication (mock)
⚡ Fast and lightweight
🎯 Intuitive user experience
🎭 **Demo mode with mock data**

## Tech Stack

- React 18
- Vite
- Tailwind CSS
- React Router v6
- Axios
- React Hot Toast

## Quick Start

### Install Dependencies
```bash
cd frontend
npm install
```

### Run Development Server
```bash
npm run dev
```

Frontend will be available at: http://localhost:3000

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## Environment Variables

Create a `.env` file:
```
VITE_API_URL=http://localhost:5001
```

## Pages

1. **Login** (`/login`) - User authentication
2. **Register** (`/register`) - New user registration
3. **Dashboard** (`/`) - Search trains and popular routes
4. **Search Results** (`/search`) - Available trains
5. **Seat Selection** (`/seats/:trainId`) - Interactive seat map
6. **Booking** (`/booking/:bookingId`) - OTP verification and payment

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Navbar.jsx
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── SearchTrains.jsx
│   │   ├── SeatSelection.jsx
│   │   └── Booking.jsx
│   ├── utils/
│   │   ├── api.js
│   │   └── AuthContext.jsx
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── Dockerfile
```

## Design System

### Colors
- Primary: Blue (#0284c7)
- Success: Green
- Error: Red
- Gray scale for text and backgrounds

### Components
- `btn-primary` - Primary action button
- `btn-secondary` - Secondary action button
- `input-field` - Form input field
- `card` - Content card with shadow

### Animations
- `animate-fade-in` - Fade in effect
- `animate-slide-up` - Slide up effect

## API Integration

The frontend connects to the backend services:

```javascript
// Auth Service
POST /api/auth/register
POST /api/auth/login
POST /api/auth/otp/request
POST /api/auth/otp/verify

// Train Service (mock)
GET /api/trains/search
GET /api/trains/:id/seats

// Booking Service (mock)
POST /api/bookings/seats/select
POST /api/bookings/:id/verify-otp
POST /api/bookings/:id/confirm
```

## Docker

### Build Image
```bash
docker build -t train-frontend .
```

### Run Container
```bash
docker run -p 3000:3000 train-frontend
```

## Features Walkthrough

### 1. Authentication
- Clean login/register forms
- JWT token storage
- Protected routes
- Auto-redirect

### 2. Train Search
- Date picker
- Station selection
- Real-time results

### 3. Seat Selection
- Interactive seat map
- Visual seat status
- Real-time availability
- Instant selection

### 4. Booking Flow
- 5-minute timer
- OTP verification
- Mock payment
- Ticket generation

## Customization

### Change Primary Color

Edit `tailwind.config.js`:
```javascript
colors: {
  primary: {
    // Your color palette
  }
}
```

### Add New Page

1. Create component in `src/pages/`
2. Add route in `src/App.jsx`
3. Add navigation link

## Performance

- Lazy loading for routes
- Optimized bundle size
- Fast page transitions
- Minimal dependencies

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development Tips

### Hot Reload
Vite provides instant hot module replacement

### Debugging
Use React DevTools browser extension

### API Mocking
Mock data is in `src/utils/api.js`

## Production Deployment

### Build
```bash
npm run build
```

### Deploy to Netlify/Vercel
```bash
# Connect your repo and deploy
# Set VITE_API_URL environment variable
```

### Deploy with Docker
```bash
docker build -t train-frontend .
docker run -p 3000:3000 train-frontend
```

## Testing

### Manual Testing Checklist
- [ ] Register new user
- [ ] Login with credentials
- [ ] Search trains
- [ ] Select seat
- [ ] Verify OTP
- [ ] Complete payment
- [ ] View ticket

## Troubleshooting

### Port 3000 in use
Change port in `vite.config.js`

### API connection error
Check VITE_API_URL in .env

### Build errors
Delete node_modules and reinstall

## Future Enhancements

- [ ] Add booking history
- [ ] Add user profile
- [ ] Add payment gateway integration
- [ ] Add real-time seat updates
- [ ] Add mobile app
- [ ] Add PWA support

## License

MIT

## Team

Built for Bangladesh Railway Hackathon 2024
