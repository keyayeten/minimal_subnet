import subprocess
import pathlib
import pytest


@pytest.fixture
def correct_ipv4_file(request):
    path = pathlib.Path("ipv4.txt")
    rows = [
        f"0.0.0.{i}\n" for i in range(1, 10)
    ]
    with open(path, "w") as f:
        f.writelines(rows)

    def finalize():
        path.unlink(missing_ok=True)

    request.addfinalizer(finalize)
    return path


def test_command_line_functionality(correct_ipv4_file, capfd):
    command = f'minimal_subnet "{correct_ipv4_file}" "ipv4"'

    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    captured = capfd.readouterr()

    assert "0.0.0.0/28" in captured.err
    assert not error
