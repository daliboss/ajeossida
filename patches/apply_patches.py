#!/usr/bin/env python3
"""Apply ajeossida source patches to Frida build"""

import os
import shutil

def apply_patches():
    """Apply string replacement patches to Frida source before compilation"""
    patches = [
        ("libfrida-agent-raw.so", "libajeossida-agent-raw.so"),
        ("re.frida.server", "re.ajeossida.server"),
        ("frida-helper-32", "ajeossida-helper-32"),
        ("frida-helper-64", "ajeossida-helper-64"),
        ("frida-agent-", "ajeossida-agent-"),
        ("frida-server", "ajeossida-server"),
        ("frida-gadget", "ajeossida-gadget"),
        ("gum-js-loop", "ajeossida-js-loop"),
    ]
    
    for root, dirs, files in os.walk('.'):
        for filename in files:
            if filename.endswith(('.c', '.h', '.vala', '.py', '.txt', '.build')):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    for search, replace in patches:
                        content = content.replace(search, replace)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                except Exception:
                    pass

if __name__ == '__main__':
    apply_patches()
    print("[+] Source patches applied")