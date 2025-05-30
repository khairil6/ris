import orthanc
from orthanc import ChangeType, ResourceType
import sqlite3
import os
from datetime import datetime

# Path inside the container where your volume is mounted
AUDIT_DB = '/var/lib/orthanc/auditdb/audit.sqlite'

# Ensure the auditdb directory exists
os.makedirs(os.path.dirname(AUDIT_DB), exist_ok=True)

# Open SQLite connection (allow callbacks from any thread)
conn = sqlite3.connect(AUDIT_DB, check_same_thread=False)
cur = conn.cursor()

# Create the audit table if it's not already there
cur.execute('''
CREATE TABLE IF NOT EXISTS audit (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp    TEXT,
  event_type   TEXT,
  resource_id  TEXT,
  info         TEXT
)
''')
conn.commit()

# ─── NEW: build lookup tables for human-readable names ───────────────────────
CHANGE_TYPE_MAP = {
    getattr(ChangeType, attr): attr
    for attr in dir(ChangeType)
    if not attr.startswith("_")
}
RESOURCE_TYPE_MAP = {
    getattr(ResourceType, attr): attr
    for attr in dir(ResourceType)
    if not attr.startswith("_")
}
# ───────────────────────────────────────────────────────────────────────────────

def log(event, resource_id, info=''):
    ts = datetime.utcnow().isoformat()
    cur.execute(
        'INSERT INTO audit(timestamp, event_type, resource_id, info) VALUES (?,?,?,?)',
        (ts, event, resource_id, info)
    )
    conn.commit()

def OnStoredInstance(dicom, instanceId):
    """Fires whenever a new DICOM instance is stored."""
    sop = dicom.GetInstanceMetadata('SopClassUid')
    log('OnStoredInstance', instanceId, sop)

def OnChange(changeTypeInt, resourceTypeInt, resourceId):
    """Fires on any change: logs both the changeType and the resourceType."""
    # ─── MODIFIED: use our lookup tables instead of .name on the enum ─────────
    changeName   = CHANGE_TYPE_MAP.get(changeTypeInt, f'UnknownChange({changeTypeInt})')
    resourceName = RESOURCE_TYPE_MAP.get(resourceTypeInt, f'UnknownResource({resourceTypeInt})')
    # ───────────────────────────────────────────────────────────────────────────
    log(f'OnChange:{changeName}', resourceId, resourceName)

# Register our callbacks with Orthanc
orthanc.RegisterOnStoredInstanceCallback(OnStoredInstance)
orthanc.RegisterOnChangeCallback(OnChange)
