import React, { useState } from 'react'
import './FilterBar.css'

function FilterBar({ venues, eventTypes, filters, onFilterChange, onResetFilters, onSearchChange, searchQuery }) {
  const [isOpen, setIsOpen] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    onFilterChange({
      ...filters,
      [name]: value,
    })
  }

  const handleSearchChange = (e) => {
    if (onSearchChange) {
      onSearchChange(e.target.value)
    }
  }

  const toggleFilters = () => {
    setIsOpen(!isOpen)
  }

  const handleResetFilters = () => {
    onResetFilters()
    setIsOpen(false)
  }

  return (
    <div className="filter-bar">
      <div className="filter-header">
        <h2>Filters & Search</h2>
        <button className="toggle-btn" onClick={toggleFilters}>
          {isOpen ? '✕' : '☰'}
        </button>
      </div>

      {/* Search bar - always visible */}
      <div className="search-container">
        <input
          type="text"
          placeholder="Search events..."
          className="search-input"
          value={searchQuery || ''}
          onChange={handleSearchChange}
        />
      </div>

      {/* Filter inputs - collapsible on mobile */}
      <div className={`filter-inputs ${isOpen ? 'open' : ''}`}>
        <div className="filter-group">
          <label>Venue</label>
          <select
            name="venue"
            value={filters.venue}
            onChange={handleChange}
          >
            <option value="">All Venues</option>
            {venues.map((v) => (
              <option key={v} value={v}>
                {v}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Event Type</label>
          <select
            name="event_type"
            value={filters.event_type}
            onChange={handleChange}
          >
            <option value="">All Types</option>
            {eventTypes.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Start Date</label>
          <input
            type="date"
            name="start_date"
            value={filters.start_date}
            onChange={handleChange}
          />
        </div>

        <div className="filter-group">
          <label>End Date</label>
          <input
            type="date"
            name="end_date"
            value={filters.end_date}
            onChange={handleChange}
          />
        </div>

        <button className="reset-btn" onClick={handleResetFilters}>
          Reset Filters
        </button>
      </div>
    </div>
  )
}

export default FilterBar
