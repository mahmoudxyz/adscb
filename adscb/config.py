"""Package-level configuration constants.

Edit `REPO_URL` if you fork the project. Everything else is derived.
"""
from pathlib import Path

REPO_URL = "https://github.com/mahmoudxyz/adscb.git"

# Local clone location — separate from workspace/ and progress.json
# so users can nuke it (or `adscb sync`) without losing their solutions.
USER_HOME = Path.home() / ".adscb"
REPO_DIR = USER_HOME / "repo"

# Path inside the repo where problem files live, relative to REPO_DIR.
PROBLEMS_SUBPATH = Path("adscb") / "problems"
