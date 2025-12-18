import React from 'react'
import './EventTable.css'

function EventTable({ events }) {
  if (events.length === 0) {
    return (
      <div className="empty-state">
        <p>No events found. Try adjusting your filters.</p>
      </div>
    )
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

  return (
    <div className="table-container">
      <table className="event-table">
        <thead>
          <tr>
            <th>Venue</th>
            <th>Event Type</th>
            <th>Event Name</th>
            <th>Date & Time</th>
            <th>Price</th>
            <th>Tickets</th>
          </tr>
        </thead>
        <tbody>
          {events.map((event, idx) => (
            <tr key={idx}>
              <td className="venue">{event.venue}</td>
              <td>
                <span className={`event-type ${event.event_type.toLowerCase()}`}>
                  {event.event_type}
                </span>
              </td>
              <td className="event-name">{event.event_name}</td>
              <td className="date">{formatDate(event.start_date_time)}</td>
              <td className="price">
                {event.price ? `€${event.price.toFixed(2)}` : '—'}
              </td>
              <td>
                <a
                  href={event.ticket_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="ticket-link"
                >
                  View
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default EventTable
