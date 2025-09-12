import os
import pytest
from loaders.iterator import ResumableIterator  # adjust import to your project



file_dict = {
    "a": "file1.txt",
    "b": "file2.txt",
    "c": "error_file.txt",  # will simulate error
    "d64": "file3.txt",
    "a64": "file1.txt",
    "b64": "file2.txt",
    # "c64": "error_file.txt",  # will simulate error
    "d64": "file3.txt",
    "as64": "file1.txt",
    "b6s4": "file2.txt",
    # "c64d": "error_file.txt",  # will simulate error
    "dd64": "file3.txt",
    "a6gf4": "file1.txt",
    "b6gf4": "file2.txt",
    # "c6gf4": "error_file.txt",  # will simulate error
    "d64fxd": "file3.txt",
    "a64gb": "file1.txt",
    "b6b4": "file2.txt",
    # "c64x": "error_file.txt",  # will simulate error
    "d64e": "file3.txt",
    "ar64": "file1.txt",
    "b6t4": "file2.txt",
    # "c464": "error_file.txt",  # will simulate error
    "d64": "file3.txt",
    "a624": "file1.txt",
    "b645": "file2.txt",
    # "c642": "error_file.txt",  # will simulate error
    "d6413": "file3.txt",
    "a64321": "file1.txt",
    "b64985": "file2.txt",
    # "c6478": "error_file.txt",  # will simulate error
    "d6884": "file3.txt",
    "a674": "file1.txt",
    "b6499": "file2.txt",
    # "c64789": "error_file.txt",  # will simulate error
    "d647894": "file3.txt",
}
def process_file(path):
    sleep(0.3)
    if "error" in path:
        raise ValueError("Simulated failure")
    return f"Processed {path}"


def test_resumable_iterator(tmp_path):
    checkpoint = tmp_path / "progress.json"

    runner = ResumableIterator(file_dict.values(), checkpoint=str(checkpoint), batch_size=2)

    # First run: should stop at error_file.txt
    runner.run(process_file)
    done_after_first = runner.done
    assert "file1.txt" in done_after_first
    assert "file2.txt" in done_after_first
    assert "error_file.txt" not in done_after_first

    # Second run: should resume and finish remaining files
    runner.run(process_file)
    done_after_second = runner.done
    assert "file3.txt" in done_after_second
    assert len(done_after_second) == 3  # all except error_file.txt
