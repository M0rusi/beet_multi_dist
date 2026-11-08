from beet.toolchain.helpers import run_beet
from pathlib import Path
import zipfile

TEST_CASE = Path(__file__).parent / "fixtures" / "datapack"


def test_multi_dists(tmp_path: Path):
    with run_beet(
        config={
            "data_pack": {"load": "."},
            "require": ["src.multi_dist"],
            "output": str(tmp_path),
            "meta": {
                "multi_dist": {
                    "dir": {
                        "directory": str(tmp_path)
                    },
                    "zip": {
                        "directory": str(tmp_path),
                        "zipped": True
                    }
                }
            }
        },
        directory=TEST_CASE
    ):
        pass

    assert (tmp_path / "dir").is_dir()
    assert zipfile.is_zipfile(tmp_path / "zip.zip")


def test_template_dist_name(tmp_path: Path):
    with run_beet(
        config={
            "name": "example",
            "version": "1.0.0",
            "data_pack": {"load": "."},
            "require": ["src.multi_dist"],
            "meta": {
                "multi_dist": {
                    "{{ project_name }}_v{{ project_version }}": {
                        "directory": str(tmp_path),
                    },
                    "{{ project_name }}_v{{ project_version }}_{{ mark }}": {
                        "directory": str(tmp_path),
                        "zipped": True
                    }
                },
                "mark": "portable"
            }
        },
        directory=TEST_CASE
    ):
        pass

    assert (tmp_path / "example_v1.0.0").is_dir()
    assert zipfile.is_zipfile(tmp_path / "example_v1.0.0_portable.zip")
