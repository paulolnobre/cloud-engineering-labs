ec2_instances: list[dict] = [
    {"id": "i-001", "state": "running", "region": "us-west-1", "monthly_cost": 120.50},
    {"id": "i-002", "state": "stopped", "region": "us-west-1", "monthly_cost": 0.00},
    {"id": "i-003", "state": "running", "region": "us-east-1", "monthly_cost": 85.25},
    {"id": "i-004", "state": "running", "region": "us-east-1", "monthly_cost": 150.00},
    {"id": "i-005", "state": "stopped", "region": "us-west-2", "monthly_cost": 0.00},
    {"id": "i-006", "state": "running", "region": "us-west-2", "monthly_cost": 200.75},
]

print(f"\n{'ID':<10} {'State':<10} {'Region':<15} {'Monthly Cost':>15}")
print("=" * 54)

for instance in ec2_instances:
    cost = f"${instance['monthly_cost']:,.2f}"
    print(f"{instance['id']:<10} {instance['state']:<10} {instance['region']:<15} {cost:>15}")

total_cost = sum(instance["monthly_cost"] for instance in ec2_instances)
running_count = sum(1 for instance in ec2_instances if instance["state"] == "running")
stopped_count = sum(1 for instance in ec2_instances if instance["state"] == "stopped")

print()
print("=" * 54)
print("=== Summary ===".center(54))
print("-" * 54)
print(f"  {'Total Monthly Cost:':<22} {f'${total_cost:,.2f}':>8}")
print(f"  {'Running Instances:':<22} {running_count:>8}")
print(f"  {'Stopped Instances:':<22} {stopped_count:>8}")
print("=" * 54)
