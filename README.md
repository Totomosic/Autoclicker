# Simple Python Autoclicker

Basic Usage: `python autoclick.py -i AVG -jmin MIN_JITTER -jmax MAX_JITTER`

where:  
- `AVG`: The average interval in milliseconds between clicks  
- `MIN_JITTER`: The maximum number of milliseconds that could be subtracted from `AVG`  
- `MAX_JITTER`: The maximum number of milliseconds that could be added to `AVG`  

Therefore the delay between clicks is between `AVG-MIN_JITTER` and `AVG+MAX_JITTER`.