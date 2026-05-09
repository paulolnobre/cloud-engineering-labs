import json
from datetime import datetime


def load_aws_config(filepath):
    """
    Reads an AWS JSON config file and returns it as a dictionary.
    """
    with open(filepath, "r") as f:
        return json.load(f)


def load_ec2_instances(filepath):
    """
    Reads a JSON file containing a list of EC2 instances.
    """
    with open(filepath, "r") as f:
        return json.load(f)


def filter_instances_by_state(instances, state):
    """
    Filters instances by state: "running" or "stopped".
    """
    return [instance for instance in instances if instance["state"] == state]


def write_text_report(instances, config, filepath):
    """
    Writes a .txt report summarizing the EC2 instances.
    """
    timestamp = datetime.now().isoformat()

    with open(filepath, "w") as f:
        f.write("=== AWS EC2 Report ===\n")
        f.write(f"Project: {config['project']} | Env: {config['environment']} | Region: {config['region']}\n")
        f.write(f"Generated: {timestamp}\n")
        f.write("\n")
        for instance in instances:
            f.write(f"  [{instance['state'].upper()}] {instance['name']} ({instance['id']}) - {instance['type']}\n")


def write_json_report(instances, running, stopped, config, filepath):
    """
    Writes a structured .json report — suitable for ingestion
    by other systems or storage in S3.
    """
    report = {
        "generated_at": datetime.now().isoformat(),
        "project": config["project"],
        "environment": config["environment"],
        "region": config["region"],
        "summary": {
            "total": len(instances),
            "running": len(running),
            "stopped": len(stopped)
        },
        "instances": instances
    }

    with open(filepath, "w") as f:
        json.dump(report, f, indent=2)


if __name__ == "__main__":
    config = load_aws_config("aws_config.json")
    print(f"Config loaded: {config['project']} / {config['environment']} / {config['region']}")

    instances = load_ec2_instances("ec2_instances.json")
    print(f"Instances loaded: {len(instances)} total")

    running = filter_instances_by_state(instances, "running")
    stopped = filter_instances_by_state(instances, "stopped")
    print(f"  Running: {len(running)} | Stopped: {len(stopped)}")

    write_text_report(instances, config, "ec2_report.txt")
    print("TXT report generated: ec2_report.txt")

    write_json_report(instances, running, stopped, config, "ec2_report.json")
    print("JSON report generated: ec2_report.json")
