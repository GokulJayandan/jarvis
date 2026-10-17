"""Idempotent prose-only overlay after historical report regeneration/CI overlay."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    old='The official submission issue has not been created; it requires separate authorization. This documentation revision also awaits authorization to push.'
    new='Final hardening status, expanded contract tests, release fixes, and current Docker evidence are recorded in `docs/FINAL_HARDENING_AUDIT.md`. The official submission issue is prepared separately and has not been posted.'
    for name in ('README.md','report/TECHNICAL_REPORT.md','docs/RECOVERY_RELEASE.md'):
        path=ROOT/name;text=path.read_text(encoding='utf-8').replace(old,new)
        text=text.replace('Docker execution is blocked on this host; this build must not be represented as submission-ready until that gate passes.',
            'At the original study date Docker was absent on the Windows host. That historical blocker was subsequently cleared for the released V1_greedy by verified Linux CI; see the current release audit above.')
        text=text.replace('The optional website was not started because mandatory Docker verification remains blocked.',
            'No website is part of this submission. Historical Docker failures are superseded by the verified Linux CI evidence in the current release audit.')
        path.write_text(text,encoding='utf-8')

if __name__=='__main__':main()
