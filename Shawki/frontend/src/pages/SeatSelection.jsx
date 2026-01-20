import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'

const SeatSelection = () => {
  const { trainId } = useParams()
  const navigate = useNavigate()
  const [seats, setSeats] = useState([])
  const [selectedSeats, setSelectedSeats] = useState([])
  const [loading, setLoading] = useState(true)
  const [booking, setBooking] = useState(false)

  useEffect(() => {
    loadSeats()
  }, [trainId])

  const loadSeats = async () => {
    // Simulate API delay
    setTimeout(() => {
      // Generate mock seats (5 rows x 11 columns = 55 seats)
      const mockSeats = []
      const rows = ['A', 'B', 'C', 'D', 'E']
      for (let row of rows) {
        for (let col = 1; col <= 11; col++) {
          const seatNumber = `${row}${col}`
          // Randomly mark some seats as booked
          const isBooked = Math.random() > 0.7
          mockSeats.push({
            id: mockSeats.length + 1,
            number: seatNumber,
            status: isBooked ? 'booked' : 'available',
            price: 550
          })
        }
      }
      setSeats(mockSeats)
      setLoading(false)
    }, 500)
  }

  const handleSeatClick = (seat) => {
    if (seat.status === 'booked') {
      toast.error('This seat is already booked')
      return
    }
    
    // Toggle seat selection
    const isSelected = selectedSeats.find(s => s.id === seat.id)
    if (isSelected) {
      setSelectedSeats(selectedSeats.filter(s => s.id !== seat.id))
    } else {
      // Limit to 4 seats per booking
      if (selectedSeats.length >= 4) {
        toast.error('Maximum 4 seats can be selected at once')
        return
      }
      setSelectedSeats([...selectedSeats, seat])
    }
  }

  const handleBookSeats = async () => {
    if (selectedSeats.length === 0) return
    
    setBooking(true)
    
    // Simulate API delay
    setTimeout(() => {
      // Generate mock booking ID
      const mockBookingId = Math.floor(Math.random() * 10000) + 1
      toast.success(`${selectedSeats.length} seat(s) reserved! Complete booking within 5 minutes`)
      navigate(`/booking/${mockBookingId}`, { state: { seats: selectedSeats } })
      setBooking(false)
    }, 500)
  }

  const getTotalPrice = () => {
    return selectedSeats.reduce((total, seat) => total + seat.price, 0)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Select Your Seat(s)</h1>
        <p className="text-gray-600">Click on available seats to select (up to 4 seats)</p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Seat Map */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="grid grid-cols-5 gap-3">
              {seats.map((seat) => (
                <button
                  key={seat.id}
                  onClick={() => handleSeatClick(seat)}
                  disabled={seat.status === 'booked'}
                  className={`
                    aspect-square rounded-lg font-medium text-sm transition-all
                    ${seat.status === 'booked' 
                      ? 'bg-gray-200 text-gray-400 cursor-not-allowed' 
                      : selectedSeats.find(s => s.id === seat.id)
                      ? 'bg-primary-600 text-white shadow-lg scale-105'
                      : 'bg-green-100 text-green-700 hover:bg-green-200 hover:scale-105'
                    }
                  `}
                >
                  {seat.number}
                </button>
              ))}
            </div>
          </div>

          {/* Legend */}
          <div className="flex gap-6 mt-6 justify-center">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-green-100 rounded"></div>
              <span className="text-sm text-gray-600">Available</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-primary-600 rounded"></div>
              <span className="text-sm text-gray-600">Selected</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-gray-200 rounded"></div>
              <span className="text-sm text-gray-600">Booked</span>
            </div>
          </div>
        </div>

        {/* Booking Summary */}
        <div>
          <div className="card sticky top-4">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Booking Summary</h3>
            {selectedSeats.length > 0 ? (
              <>
                <div className="space-y-3 mb-6">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Selected Seats</span>
                    <span className="font-medium">
                      {selectedSeats.map(s => s.number).join(', ')}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Quantity</span>
                    <span className="font-medium">{selectedSeats.length} seat(s)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Price per seat</span>
                    <span className="font-medium">৳{selectedSeats[0].price}</span>
                  </div>
                  <div className="border-t pt-3 flex justify-between">
                    <span className="font-bold">Total</span>
                    <span className="font-bold text-primary-600">৳{getTotalPrice()}</span>
                  </div>
                </div>
                <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                  <p className="text-xs text-blue-800">
                    💡 You can select up to 4 seats
                  </p>
                </div>
                <button
                  onClick={handleBookSeats}
                  disabled={booking}
                  className="btn-primary w-full"
                >
                  {booking ? 'Reserving...' : `Reserve ${selectedSeats.length} Seat(s)`}
                </button>
              </>
            ) : (
              <p className="text-gray-500 text-center py-8">Select seat(s) to continue</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default SeatSelection
