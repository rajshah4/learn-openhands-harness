#!/usr/bin/env python3
"""Build a deterministic student ZIP using an explicit public-file allowlist."""
from pathlib import Path
import hashlib
import zipfile
from setup_examples import ROOT, verify


def main():
    verify(ROOT / 'package')
    out = ROOT / 'dist'
    out.mkdir(exist_ok=True)
    target = out / 'harness-conversations-2026-10-18.zip'
    names = ['README.md', 'setup_examples.py', 'prepare_runtime.py', 'view_canvas.py', 'serve_transcripts.py']
    files = [ROOT / n for n in names] + sorted((ROOT / 'package').rglob('*'))
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            if path.is_symlink():
                raise ValueError('Symlinks are forbidden')
            if not path.is_file():
                continue
            info = zipfile.ZipInfo('harness-conversations/' + path.relative_to(ROOT).as_posix(), (2026, 10, 18, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compresslevel=9)
    checksum = hashlib.sha256(target.read_bytes()).hexdigest()
    (out / 'SHA256SUMS.txt').write_text(checksum + '  ' + target.name + '\n')
    print(target)
    print(checksum)


if __name__ == '__main__':
    main()
