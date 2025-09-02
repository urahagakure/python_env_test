# R3/R6: 状態を一目で把握する簡易ヘルスチェック
import shutil  # R3
import subprocess  # R3
import sys  # R3


def which(cmd: str) -> str:  # R3
    p = shutil.which(cmd)  # R3
    return p or "NOT FOUND"  # R3


def run(cmd: list[str]) -> str:  # R3
    try:  # R3
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)  # R3
        return out.decode().strip()  # R3
    except Exception as e:  # R3
        return f"ERR: {e}"  # R3


print("== Healthcheck ==")  # R6
print(f"python  : {sys.executable}")  # R3
print(f"pyenv   : {which('pyenv')}")  # R3
print(f"poetry  : {which('poetry')}")  # R3
print(f"git     : {which('git')}")  # R3

print("\n-- Git --")  # R3
print("branch  :", run(["git", "rev-parse", "--abbrev-ref", "HEAD"]))  # R3
print("remote  :", run(["git", "remote", "-v"]))  # R3
print("status  :", run(["git", "status", "-s"]))  # R3

print("\n-- Poetry --")  # R3
print("venv    :", run(["poetry", "env", "info", "-p"]))  # R3
print("deps ok?:", run(["poetry", "check"]))  # R3

print("\nOK: 異常がなければこのまま開発を開始してください")  # R6
