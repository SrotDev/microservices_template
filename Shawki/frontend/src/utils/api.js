import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth API
export const authAPI = {
  register: (data) => api.post('/api/auth/register', data),
  login: (data) => api.post('/api/auth/login', data),
  getMe: () => api.get('/api/auth/me'),
  requestOTP: (phone) => api.post('/api/auth/otp/request', { phone }),
  verifyOTP: (phone, otp) => api.post('/api/auth/otp/verify', { phone, otp }),
}

// Train API (mock for now)
export const trainAPI = {
  search: (from, to, date) => {
    // Mock data - replace with actual API call
    return Promise.resolve({
      data: {
        trains: [
          {
            id: 1,
            name: 'Suborno Express',
            from: 'Dhaka',
            to: 'Chittagong',
            departure: '08:00 AM',
            arrival: '02:30 PM',
            duration: '6h 30m',
            availableSeats: 45,
            price: 550
          },
          {
            id: 2,
            name: 'Turna Nishitha',
            from: 'Dhaka',
            to: 'Chittagong',
            departure: '11:00 PM',
            arrival: '06:00 AM',
            duration: '7h 00m',
            availableSeats: 32,
            price: 600
          },
          {
            id: 3,
            name: 'Mohanagar Godhuli',
            from: 'Dhaka',
            to: 'Chittagong',
            departure: '03:00 PM',
            arrival: '09:45 PM',
            duration: '6h 45m',
            availableSeats: 18,
            price: 580
          },
        ]
      }
    })
  },
  getSeats: (trainId) => {
    // Mock seat data
    const seats = []
    for (let i = 1; i <= 55; i++) {
      seats.push({
        id: i,
        number: `A${i}`,
        status: Math.random() > 0.3 ? 'available' : 'booked',
        price: 550
      })
    }
    return Promise.resolve({ data: { seats } })
  }
}

// Booking API (mock for now)
export const bookingAPI = {
  selectSeat: (seatId) => {
    return Promise.resolve({
      data: {
        booking_id: Math.floor(Math.random() * 10000),
        seat_id: seatId,
        status: 'pending',
        expires_at: new Date(Date.now() + 5 * 60 * 1000).toISOString()
      }
    })
  },
  verifyOTP: (bookingId, otp) => {
    return Promise.resolve({
      data: { verified: true }
    })
  },
  confirmBooking: (bookingId) => {
    return Promise.resolve({
      data: {
        booking_id: bookingId,
        status: 'confirmed',
        ticket_number: `TKT${Math.floor(Math.random() * 100000)}`,
        qr_code: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
      }
    })
  }
}

export default api
