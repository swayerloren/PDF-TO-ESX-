from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parent
src_dir = repo_root / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from pdf_to_esx_agent.app.bootstrap import main


if __name__ == "__main__":
    raise SystemExit(main())
