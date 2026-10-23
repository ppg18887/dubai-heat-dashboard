"""
Split a big dashboard into pieces small enough for GitHub's web upload (limit 25 MB per file).

    python split_dashboard.py dubai_uhi_dashboard_open_models.html

It compresses the file and writes static/dashboard.html.gz.part01, part02, ...
(each about 20 MB). Upload every part to the repository's static folder.
The app joins and unpacks them by itself the first time it starts.
Old parts are removed first so a smaller new file never keeps stale pieces.
"""
import glob
import gzip
import os
import shutil
import sys

PART_BYTES = 20 * 1024 * 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


def main(src: str) -> None:
    os.makedirs(OUT, exist_ok=True)
    for old in glob.glob(os.path.join(OUT, "dashboard.html*")):
        os.remove(old)
    tmp = os.path.join(OUT, "_tmp.gz")
    with open(src, "rb") as f, gzip.open(tmp, "wb", compresslevel=9) as g:
        shutil.copyfileobj(f, g)
    n = 0
    with open(tmp, "rb") as g:
        while True:
            chunk = g.read(PART_BYTES)
            if not chunk:
                break
            n += 1
            with open(os.path.join(OUT, f"dashboard.html.gz.part{n:02d}"), "wb") as p:
                p.write(chunk)
    os.remove(tmp)
    print(f"Wrote {n} part(s) to {OUT}:")
    for p in sorted(glob.glob(os.path.join(OUT, "dashboard.html.gz.part*"))):
        print(f"  {os.path.basename(p)}  {os.path.getsize(p) / 1e6:.1f} MB")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
