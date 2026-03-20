import requests

BASE_URL = "https://tds-network-games.sanand.workers.dev"
EMAIL = "24f2006754@ds.study.iitm.ac.in"

session = requests.Session()

# ---------------------------
# START SESSION AGAIN (fresh)
# ---------------------------
res = session.post(
    f"{BASE_URL}/labyrinth/start",
    json={"email": EMAIL}
)

data = res.json()
print("Start:", data)

# attach session token
session.headers.update({
    "X-Session-Token": data["session_token"]
})

# ---------------------------
# DIRECT SUBMIT (FINAL ANSWER)
# ---------------------------
answer = 12

res = session.post(
    f"{BASE_URL}/labyrinth/submit",
    json={"answer": answer}
)

print("\nSubmit Response:")
print(res.json())
