import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../utils/AuthContext'

const Dashboard = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [searchData, setSearchData] = useState({
    from: 'Dhaka',
    to: 'Chittagong',
    date: new Date().toISOString().split('T')[0]
  })

  const handleSearch = (e) => {
    e.preventDefault()
    navigate('/search', { state: searchData })
  }

  const popularRoutes = [
    { from: 'Dhaka', to: 'Chittagong', trains: 12 },
    { from: 'Dhaka', to: 'Sylhet', trains: 8 },
    { from: 'Dhaka', to: 'Rajshahi', trains: 6 },
    { from: 'Chittagong', to: 'Sylhet', trains: 4 },
  ]

  const handleRouteClick = (route) => {
    const routeData = {
      from: route.from,
      to: route.to,
      date: new Date().toISOString().split('T')[0]
    }
    navigate('/search', { state: routeData })
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      {/* Hero Section */}
      <div className="text-center mb-12 animate-fade-in">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Welcome, {user?.name}! 👋
        </h1>
        <p className="text-lg text-gray-600">
          Book your train tickets in seconds
        </p>
      </div>

      {/* Search Card */}
      <div className="max-w-3xl mx-auto mb-12 animate-slide-up">
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Search Trains</h2>
          <form onSubmit={handleSearch} className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">From</label>
                <select
                  value={searchData.from}
                  onChange={(e) => setSearchData({ ...searchData, from: e.target.value })}
                  className="input-field"
                >
                  <option>Dhaka</option>
                  <option>Chittagong</option>
                  <option>Sylhet</option>
                  <option>Rajshahi</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">To</label>
                <select
                  value={searchData.to}
                  onChange={(e) => setSearchData({ ...searchData, to: e.target.value })}
                  className="input-field"
                >
                  <option>Chittagong</option>
                  <option>Dhaka</option>
                  <option>Sylhet</option>
                  <option>Rajshahi</option>
                </select>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Date</label>
              <input
                type="date"
                value={searchData.date}
                onChange={(e) => setSearchData({ ...searchData, date: e.target.value })}
                className="input-field"
                min={new Date().toISOString().split('T')[0]}
              />
            </div>
            <button type="submit" className="btn-primary w-full">
              Search Trains
            </button>
          </form>
        </div>
      </div>

      {/* Popular Routes */}
      <div className="max-w-4xl mx-auto">
        <h3 className="text-xl font-bold text-gray-900 mb-6">Popular Routes</h3>
        <div className="grid md:grid-cols-2 gap-4">
          {popularRoutes.map((route, index) => (
            <div 
              key={index} 
              onClick={() => handleRouteClick(route)}
              className="card hover:border-primary-300 cursor-pointer transition-all hover:shadow-lg"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-semibold text-gray-900">{route.from} → {route.to}</p>
                  <p className="text-sm text-gray-500">{route.trains} trains available</p>
                </div>
                <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
