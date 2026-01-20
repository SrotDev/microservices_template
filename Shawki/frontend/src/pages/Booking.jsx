import { useState, useEffect } from 'react'
import { useParams, useLocation } from 'react-router-dom'
import { useAuth } from '../utils/AuthContext'
import toast from 'react-hot-toast'

const Booking = () => {
  const { bookingId } = useParams()
  const location = useLocation()
  const { user } = useAuth()
  const [step, setStep] = useState(1) // 1: OTP, 2: Payment, 3: Confirmed
  const [otp, setOtp] = useState('')
  const [timeLeft, setTimeLeft] = useState(300) // 5 minutes
  const [loading, setLoading] = useState(false)
  const [ticket, setTicket] = useState(null)
  
  // Get seats from navigation state or use default
  const bookedSeats = location.state?.seats || [{ number: 'A12', price: 550 }]
  const totalAmount = bookedSeats.reduce((sum, seat) => sum + seat.price, 0)

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => (prev > 0 ? prev - 1 : 0))
    }, 1000)
    return () => clearInterval(timer)
  }, [])

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const handleRequestOTP = async () => {
    // Mock OTP request
    toast.success(`OTP sent to ${user.phone}`)
    toast.success(`Test OTP: 123456`, { duration: 5000 })
  }

  const handleVerifyOTP = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    // Simulate API delay
    setTimeout(() => {
      // Accept any OTP
      toast.success('OTP verified!')
      setStep(2)
      setLoading(false)
    }, 500)
  }

  const handlePayment = async () => {
    setLoading(true)
    
    // Simulate API delay
    setTimeout(() => {
      // Mock ticket data
      const mockTicket = {
        ticket_number: 'TKT' + Date.now(),
        booking_id: bookingId,
        status: 'Confirmed'
      }
      setTicket(mockTicket)
      toast.success('Booking confirmed!')
      setStep(3)
      setLoading(false)
    }, 1000)
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-12">
      {/* Timer */}
      {step < 3 && (
        <div className="mb-8 text-center">
          <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full ${
            timeLeft < 60 ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'
          }`}>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="font-medium">Time remaining: {formatTime(timeLeft)}</span>
          </div>
        </div>
      )}

      {/* Step 1: OTP Verification */}
      {step === 1 && (
        <div className="card animate-slide-up">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Verify OTP</h2>
          <p className="text-gray-600 mb-6">
            Enter the OTP sent to {user?.phone}
          </p>
          <form onSubmit={handleVerifyOTP} className="space-y-4">
            <div>
              <input
                type="text"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                className="input-field text-center text-2xl tracking-widest"
                placeholder="000000"
                maxLength={6}
                required
              />
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full">
              {loading ? 'Verifying...' : 'Verify OTP'}
            </button>
            <button
              type="button"
              onClick={handleRequestOTP}
              className="btn-secondary w-full"
            >
              Resend OTP
            </button>
          </form>
        </div>
      )}

      {/* Step 2: Payment */}
      {step === 2 && (
        <div className="card animate-slide-up">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Payment</h2>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <p className="text-sm text-blue-800">
              💳 Mock Payment - Click confirm to complete booking
            </p>
          </div>
          <div className="space-y-3 mb-6">
            <div className="flex justify-between">
              <span className="text-gray-600">Booking ID</span>
              <span className="font-medium">#{bookingId}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Seat(s)</span>
              <span className="font-medium">{bookedSeats.map(s => s.number).join(', ')}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Quantity</span>
              <span className="font-medium">{bookedSeats.length} seat(s)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Price per seat</span>
              <span className="font-medium">৳{bookedSeats[0].price}</span>
            </div>
            <div className="border-t pt-3 flex justify-between">
              <span className="font-bold text-lg">Total Amount</span>
              <span className="font-bold text-lg text-primary-600">৳{totalAmount}</span>
            </div>
          </div>
          <button
            onClick={handlePayment}
            disabled={loading}
            className="btn-primary w-full"
          >
            {loading ? 'Processing...' : 'Confirm Payment'}
          </button>
        </div>
      )}

      {/* Step 3: Confirmed */}
      {step === 3 && ticket && (
        <div className="card animate-slide-up text-center">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-12 h-12 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Booking Confirmed!</h2>
          <p className="text-gray-600 mb-8">
            {bookedSeats.length === 1 
              ? 'Your ticket has been booked successfully' 
              : `${bookedSeats.length} tickets have been booked successfully`}
          </p>
          
          <div className="bg-gray-50 rounded-lg p-6 mb-6 text-left">
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Ticket Number</span>
                <span className="font-bold">{ticket.ticket_number}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Booking ID</span>
                <span className="font-medium">#{ticket.booking_id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Seat(s)</span>
                <span className="font-medium">{bookedSeats.map(s => s.number).join(', ')}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Total Amount</span>
                <span className="font-bold text-primary-600">৳{totalAmount}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Status</span>
                <span className="text-green-600 font-medium">Confirmed</span>
              </div>
            </div>
          </div>

          <button onClick={() => window.print()} className="btn-primary w-full">
            Download Ticket{bookedSeats.length > 1 ? 's' : ''}
          </button>
        </div>
      )}
    </div>
  )
}

export default Booking
