def validate_instance_id(instance_id: str) -> None:
    if not instance_id:
        raise ValueError("Instance ID cannot be empty.")

    if not instance_id.startswith("i-"):
        raise LookupError(f"Instance not found: {instance_id}")


def describe_instance(instance_id: str) -> dict:
    if instance_id == "i-0000000":
        raise PermissionError("Not authorized to perform ec2:DescribeInstances.")

    return {
        "id": instance_id,
        "state": "running",
        "type": "t3.micro",
    }


def handle_instance_check(instance_id: str) -> None:
    try:
        validate_instance_id(instance_id)
        instance = describe_instance(instance_id)

        print(
            f"[OK] Instance {instance['id']} is {instance['state']} "
            f"and type is {instance['type']}."
        )

    except ValueError as error:
        print(f"[INVALID INPUT] {error}")
    except PermissionError as error:
        print(f"[ACCESS DENIED] Check your IAM policy. Detail: {error}")
    except LookupError as error:
        print(f"[NOT FOUND] {error}")


def main() -> None:
    test_cases = ["", "i-0000000", "x-9999", "i-0abc123"]

    for instance_id in test_cases:
        handle_instance_check(instance_id)


if __name__ == "__main__":
    main()
