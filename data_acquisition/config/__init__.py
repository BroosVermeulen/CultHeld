"""Shared configuration for data acquisition.

Expose knobs that affect cross-venue behavior.
"""

# Venues where we expect a real ticket price in the staging output and
# therefore enforce non-null `price` during validation.
# Adjust this list as scrapers evolve.
PRICE_REQUIRED_VENUES: set[str] = {
	'Concertgebouw',
	'Studio K',
	'FCHYENA',
	'De Balie',
}
