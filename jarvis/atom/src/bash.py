from __future__ import annotations
import sys

sys.dont_write_bytecode = True
from typing import Union, Optional
from subprocess import run, PIPE


class Output:
    def __init__(self, stdout: str, stderr: str):
        self.stdout = stdout
        self.stderr = stderr

    def observe(self):
        if self.stdout == "" and self.stderr != "":
            raise RuntimeError(self.stderr)
        else:
            return self.stdout

    def __str__(self):
        print([self.stdout, self.stderr])
        return self.stdout + self.stderr


class Bash:
    def __init__(self, cmd: str, stdin: Optional[str]=None):
        self.cmd = cmd
        self.stdin = stdin

    def __call__(self, *arg) -> str:
        result = run(
            [self.cmd, *arg],
            input=self.stdin,
            capture_output=True,
            text=True
        )
        return Output(result.stdout, result.stderr)


class Promise():
    def __init__(self, stdin: Optional[str]=None):
        self.stdin = stdin
        self.stash = None
        self.stdout = None

    def then(self, bash: Union[str, Bash], *arg) -> Promise:
        if type(bash) == str:
            bash = Bash(bash)
        self.stash = bash
        self.stash.stdin = self.stdout if self.stdout != None else self.stdin
        return self.__call__(*arg) if len(arg) > 0 else self

    def observe(self) -> str:
        return self.stdout.strip("\n")

    def __call__(self, *arg) -> Promise:
        if self.stash != None:
            self.stdout = self.stash(*arg).observe()
            self.stash = None
            return self
        else:
            return self.observe()


Pkexec = \
    lambda cmd: \
    lambda *arg: \
        Bash("pkexec")(cmd, *arg)

Pkexec_GUI = \
    lambda cmd: \
    lambda *arg: \
        Bash("pkexec")(
            "env",
            "DISPLAY=$DISPLAY",
            "XAUTHORITY=$XAUTHORITY",
            cmd,
            *arg
        )
