ec2_instances: list[dict] = [
    {"id": "i-001", "state": "running", "region": "us-west-1", "tags": {"env": "production", "owner": "team-a"}},
    {"id": "i-002", "state": "stopped", "region": "us-west-1", "tags": {"env": "staging"}},
    {"id": "i-003", "state": "running", "region": "us-east-1", "tags": {"owner": "team-b"}},
    {"id": "i-004", "state": "running", "region": "us-east-1", "tags": {"env": "production"}},
    {"id": "i-005", "state": "stopped", "region": "us-west-2", "tags": {"env": "development", "owner": "team-c"}},
    {"id": "i-006", "state": "running", "region": "us-west-2", "tags": {"env": "production", "owner": "team-a"}},
]

missing_owner: list[str] = []
missing_env: list[str] = []
running_count = 0
stopped_count = 0

for instance in ec2_instances:
    instance_id = instance["id"]
    state = instance["state"]
    region = instance["region"]
    tags = instance["tags"]
    owner = tags.get("owner", "N/A")
    env = tags.get("env", "N/A")

    print(f"ID: {instance_id} | State: {state} | Region: {region} | Env: {env} | Owner: {owner}")

    if state == "running":
        running_count += 1
    else:
        stopped_count += 1

    if owner == "N/A":
        missing_owner.append(instance_id)
    if env == "N/A":
        missing_env.append(instance_id)

print("\n=== Audit Report ===")
print(f"Running:       {running_count}")
print(f"Stopped:       {stopped_count}")
print(f"Missing owner: {missing_owner}")
print(f"Missing env:   {missing_env}")
    
