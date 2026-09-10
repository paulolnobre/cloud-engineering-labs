"""Unit tests for Stage 2 governance and cleanup logic.

The modules are loaded from their file paths because some lab directory names use
hyphens and therefore are not importable as regular Python package names.
"""

from __future__ import annotations

import importlib.util
import logging
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock

import pytest


STAGE_2 = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str) -> ModuleType:
    """Load a Stage 2 script as a module without executing its main block."""
    module_path = STAGE_2 / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {module_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


tag_enforcer = load_module("stage2_tag_enforcer", "tagging-cleanup/tag_enforcer.py")
cleanup = load_module("stage2_cleanup", "tagging-cleanup/cleanup.py")
sg_auditor = load_module("stage2_sg_auditor", "security-groups/sg_auditor.py")


def test_audit_tags_returns_only_non_compliant_instances() -> None:
    instances = [
        {
            "InstanceId": "i-compliant",
            "Tags": [
                {"Key": "Name", "Value": "api"},
                {"Key": "Environment", "Value": "dev"},
                {"Key": "Owner", "Value": "platform"},
            ],
        },
        {
            "InstanceId": "i-missing-owner",
            "Tags": [
                {"Key": "Name", "Value": "worker"},
                {"Key": "Environment", "Value": "dev"},
            ],
        },
        {"InstanceId": "i-no-tags"},
    ]

    result = tag_enforcer.audit_tags(instances)

    assert result == ["i-missing-owner", "i-no-tags"]


def test_get_instances_uses_paginator_without_calling_aws() -> None:
    client = MagicMock()
    paginator = client.get_paginator.return_value
    paginator.paginate.return_value = [
        {"Reservations": [{"Instances": [{"InstanceId": "i-one"}]}]},
        {"Reservations": [{"Instances": [{"InstanceId": "i-two"}]}]},
    ]

    result = tag_enforcer.get_instances(client)

    client.get_paginator.assert_called_once_with("describe_instances")
    paginator.paginate.assert_called_once_with()
    assert [item["InstanceId"] for item in result] == ["i-one", "i-two"]


def test_terminate_instance_dry_run_does_not_call_client() -> None:
    client = MagicMock()

    cleanup.terminate_instance(client, "i-lab", dry_run=True)

    client.terminate_instances.assert_not_called()


def test_terminate_instance_calls_expected_instance_when_enabled() -> None:
    client = MagicMock()

    cleanup.terminate_instance(client, "i-lab", dry_run=False)

    client.terminate_instances.assert_called_once_with(InstanceIds=["i-lab"])


def test_open_ssh_is_reported_as_critical(
    caplog: pytest.LogCaptureFixture,
) -> None:
    rules = [
        {
            "IpProtocol": "tcp",
            "FromPort": 22,
            "ToPort": 22,
            "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
        }
    ]

    with caplog.at_level(logging.WARNING, logger=sg_auditor.logger.name):
        sg_auditor.audit_inbound_rules("sg-open", "open-ssh", rules)

    assert any(
        "[CRITICAL]" in record.message and "port 22" in record.message
        for record in caplog.records
    )


def test_restricted_rule_is_reported_as_ok(
    caplog: pytest.LogCaptureFixture,
) -> None:
    rules = [
        {
            "IpProtocol": "tcp",
            "FromPort": 443,
            "ToPort": 443,
            "IpRanges": [{"CidrIp": "10.0.0.0/8"}],
        }
    ]

    with caplog.at_level(logging.INFO, logger=sg_auditor.logger.name):
        sg_auditor.audit_inbound_rules("sg-private", "private-https", rules)

    assert any("[OK]" in record.message for record in caplog.records)
    assert not any("[CRITICAL]" in record.message for record in caplog.records)
