from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];record=json.loads((ROOT/'docs/skill-transfer.json').read_text());assert record['version']=='2.0.0'
consumed=ROOT/record.get('consumed_skill_path','skills/eda-lesson-studio')
for rel,digest in record['consumed_files'].items():assert hashlib.sha256((consumed/rel).read_bytes()).hexdigest()==digest,rel
assert len(record['consumed_files'])==5
print('PASS: all five consumed skill files match the frozen v2.0.0 hashes at '+str(consumed.relative_to(ROOT)))
