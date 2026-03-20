import requests

BASE_URL = "https://tds-network-games.sanand.workers.dev"
EMAIL = "24f2006754@ds.study.iitm.ac.in"

session = requests.Session()

opposite = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}

# ---------------------------
# START
# ---------------------------
res = session.post(f"{BASE_URL}/labyrinth/start", json={"email": EMAIL})
data = res.json()

print("Start:", data)

token = data["session_token"]

session.headers.update({
    "X-Session-Token": token
})

fragments_required = data["fragments_required"]

# ---------------------------
# HELPERS
# ---------------------------
def look():
    return session.get(f"{BASE_URL}/labyrinth/look").json()

def move(direction):
    return session.post(f"{BASE_URL}/labyrinth/move", json={"direction": direction}).json()

def collect():
    return session.post(f"{BASE_URL}/labyrinth/collect").json()

def inventory():
    return session.get(f"{BASE_URL}/labyrinth/inventory").json()

# ---------------------------
# DFS WITH GLOBAL STOP
# ---------------------------
visited = set()
stop = False   # 🔥 GLOBAL STOP FLAG

def dfs():
    global stop

    if stop:
        return

    state = look()

    # 🔥 HARD STOP
    if state.get("fragments_collected", 0) >= fragments_required:
        stop = True
        return

    room = state["room_id"]

    if room in visited:
        return
    visited.add(room)

    # collect
    if state.get("has_item") and not state.get("item_collected"):
        item = collect()
        if item.get("fragment_type") == "required":
            print("Collected:", item["fragment"])

    for d in state.get("exits", []):
        if stop:
            return

        next_state = move(d)

        if not next_state.get("success"):
            continue

        dfs()

        if stop:
            return

        move(opposite[d])

# run DFS
dfs()

print("\nStopped exploration early!")

# ---------------------------
# GET ALL FRAGMENTS
# ---------------------------
inv = inventory()
all_fragments = inv.get("fragments", [])

print("Total fragments:", len(all_fragments))

# ---------------------------
# SOLVE
# ---------------------------
clean = []
for f in all_fragments:
    d = f["data"]

    sl = d.get("session_length")
    th = d.get("timestamp_hour")

    if isinstance(sl, (int, float)) and isinstance(th, (int, float)):
        clean.append(d)

sorted_fragments = sorted(clean, key=lambda x: x["session_length"], reverse=True)
top3 = sorted_fragments[:3]

answer = sum(x["timestamp_hour"] for x in top3)

print("\nTop 3:", top3)
print("Final Answer:", answer)

# ---------------------------
# SUBMIT
# ---------------------------
res = session.post(
    f"{BASE_URL}/labyrinth/submit",
    json={"answer": answer}
)

print("\nSubmit:", res.json())
