#!/usr/bin/env python3
"""Apply binary patches to built Frida executables"""

import os
import gzip

def binary_patch(filepath):
    """Apply hex/binary string patches to compiled binary"""
    
    binary_patches = [
        # Thread names
        (b"gmain\x00", b"amain\x00"),
        (b"gdbus\x00", b"gdbug\x00"),
        (b"pool-spawner\x00", b"pool-spoiler\x00"),
        # Symbol names
        (b"frida_agent_main", b"ajeossida_agent_main"),
        (b"frida-server", b"ajeossida-server"),
        (b"libfrida-agent-raw.so", b"libajeossida-agent-raw.so"),
        (b"frida-helper-32", b"ajeossida-helper-32"),
        (b"frida-helper-64", b"ajeossida-helper-64"),
    ]
    
    with open(filepath, 'rb') as f:
        content = f.read()
    
    for search, replace in binary_patches:
        if search in content:
            content = content.replace(search, replace)
    
    with open(filepath, 'wb') as f:
        f.write(content)
    
    # Compress with gzip
    with open(filepath, 'rb') as f_in:
        with gzip.open(filepath + '.gz', 'wb') as f_out:
            f_out.writelines(f_in)
    
    return True

if __name__ == '__main__':
    # Find and patch server binaries
    for root, dirs, files in os.walk('.'):
        for filename in files:
            if 'server' in filename and filename.endswith(('.so', '')):
                filepath = os.path.join(root, filename)
                if binary_patch(filepath):
                    print(f"[+] Patched: {filepath}")
    
    print("[+] Binary patching complete")