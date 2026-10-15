# backup-chain-audit

Trace retained targets to their bases, detect missing/unverified/cyclic ancestry, count shared bytes once and explain deletion blockers.

## User and task

Backup operators reviewing an explicit base/incremental manifest and a retention/deletion proposal. Deleting one base can strand multiple retained incrementals; total storage can double-count shared ancestors.

## Install and first useful result

Python 3.10+ and pip. Git source install; no external-registry release is claimed.

```sh
git clone https://github.com/nripankadas07/backup-chain-audit.git
cd backup-chain-audit
python -m venv .venv
# POSIX: . .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install .
backup-chain-audit example.json
```

The example needs base and delta, counts 120 bytes once and marks only obsolete eligible under the declared preservation contract. The example is synthetic. JSON goes to stdout. Exit0 means analyzed with no review findings; exit 1 means review findings; exit 2 means malformed/unsupported input or an IO error. Differences explicitly labeled informational do not alone trigger exit 1. Help: `backup-chain-audit --help`.

## Input contract

Required top-level keys: snapshots, retain, delete. Each snapshot has id, parent (id or null), verified (boolean declaration), bytes (nonnegative integer). A null parent declares a self-contained base. Each incremental has exactly one parent. retain/delete contain unique ids. Delete proposals must name known snapshots. A missing retained id or parent is a finding. Every retained chain must be complete and declared verified before any deletion eligibility is reported. eligible_delete applies only to the supplied delete proposal and preservation roots, not all imaginable restores.

Every object rejects unknown keys. CLI input is UTF-8 JSON, read with a 2 MiB cap before parsing; duplicate keys/nonfinite values fail. Default arrays allow at most 512 entries, strings1..256 characters and nonnegative integers up to2^63-1 except where a tighter/different bound is documented. The example shows the complete input shape. JSON output includes the supplied identities; review it before sharing sensitive inputs.

## Validate

```sh
python -m unittest -v
python -m compileall -q backup_chain_audit.py
python -m pip wheel --no-deps --wheel-dir dist .
python -m venv /tmp/backup-chain-audit-installed
/tmp/backup-chain-audit-installed/bin/python -m pip install --no-index --no-deps dist/*.whl
python test_installed_cli.py /tmp/backup-chain-audit-installed/bin/python
```

The last commands show the Linux/POSIX path; use the equivalent Scripts/python.exe path on Windows. Remote configured CI uses Linux Python 3.10/3.12/3.14. [Validation](VALIDATION.md) records actual preparation checks and limits; a workflow configuration is not itself proof of a passing run.

## Scope and limitations

Not an adapter for restic, Borg, Duplicati or any backup format. No backup bytes, checksums, encryption, availability, retention calendar or actual restore is verified. Caller-supplied verified=true is evidence to review, not proof. No files are deleted. Empty retain means no preservation roots were requested. Corruption outside selected chains is not exhaustively assessed.

No runtime third-party packages. Setuptools is a build dependency. Original implementation developed with AI assistance, MIT licensed; no competitor code, prose or branding copied. [Research](RESEARCH.md), [contribution](CONTRIBUTING.md), [support](SUPPORT.md) and [security](SECURITY.md) guidance are included.
