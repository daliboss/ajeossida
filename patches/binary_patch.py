#!/usr/bin/env python3
"""Apply ajeossida stealth binary patches to Frida server executables"""

import gzip
import os
import sys

BINARY_PATCHES = [
    # Agent entry point
    (b"frida_agent_main", b"ajeossida_agent_main"),
    # Server binary name references
    (b"frida-server", b"ajeossida-server"),
    # Agent library
    (b"libfrida-agent-raw.so", b"libajeossida-agent-raw.so"),
    # Helper binaries
    (b"frida-helper-32", b"ajeossida-helper-32"),
    (b"frida-helper-64", b"ajeossida-helper-64"),
    # Thread names
    (b"pool-frida", b"pool-ajeossida"),
    (b"pool-spawner\x00", b"pool-spoiler\x00"),
    # Event loop thread name
    (b"gum-js-loop", b"ajeossida-js-loop"),
    # GLib thread names (null-padded to keep same length)
    (b"gmain\x00", b"amain\x00"),
    (b"gdbus\x00", b"gdbug\x00"),
]


def patch_binary(filepath):
    """Apply stealth patches to a Frida binary"""
    print(f"[*] Patching: {filepath}")

    with open(filepath, "rb") as f:
        content = f.read()

    patched = False
    for search, replace in BINARY_PATCHES:
        count = content.count(search)
        if count > 0:
            content = content.replace(search, replace)
            print(f"    {search.decode(errors='replace')} → {replace.decode(errors='replace')} ({count} occurrences)")
            patched = True

    if patched:
        with open(filepath, "wb") as f:
            f.write(content)
        print(f"[+] Binary patched successfully")
    else:
        print(f"[!] No patches applied (strings not found)")

    return patched


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 binary_patch.py <binary_path> [binary_path2 ...]")
        sys.exit(1)

    for binary_path in sys.argv[1:]:
        if os.path.isfile(binary_path):
            patch_binary(binary_path)
        else:
            print(f"[!] File not found: {binary_path}")

    print("[+] Done")