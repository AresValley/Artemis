import hashlib
from pandas import read_csv

def checksum_ok(data, what):
    code = hashlib.sha256()
    code.update(data)
    ref_loc = 'https://aresvalley.com/Storage/Artemis/Database/data.zip.log'
    if what == "folder":
        n = 0
    elif what == "db":
        n = 1
    else:
        raise ValueError("Wrong entry name.")
    try:
        reference = read_csv(ref_loc, delimiter = '*').iat[-1, n]
    except HTTPError:
        return False
    return code.hexdigest() == reference