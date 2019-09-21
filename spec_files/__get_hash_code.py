import hashlib
import sys


"""Print on stadard output the size in KB and sha256 codes of a list
of command line-provided file names."""

print()

try:
    fnames = sys.argv[1:]
except Exception:
    print("Provide a valid filename.")
    exit()

for fname in fnames:
    try:
        with open(fname, mode='rb') as f:
            target = f.read()
    except Exception:
        print("File not found")
        exit()

    code = hashlib.sha256()
    code.update(target)
    hash_code = code.hexdigest()

    print("File name:", fname)
    print("Size (KB):", round(len(target) / 1024, 3))
    print("Hash code:", hash_code)
    print("-" * 80)
