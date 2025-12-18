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
  const [error, setError] = useState(null)
  const [venues, setVenues] = useState([])
  const [eventTypes, setEventTypes] = useState([])

  // Pagination state
  const [page, setPage] = useState(1)
  const [limit, setLimit] = useState(50)
  const [total, setTotal] = useState(0)

  // Filter state with default dates (today to today + 7 days)
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

  // Fetch events when filters or page changes
  useEffect(() => {
    const fetchEvents = async () => {
      setLoading(true)
      setError(null)
      try {
        const params = {
          page,
          limit,
          ...Object.fromEntries(
            Object.entries(filters).filter(([, v]) => v !== '')
          ),
        }
        const response = await axios.get(`${API_BASE}/events`, { params })
        setEvents(response.data.events)
        setTotal(response.data.total)
      } catch (err) {
        setError('Failed to fetch events. Make sure the backend is running.')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchEvents()
  }, [filters, page, limit])

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters)
    setPage(1) // Reset to first page on filter change
  }

  const handleResetFilters = () => {
    setFilters({
      venue: '',
      event_type: '',
      start_date: '',
      end_date: '',
    })
    setPage(1)
  }

  const totalPages = Math.ceil(total / limit)

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎭 CultHeld Events</h1>
        <p>Browse cultural events in Amsterdam</p>
      </header>

      <main className="app-main">
        <FilterBar
          venues={venues}
          eventTypes={eventTypes}
          filters={filters}
          onFilterChange={handleFilterChange}
          onResetFilters={handleResetFilters}
        />

        {error && <div className="error-message">{error}</div>}

        {loading && <div className="loading">Loading events...</div>}

        {!loading && (
          <>
            <div className="results-info">
              Showing {events.length} of {total} events
            </div>
            <EventTable events={events} />

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="pagination">
                <button
                  onClick={() => setPage(Math.max(1, page - 1))}
                  disabled={page === 1}
                >
                  ← Previous
                </button>
                <span className="page-info">
                  Page {page} of {totalPages}
                </span>
                <button
                  onClick={() => setPage(Math.min(totalPages, page + 1))}
                  disabled={page === totalPages}
                >
                  Next →
                </button>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}

export default App
