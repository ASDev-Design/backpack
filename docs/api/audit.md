# Audit Logging

The `backpack.audit` module provides the `AuditLogger` class for creating an encrypted, tamper-evident log of sensitive operations.

## Class: AuditLogger

Manages an encrypted append-only audit log. Each log entry is individually encrypted and signed (via authenticated encryption) to ensure integrity and confidentiality.

### `__init__(file_path: str = "agent_audit.log")`

Initialize an AuditLogger instance.

- **file_path**: Path to the audit log file (default: "agent_audit.log").

### `log_event(event_type: str, details: Dict[str, Any] = None) -> None`

Log an event to the encrypted audit log.

- **event_type**: Identifier for the type of event (e.g., "key_access", "lock_created").
- **details**: Optional dictionary containing non-sensitive event details.

### `read_logs() -> List[Dict[str, Any]]`

Read and decrypt all entries from the audit log.

**Returns:**
List of decrypted log entries sorted by timestamp.

### `clear() -> None`

Clear the audit log file.
