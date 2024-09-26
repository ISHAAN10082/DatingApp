import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.absolute()

# Add project root to sys.path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print("Python path:", sys.path)