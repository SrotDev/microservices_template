import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'

const SearchTrains = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const [trains, setTrains] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadTrains()
  }, [])

  const loadTrains = async () => {
    // Simulate API delay
    setTimeout(() => {
      // Mock train data
      const mockTrains = [
        {
          id: 1,
          name: 'Suborno Express',
          from: 'Dhaka',
          to: 'Chittagong',
          departure: '08:00 AM',
          arrival: '02:30 PM',
          duration: '6h 30m',
          price: 550,
          availableSeats: 45
        },
        {
          id: 2,
          name: 'Turna Nishitha',
          from: 'Dhaka',
          to: 'Chittagong',
          departure: '11:00 PM',
          arrival: '06:00 AM',
          duration: '7h 00m',
          price: 600,
          availableSeats: 32
        },
        {
          id: 3,
          name: 'Mohanagar Godhuli',
          from: 'Dhaka',
          to: 'Chittagong',
          departure: '03:30 PM',
          arrival: '10:00 PM',
          duration: '6h 30m',
          price: 580,
          availableSeats: 28
        }
      ]
      setTrains(mockTrains)
      setLoading(false)
    }, 500)
  }

  const handleSelectTrain = (trainId) => {
    navigate(`/seats/${trainId}`)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Available Trains</h1>
        <p className="text-gray-600">
          {location.state?.from} → {location.state?.to} | {location.state?.date}
        </p>
      </div>

      <div className="space-y-4">
        {trains.map((train) => (
          <div key={train.id} className="card hover:shadow-lg transition-all">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div className="flex-1">
                <h3 className="text-xl font-bold text-gray-900 mb-2">{train.name}</h3>
                <div className="flex items-center gap-6 text-sm text-gray-600">
                  <div>
                    <p className="font-medium text-gray-900">{train.departure}</p>
                    <p>{train.from}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="h-px w-12 bg-gray-300"></div>
                    <span className="text-xs">{train.duration}</span>
                    <div className="h-px w-12 bg-gray-300"></div>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{train.arrival}</p>
                    <p>{train.to}</p>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-right">
                  <p className="text-2xl font-bold text-primary-600">৳{train.price}</p>
                  <p className="text-sm text-gray-500">{train.availableSeats} seats left</p>
                </div>
                <button
                  onClick={() => handleSelectTrain(train.id)}
                  className="btn-primary"
                  disabled={train.availableSeats === 0}
                >
                  Select
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default SearchTrains
