# *- coding: utf-8 -*-

import sys
import subprocess
import semantic_version

MAIN_BRANCH = 'main'
MAX_PATCH = 40
MAX_MINOR = 30


def new_version():
    command = ["git", "--no-pager", "tag"]

    rc = subprocess.run(command, capture_output=True)

    if rc.returncode != 0:
        print(rc.stderr.decode())
        sys.exit(rc.returncode)

    tags = rc.stdout.decode().strip().split('\n')
    print("version tags:", tags)

    versions = []

    for tag in tags:
        try:
            v=semantic_version.Version(tag)
            versions.append(v)
        except ValueError:
            continue

    versions.sort()

    latestVer = versions[-1]
    print("got latest version:", latestVer)

    major, minor, patch = latestVer.major, latestVer.minor, latestVer.patch

    if patch > MAX_PATCH:
        minor += 1
        patch = 0
    elif minor > MAX_MINOR:
        major += 1
        minor = 0
    else:
        patch += 1

    print("got new version:", major, minor, patch)

    return semantic_version.Version(major=major, minor=minor, patch=patch)


def release():
    v = new_version()

    branch = "release-{}.{}.{}".format(v.major, v.minor, v.patch)
    tag = "{}.{}.{}-rc.0".format(v.major, v.minor, v.patch)

    commands = [
        ['git', 'checkout', MAIN_BRANCH],
        ['git', 'checkout', '-b', branch],
        ['git', 'push', 'origin', branch],
        ['git', 'tag', tag, '-m', 'new release rc'],
        ['git', 'push', 'origin', tag],
        ['git', 'checkout', MAIN_BRANCH]
    ]

    print("---------------- release ----------------")
    print("branch:", branch)
    print("tag:", tag)

    for command in commands:
        print('command: ', command)
        rc = subprocess.run(command, capture_output=True)

        if rc.returncode != 0:
            print(rc.stderr.decode())
            sys.exit(rc.returncode)

        print(rc.stdout.decode())


if __name__ == '__main__':
    release()
