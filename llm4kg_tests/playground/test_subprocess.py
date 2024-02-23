import subprocess

def test_java():
    subprocess.run(["java", "-version"])