import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'
import FilterBar from './components/FilterBar.jsx'
import EventTable from './components/EventTable.jsx'

// Use Railway in production, localhost in development
const API_BASE = import.meta.env.MODE === 'production' 
  ? 'https://cultheld-production.up.railway.app/api'
  : 'http://localhost:8000/api'

function App() {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(false)
  const [loadingMore, setLoadingMore] = useState(false)
  const [error, setError] = useState(null)
  const [venues, setVenues] = useState([])
  const [eventTypes, setEventTypes] = useState([])
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('darkMode') === 'true'
  })

  // Pagination state - using offset for infinite scroll
  const [offset, setOffset] = useState(0)
  const [limit, setLimit] = useState(50)
  const [total, setTotal] = useState(0)
  const [hasMore, setHasMore] = useState(true)

  // Filter and search state with default dates (today to today + 7 days)
  const getDefaultDates = () => {
    const today = new Date()
    const nextWeek = new Date(today)
    nextWeek.setDate(today.getDate() + 7)
    
    return {
      start_date: today.toISOString().split('T')[0],
      end_date: nextWeek.toISOString().split('T')[0],
    }
  }

  const [filters, setFilters] = useState({
    venue: '',
    event_type: '',
    ...getDefaultDates(),
  })

  const [searchQuery, setSearchQuery] = useState('')

  // Apply dark mode
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark-mode')
    } else {
      document.documentElement.classList.remove('dark-mode')
    }
    localStorage.setItem('darkMode', darkMode)
  }, [darkMode])

  // Fetch venues and event types on mount
  useEffect(() => {
    const fetchMetadata = async () => {
      try {
        const [venuesRes, typesRes] = await Promise.all([
          axios.get(`${API_BASE}/venues`),
          axios.get(`${API_BASE}/event-types`),
        ])
        setVenues(venuesRes.data.venues)
        setEventTypes(typesRes.data.event_types)
      } catch (err) {
        console.error('Failed to fetch metadata:', err)
      }
    }
    fetchMetadata()
  }, [])

  // Fetch events - reset offset when filters change
  useEffect(() => {
    setOffset(0)
    setEvents([])
    setHasMore(true)
  }, [filters, searchQuery])

  // Fetch events when offset changes
  useEffect(() => {
    const fetchEvents = async () => {
      if (offset === 0) {
        setLoading(true)
      } else {
        setLoadingMore(true)
      }
      setError(null)
      try {
        const params = {
          offset,
          limit,
          search: searchQuery,
          ...Object.fromEntries(
            Object.entries(filters).filter(([, v]) => v !== '')
          ),
        }
        const response = await axios.get(`${API_BASE}/events`, { params })
        
        if (offset === 0) {
          setEvents(response.data.events)
        } else {
          setEvents(prev => [...prev, ...response.data.events])
        }
        
        setTotal(response.data.total)
        setHasMore(offset + limit < response.data.total)
      } catch (err) {
        setError('Failed to fetch events. Make sure the backend is running.')
        console.error(err)
      } finally {
        setLoading(false)
        setLoadingMore(false)
      }
    }
    fetchEvents()
  }, [offset])

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters)
  }

  const handleResetFilters = () => {
    setFilters({
      venue: '',
      event_type: '',
      start_date: '',
      end_date: '',
    })
    setSearchQuery('')
  }

  const handleSearchChange = (query) => {
    setSearchQuery(query)
  }

  const handleLoadMore = () => {
    setOffset(prev => prev + limit)
  }

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
  }

  return (
    <div className={`app ${darkMode ? 'dark-mode' : ''}`}>
      <header className="app-header">
        <div className="header-content">
          <div>
            <h1>🎭 CultHeld Events</h1>
            <p>Browse cultural events in Amsterdam</p>
          </div>
          <button 
            className="dark-mode-toggle"
            onClick={toggleDarkMode}
            title={darkMode ? 'Light mode' : 'Dark mode'}
          >
            {darkMode ? '☀️' : '🌙'}
          </button>
        </div>
      </header>

      <main className="app-main">
        <FilterBar
          venues={venues}
          eventTypes={eventTypes}
          filters={filters}
          onFilterChange={handleFilterChange}
          onResetFilters={handleResetFilters}
          onSearchChange={handleSearchChange}
          searchQuery={searchQuery}
        />

        {error && <div className="error-message">{error}</div>}

        {loading && <div className="loading">Loading events...</div>}

        {!loading && (
          <>
            <div className="results-info">
              Showing {events.length} of {total} events
            </div>
            <EventTable 
              events={events}
              onLoadMore={handleLoadMore}
              hasMore={hasMore}
              isLoading={loadingMore}
            />

            {/* Load More Button */}
            {hasMore && !loadingMore && (
              <div className="load-more-container">
                <button 
                  className="btn-load-more"
                  onClick={handleLoadMore}
                >
                  Load More Events
                </button>
              </div>
            )}

            {loadingMore && (
              <div className="loading-more">Loading more events...</div>
            )}
          </>
        )}
      </main>
    </div>
  )
}

export default App
