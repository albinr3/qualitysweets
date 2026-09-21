"""Backward-compatible entry point for the unified Catering deployment.

Use deploy_catering_hub_2_4.py as the canonical deployment script.
"""

from deploy_catering_hub_2_4 import main


if __name__ == "__main__":
    raise SystemExit(main())
