import React, { useState } from 'react'
import './EventTable.css'

function EventTable({ events, onLoadMore, hasMore, isLoading }) {
  const [expandedId, setExpandedId] = useState(null)

  const handleShare = (event) => {
    const text = `${event.event_name} at ${event.venue}\n${new Date(event.start_date_time).toLocaleString('nl-NL')}\n${event.ticket_url}`
    if (navigator.share) {
      navigator.share({
        title: event.event_name,
        text: text,
      })
    } else {
      navigator.clipboard.writeText(text)
      alert('Event details copied!')
    }
  }

  const toggleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id)
  }

  const formatDate = (dateString) => {
    try {
      return new Date(dateString).toLocaleString('nl-NL', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    } catch {
      return dateString
    }
  }

  if (events.length === 0) {
    return (
      <div className="empty-state">
        <p>No events found. Try adjusting your filters.</p>
      </div>
    )
  }

  return (
    <div className="events-container">
      <div className="events-grid">
        {events.map((event, index) => (
          <div key={`${event.venue}-${event.event_name}-${index}`} className="event-card">
            <div className="card-header" onClick={() => toggleExpand(index)}>
              <div className="card-title-section">
                <h3 className="event-name">{event.event_name}</h3>
                <div className="card-meta">
                  <span className="badge">{event.venue}</span>
                  <span className={`event-type ${event.event_type.toLowerCase()}`}>
                    {event.event_type}
                  </span>
                </div>
              </div>
              <div className="card-toggle">
                {expandedId === index ? '▼' : '▶'}
              </div>
            </div>

            <div className="card-date">
              {formatDate(event.start_date_time)}
            </div>

            {expandedId === index && (
              <div className="card-details">
                <div className="card-price">
                  {event.price ? `€${event.price.toFixed(2)}` : 'Price not available'}
                </div>
                <div className="card-actions">
                  <a 
                    href={event.ticket_url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="btn-ticket"
                  >
                    Get Tickets
                  </a>
                  <button 
                    className="btn-share"
                    onClick={(e) => {
                      e.stopPropagation()
                      handleShare(event)
                    }}
                  >
                    Share
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {hasMore && (
        <div className="load-more-container">
          <button 
            className="btn-load-more"
            onClick={onLoadMore}
            disabled={isLoading}
          >
            {isLoading ? 'Loading...' : 'Load More Events'}
          </button>
        </div>
      )}
    </div>
  )
}

export default EventTable
