
import os
import logging
from unittest.mock import patch, MagicMock
import pytest
from click.testing import CliRunner
from backpack.crypto import derive_key, encrypt_data, decrypt_data
from backpack.exceptions import ValidationError, KeyDerivationError, EncryptionError, DecryptionError
from backpack.cli import cli, _configure_logging, rotate
from backpack.agent_lock import AgentLock

class TestCryptoCoverage:
    def test_derive_key_short_salt(self):
        with pytest.raises(ValidationError, match="Salt must be at least 8 bytes"):
            derive_key("password", salt=b"short")

    def test_derive_key_unexpected_error(self):
        with patch("backpack.crypto.PBKDF2HMAC", side_effect=Exception("Boom")):
            with pytest.raises(KeyDerivationError, match="Failed to derive encryption key"):
                derive_key("password")

    def test_encrypt_data_unexpected_error(self):
        with patch("backpack.crypto.derive_key", side_effect=Exception("Boom")):
            with pytest.raises(EncryptionError, match="Failed to encrypt data"):
                encrypt_data("data", "password")

    def test_decrypt_data_unexpected_error(self):
        with patch("backpack.crypto.base64.b64decode", side_effect=Exception("Boom")):
            with pytest.raises(DecryptionError, match="Decryption failed"):
                decrypt_data({"data": "d", "salt": "s"}, "password")

class TestCLICoverage:
    def test_configure_logging_file(self, temp_dir):
        log_file = os.path.join(temp_dir, "backpack.log")
        with patch.dict(os.environ, {"BACKPACK_LOG_FILE": log_file}):
            # Reset logger handlers to force reconfiguration
            root = logging.getLogger()
            handlers = root.handlers[:]
            root.handlers = []
            try:
                _configure_logging()
                assert os.path.exists(log_file) or any(isinstance(h, logging.FileHandler) for h in root.handlers)
            finally:
                root.handlers = handlers

    def test_rotate_command(self, temp_dir):
        runner = CliRunner()
        with runner.isolated_filesystem():
            # Create initial agent.lock
            agent_lock = AgentLock(master_key="old-key")
            agent_lock.create({"KEY": "val"}, {"prompt": "p"})
            
            # Run rotate
            # We need to provide new key via prompt
            result = runner.invoke(cli, ["rotate", "--key-file", "agent.lock"], input="new-key\nnew-key\n", env={"AGENT_MASTER_KEY": "old-key"})
            
            assert result.exit_code == 0
            assert "Successfully decrypted" in result.output
            assert "Re-encrypted" in result.output

            # Verify with new key
            new_lock = AgentLock(master_key="new-key")
            data = new_lock.read()
            assert data["credentials"]["KEY"] == "val"

    def test_rotate_command_not_found(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ["rotate", "--key-file", "missing.lock"])
            assert result.exit_code == 1
            assert "not found" in result.output

    def test_rotate_command_decrypt_fail(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
             with open("agent.lock", "w") as f:
                 f.write("junk")
             
             result = runner.invoke(cli, ["rotate"], env={"AGENT_MASTER_KEY": "wrong"})
             assert result.exit_code == 1
             assert "Failed to decrypt" in result.output

    def test_rotate_command_empty_key(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            agent_lock = AgentLock(master_key="old-key")
            agent_lock.create({}, {})
            
            result = runner.invoke(cli, ["rotate"], input="\n\n", env={"AGENT_MASTER_KEY": "old-key"})
            assert result.exit_code == 1
            assert "Key cannot be empty" in result.output

    def test_rotate_command_write_fail(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            agent_lock = AgentLock(master_key="old-key")
            agent_lock.create({}, {})
            
            with patch("backpack.cli.AgentLock.create", side_effect=Exception("Write failed")):
                result = runner.invoke(cli, ["rotate", "--new-key", "new"], env={"AGENT_MASTER_KEY": "old-key"})
                assert result.exit_code == 1
                assert "Failed to rotate key" in result.output

    def test_run_cloud_mode(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("script.py", "w") as f:
                f.write("pass")
            
            agent_lock = AgentLock(master_key="key")
            agent_lock.create({"ENV_KEY": "val"}, {})

            with patch("subprocess.run") as mock_run:
                mock_run.return_value.returncode = 0
                # Set ENV_KEY in environment to simulate it being there
                with patch.dict(os.environ, {"AGENT_MASTER_KEY": "key", "ENV_KEY": "val"}):
                    result = runner.invoke(cli, ["run", "script.py"])
                    assert result.exit_code == 0
                    # Check that we didn't prompt
                    assert "Allow access?" not in result.output

    def test_run_key_sources(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("script.py", "w") as f:
                f.write("pass")
            
            # Setup:
            # ENV_KEY: in environment
            # LOCK_KEY: in agent.lock (real value)
            # VAULT_KEY: in vault
            # MISSING_KEY: nowhere
            
            creds = {
                "ENV_KEY": "placeholder",
                "LOCK_KEY": "real-lock-value",
                "VAULT_KEY": "placeholder",
                "MISSING_KEY": "placeholder"
            }
            
            agent_lock = AgentLock(master_key="key")
            agent_lock.create(creds, {})

            with patch("subprocess.run") as mock_run, \
                 patch("backpack.cli.get_key") as mock_get_key:
                
                mock_run.return_value.returncode = 0
                mock_get_key.side_effect = lambda k: "vault-value" if k == "VAULT_KEY" else None
                
                with patch.dict(os.environ, {"ENV_KEY": "env-value"}):
                    # Interactive run, approve all
                    result = runner.invoke(cli, ["run", "script.py"], input="y\ny\n")
                    
                    assert "Key ENV_KEY found in environment" in result.output
                    assert "Allow access?" in result.output # For LOCK_KEY and VAULT_KEY
                    assert "Key MISSING_KEY not found" in result.output
                    
                    # Verify env vars passed to subprocess
                    call_args = mock_run.call_args
                    env_passed = call_args[1]['env']
                    assert env_passed['ENV_KEY'] == 'env-value'
                    assert env_passed['LOCK_KEY'] == 'real-lock-value'
                    assert env_passed['VAULT_KEY'] == 'vault-value'
