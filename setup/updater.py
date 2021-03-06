# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import create_subprocess_exec, get_event_loop
from asyncio.subprocess import PIPE
from difflib import unified_diff
from shlex import split
from sys import argv
from typing import Tuple


async def lines_differnce(file1, file2):
    with open(file1) as f1:
        lines1 = f1.readlines()
        lines1 = [line.rstrip("\n") for line in lines1]
    with open(file2) as f2:
        lines2 = f2.readlines()
        lines2 = [line.rstrip("\n") for line in lines2]
    diff = unified_diff(lines1, lines2, fromfile=file1, tofile=file2, lineterm="", n=0)
    lines = list(diff)[2:]
    added = [line[1:] for line in lines if line[0] == "+"]
    removed = [line[1:] for line in lines if line[0] == "-"]
    additions = [i for i in added if i not in removed]
    removedt = [i for i in removed if i not in added]
    return additions, removedt


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = split(cmd)
    process = await create_subprocess_exec(*args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def update_requirements(main, test):
    a, r = await lines_differnce(main, test)
    try:
        for i in a:
            await runcmd(f"pip install {i}")
            print(f"Succesfully installed {i}")
    except Exception as e:
        print(f"Error while installing requirments {str(e)}")


loop = get_event_loop()
loop.run_until_complete(update_requirements(argv[1], argv[2]))
loop.close()
