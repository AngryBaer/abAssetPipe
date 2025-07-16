"""abETL API Module"""
import os
import subprocess
import enum

from abEnvs import EnvSetup, EnvMode
from config import PipePaths

from .core import extract


class ETL(enum.Enum):
    """Enum for ETL processes."""
    ROOT= os.path.dirname(os.path.abspath(__file__))
    CORE = os.path.join(ROOT, "core")
    TRANSFORM = os.path.join(CORE, "transform")
    TYPE = {
        "FBX-USD": os.path.join(TRANSFORM, "fbx_to_usd.py")
    }


def run_extract(archive_name: str, pattern: str = ".fbx"):
    """Extract files from the given archive."""
    zip_file = os.path.join(PipePaths.ARCHIVES.value, archive_name)
    tmp_file = extract.from_archive(zip_file)

    extract.prime_in(tmp_file, pattern)
    extract.cleanup(tmp_file)


def run_transform(app_name: str, process: os.PathLike, dev: bool = False, ):
    """Run the given app in a subprocess."""
    if dev:
        mode = EnvMode.DEV
    else:
        mode = EnvMode.PROD

    configuration = EnvSetup(app_name, mode)
    configuration.setup_envs()
    configuration.setup_paths()

    command = f'"{configuration.executable}" {process}'

    try:
        print(f"Running command: {command}")
        result = subprocess.run(command, check=True, shell=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Subprocess failed!")
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)
        raise


### TEST ###
def test_run_all():
    """Test function to run all ETL processes."""
    # Run extract
    run_extract("fbx_archive.zip", ".fbx")

    # Run transform
    run_transform("hython", dev=True, process=ETL.TYPE.value["FBX-USD"])

    # Load step would go here...
### TEST ###


if __name__ == "__main__":
    test_run_all()
