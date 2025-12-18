import React from 'react'
import './FilterBar.css'

function FilterBar({ venues, eventTypes, filters, onFilterChange, onResetFilters }) {
  const handleChange = (e) => {
    const { name, value } = e.target
    onFilterChange({
      ...filters,
      [name]: value,
    })
  }

  return (
    <div className="filter-bar">
      <h2>Filters</h2>
      <div className="filter-inputs">
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

        <button className="reset-btn" onClick={onResetFilters}>
          Reset Filters
        </button>
      </div>
    </div>
  )
}

export default FilterBar
