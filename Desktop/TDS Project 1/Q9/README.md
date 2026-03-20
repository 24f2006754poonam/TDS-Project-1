# Data Labyrinth Automation Script

This script automates solving the Data Labyrinth game from TDS IITM course by reverse-engineering the API and using BFS to map the labyrinth, collect fragments, and answer the final query.

## Prerequisites

- Python 3
- `requests` library
- Access to the game (find the URL in your course dashboard)

## Setup

1. Navigate to the Q9 directory: `cd "/Users/poonamgupta/Desktop/TDS Project 1/Q9"`
2. Create virtual environment: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install requests: `pip install requests`

## Inspect the Game

1. Open the game in your browser.
2. Open DevTools (F12) → Network tab → Filter Fetch/XHR.
3. Play manually to see API calls (/start, /move, /query, /submit).
4. Note the base URL, request/response formats.

## Adjust the Script

- Update `BASE_URL` to the actual game URL.
- If directions are different (e.g., north/south), change `directions` and `dx`/`dy`.
- Modify the answer computation in the script based on the actual query (e.g., sum, average, max of specific fields).
- If fragments are not dicts with 'value', adjust the collection and computation.

## Run the Script

```bash
python labyrinth.py
```

The script will:
- Start the game with your email.
- Use BFS to explore all reachable positions, collecting fragments.
- Call /query for the final question.
- Compute and submit the answer.
- Print the JWT token.

## Troubleshooting

- If moves fail, check API payloads.
- If query is unknown, inspect the /query response and update the answer logic.
- For shifting mazes, add maze state to visited tracking.
- Ensure the game allows moving back (the script assumes it does by moving opposite directions).

## Output

The JWT will be printed, ready for submission. It should pass verification (email, game 'labyrinth', current week, recent completion).