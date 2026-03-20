import requests

BASE_URL = "https://tds-network-games.sanand.workers.dev/detective"
EMAIL = "24f2006754@ds.study.iitm.ac.in"

def start_game():
    payload = {"email": EMAIL}
    response = requests.post(f"{BASE_URL}/start", json=payload)
    return response.json()

def query_node(session_token, node_id):
    """
    Query a specific node to get its attributes and neighbors.
    Uses 1 query from your budget.
    """
    headers = {"X-Session-Token": session_token}
    payload = {"node_id": node_id}
    response = requests.post(f"{BASE_URL}/query", json=payload, headers=headers)
    return response.json()

def submit_answer(session_token, anomalous_node_id, shortest_path):
    """
    Submit the identified anomalous node and the shortest proof path.
    """
    headers = {"X-Session-Token": session_token}
    payload = {
        "anomalous_node": anomalous_node_id,
        "path": shortest_path
    }
    response = requests.post(f"{BASE_URL}/submit", json=payload, headers=headers)
    return response.json()

def solve_detective():
    print("Starting Graph Detective...")
    game_state = start_game()
    print("Game State:", game_state)
    
    if game_state.get('status') == 'failed':
        print("\nSession is already in a failed state (out of queries).")
        print("Wait for the next week's ISO timeframe or a reset opportunity.")
        return
        
    session_token = game_state.get("session_token")
    anchor_node = game_state.get("anchor_node")
    clues = game_state.get("clues")
    
    # ---------------------------------------------------------
    # Game Logic Implementation
    # You have limited queries. You shouldn't blindly run BFS.
    # Instead, use a Priority Queue (Dijkstra/A* variant)
    # evaluating nodes against the clues to find the anomaly.
    # ---------------------------------------------------------
    # ... Add logic here ...

if __name__ == "__main__":
    solve_detective()
