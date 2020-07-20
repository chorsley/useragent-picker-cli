import pytest
from ua_gen import cli
from ua_gen import consts as c

import subprocess

def capture(command):
    proc = subprocess.Popen(command,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
    )
    out,err = proc.communicate()
    return out, err, proc.returncode

def test_anagram_no_param():
    """
    Should produce a simple UA on no args
    """
    command = ["python3", "dev_runner.py"]
    out, _, exitcode = capture(command)
    assert exitcode == 0
    assert out.decode('utf-8').count('\n') == 1
    assert len(out) > 20
    assert len(out) < 500


def test_list_filters():
    """
    Should produce a simple UA on no args
    """
    command = ["python3", "dev_runner.py", "--list-filters"]
    out, _, exitcode = capture(command)
    outd = out.decode('utf-8')
    assert exitcode == 0
    assert outd.count('\n') > 10
    assert c.UA_PROP_LABELS[c.UA_PLATFORM] in outd


def test_filter():
    """
    Should produce a simple UA on no args
    """
    command = ["python3", "dev_runner.py", "Chrome"]
    out, _, exitcode = capture(command)
    outd = out.decode('utf-8')
    assert exitcode == 0
    assert outd.count('\n') == 1
    assert 'Chrome' in outd


def test_filters():
    """
    Should produce a simple UA on no args
    """
    command = ["python3", "dev_runner.py", "Chrome", "Linux"]
    out, _, exitcode = capture(command)
    outd = out.decode('utf-8')
    assert exitcode == 0
    assert outd.count('\n') == 1
    assert 'Chrome' in outd
    assert 'Linux' in outd
