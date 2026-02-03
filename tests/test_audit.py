
import json
import os
import time
from unittest.mock import patch

import pytest

from backpack.audit import AuditLogger


class TestAuditLogger:
    @pytest.fixture
    def audit_logger(self, tmp_path):
        log_file = tmp_path / "test_audit.log"
        return AuditLogger(file_path=str(log_file))

    def test_log_event(self, audit_logger):
        audit_logger.log_event("test_event", {"key": "value"})
        
        assert os.path.exists(audit_logger.file_path)
        with open(audit_logger.file_path, "r") as f:
            lines = f.readlines()
            assert len(lines) == 1
            
            # Verify it's valid JSON
            encrypted_data = json.loads(lines[0])
            assert "data" in encrypted_data
            assert "salt" in encrypted_data

    def test_read_logs(self, audit_logger):
        # Log a few events
        audit_logger.log_event("event1", {"id": 1})
        time.sleep(0.01) # Ensure timestamp difference
        audit_logger.log_event("event2", {"id": 2})
        
        logs = audit_logger.read_logs()
        assert len(logs) == 2
        assert logs[0]["event_type"] == "event1"
        assert logs[0]["details"]["id"] == 1
        assert logs[1]["event_type"] == "event2"
        assert logs[1]["details"]["id"] == 2
        
        # Verify order
        assert logs[0]["timestamp"] < logs[1]["timestamp"]

    def test_log_integrity(self, audit_logger):
        """Test that we can decrypt what we wrote."""
        details = {"secret": "hidden_value", "action": "inject"}
        audit_logger.log_event("sensitive_op", details)
        
        logs = audit_logger.read_logs()
        assert len(logs) == 1
        assert logs[0]["event_type"] == "sensitive_op"
        assert logs[0]["details"] == details

    def test_corrupted_log_entry(self, audit_logger):
        """Test that one corrupted line doesn't break reading."""
        audit_logger.log_event("valid_1", {})
        
        # Append garbage
        with open(audit_logger.file_path, "a") as f:
            f.write("garbage_data\n")
            
        audit_logger.log_event("valid_2", {})
        
        logs = audit_logger.read_logs()
        assert len(logs) == 2
        assert logs[0]["event_type"] == "valid_1"
        assert logs[1]["event_type"] == "valid_2"

    def test_clear_logs(self, audit_logger):
        audit_logger.log_event("test", {})
        assert os.path.exists(audit_logger.file_path)
        
        audit_logger.clear()
        assert not os.path.exists(audit_logger.file_path)
        
        # Reading cleared logs should return empty list
        assert audit_logger.read_logs() == []

    def test_log_error_handling(self, audit_logger):
        """Test that logging doesn't crash if file write fails."""
        # Mock open to raise an exception
        with patch("builtins.open", side_effect=IOError("Disk full")):
            # Should not raise
            audit_logger.log_event("test", {})

