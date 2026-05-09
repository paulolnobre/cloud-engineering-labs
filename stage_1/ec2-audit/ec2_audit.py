instances = [
    {"id": "i-001", "state": "running",  "type": "t3.micro",  "name": "web-server-1"},
    {"id": "i-002", "state": "stopped",  "type": "t3.large",  "name": "batch-processor"},
    {"id": "i-003", "state": "running",  "type": "t3.large",  "name": "api-gateway-proxy"},
    {"id": "i-004", "state": "stopped",  "type": "t3.micro",  "name": "dev-sandbox"},
    {"id": "i-005", "state": "running",  "type": "t3.medium", "name": "worker-node-1"},
    {"id": "i-006", "state": "stopped",  "type": "t3.large",  "name": "data-pipeline"},
]

stopped_ids = [i["id"] for i in instances if i["state"] == "stopped"]
t3_large_running = [i["id"] for i in instances if i["state"] == "running" and i["type"] == "t3.large"]

count = {}
for i in instances:
    state = i["state"]
    count[state] = count.get(state, 0) + 1

print("=== EC2 Audit Report ===")
print(f"Stopped instances (cleanup candidates): {stopped_ids}")
print(f"t3.large instances running (high cost): {t3_large_running}")
print(f"Count by state: {count}")
