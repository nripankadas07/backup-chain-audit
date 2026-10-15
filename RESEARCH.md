# Candidate brief and comparison — 15 October 2026

**User:** Backup operators reviewing an explicit base/incremental manifest and a retention/deletion proposal.

**Pain and smallest capability:** Deleting one base can strand multiple retained incrementals; total storage can double-count shared ancestors. Trace retained targets to their bases, detect missing/unverified/cyclic ancestry, count shared bytes once and explain deletion blockers.

**Acceptance criteria:** A shared ancestor is counted once; a proposed deletion of base is blocked; missing, unverified and cyclic ancestry withhold deletion eligibility; duplicate identities are rejected.

**Demand evidence:** Inferred operator/developer need, not a verified customer request. Current upstream READMEs, relevant docs/code and accessible issues were inspected. Issue titles below provide context about maintenance and operational work; they are not presented as requests for this tool. No claimed competitor absence is inferred from a successful example here.

**Discovery path:** Accurate repository description/topics, a runnable captured-input example and this evidence file; discoverable by `backup` and the task-specific terms. No unsolicited outreach or activity manipulation.

## Relevant established alternatives found

Live GitHub searches used Most stars ordering; exact queries/URLs/observations are in research-provenance.json. Highest-star relevant comparable found for this bounded workflow: `restic/restic`. Broader collections, tutorials, proxies or unrelated applications in broad results were excluded by relevance; this is not an exhaustive global ranking. Focused invoice-rounding and matrix queries were sparse and broader established tools were retained transparently.

| Comparable | Stars observed | Latest push observed | Archived | API license classification |
| --- | ---: | --- | --- | --- |
| [restic/restic](https://github.com/restic/restic) | 36575 | 2026-10-11T20:17:42Z | False | BSD-2-Clause |
| [duplicati/duplicati](https://github.com/duplicati/duplicati) | 15088 | 2026-10-14T07:43:37Z | False | NOASSERTION |
| [borgbackup/borg](https://github.com/borgbackup/borg) | 13840 | 2026-10-14T20:02:25Z | False | NOASSERTION |

Observations are dated in research-provenance.json, including README blob hashes and accessible issue links. NOASSERTION means the API did not classify the license; upstream terms must be read before reuse. No upstream source was incorporated.

restic and Borg provide encrypted/deduplicated backup workflows; Duplicati is an incremental backup client with remote targets. Those operational engines are broader than this explicit parent-manifest review contract. We have not shown that any lacks equivalent retention inspection. Borg master README identifies unstable Borg2 beta; stable version support must be checked separately.

Installation and first-use paths were inspected in current documentation, not benchmarked. These alternatives provide broader workflows, operational reliability features, docs/examples and support communities. This tool offers a bounded file/JSON contract, explicit failure modes and runnable fixtures but lacks their broader product capabilities, adoption evidence and maintenance history. Our build/install example measures only our behavior. Competitor installs, time-to-first-result, reliability and technical performance were not measured; no superiority claim or numerical performance comparison is made. Stars inform discovery, not quality or speed.

## Portfolio and candidate distinctness

Distinct from git-ref-retention (Git reachability), oci-whiteout-plan (container layers) and s3-expiry-witness (object lifecycle eligibility): this checks declared backup restoration dependencies and preservation roots.

All 178 owned repository identities/descriptions and the current project index were compared. Related release-asset-matrix, table-reconcile, sqlite-rehearsal and traceweave READMEs were inspected. The five candidates have separate users/contracts: backup dependency preservation, Kafka recovery positions, tax allocation arithmetic, span ancestry/interval coverage and CI matrix inclusion provenance. They are independent tools, not renamed/forked/subdivided versions of one product. Shared JSON CLI and packaging scaffolding does not substitute for their distinct algorithms and tests.
