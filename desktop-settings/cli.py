#!/usr/bin/env python3
"""Glasswave Desktop Configuration CLI tool."""

import sys
import json
from pathlib import Path

# Add directory to path
SETTINGS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SETTINGS_DIR))

from settings_manager import SettingsManager, ValidationError

def print_usage():
    print("""Usage: glasswave-config <command> [arguments]

Commands:
    show                    Display full current configuration as JSON
    get <sec> <key>         Get value for specific section and key
    set <sec> <key> <val>   Set value (automatically parses int/float/bool/json)
    reset                   Reset configuration to Glasswave defaults
    backup                  Create an immediate timestamped backup
    export <filepath>       Export configuration to a file
    import <filepath>       Import configuration from a file
    validate                Validate configuration against schema
""")

def parse_val(v_str: str):
    if v_str.lower() == "true":
        return True
    if v_str.lower() == "false":
        return False
    try:
        return int(v_str)
    except ValueError:
        pass
    try:
        return float(v_str)
    except ValueError:
        pass
    try:
        return json.loads(v_str)
    except Exception:
        return v_str

def main():
    if len(sys.argv) < 2:
        print_usage()
        return 1

    cmd = sys.argv[1].lower()
    mgr = SettingsManager()

    if cmd == "show":
        print(json.dumps(mgr.as_dict(), indent=2))
        return 0

    elif cmd == "get":
        if len(sys.argv) < 4:
            print("Error: 'get' requires <section> and <key>", file=sys.stderr)
            return 1
        sec, key = sys.argv[2], sys.argv[3]
        val = mgr.get(sec, key)
        if val is None:
            print(f"Key {sec}.{key} not found", file=sys.stderr)
            return 1
        print(json.dumps(val) if isinstance(val, (dict, list)) else val)
        return 0

    elif cmd == "set":
        if len(sys.argv) < 5:
            print("Error: 'set' requires <section>, <key>, and <value>", file=sys.stderr)
            return 1
        sec, key, v_raw = sys.argv[2], sys.argv[3], sys.argv[4]
        val = parse_val(v_raw)
        try:
            mgr.set(sec, key, val)
            print(f"Updated {sec}.{key} = {val}")
            return 0
        except ValidationError as e:
            print(f"Validation Error: {e}", file=sys.stderr)
            return 1

    elif cmd == "reset":
        mgr.reset_to_defaults()
        print("Glasswave configuration reset to default.")
        return 0

    elif cmd == "backup":
        bk = mgr.backup()
        print(f"Created backup at: {bk}")
        return 0

    elif cmd == "export":
        if len(sys.argv) < 3:
            print("Error: 'export' requires destination filepath", file=sys.stderr)
            return 1
        dest = mgr.export_config(Path(sys.argv[2]))
        print(f"Configuration exported to: {dest}")
        return 0

    elif cmd == "import":
        if len(sys.argv) < 3:
            print("Error: 'import' requires source filepath", file=sys.stderr)
            return 1
        try:
            mgr.import_config(Path(sys.argv[2]))
            print(f"Configuration imported from: {sys.argv[2]}")
            return 0
        except Exception as e:
            print(f"Import Error: {e}", file=sys.stderr)
            return 1

    elif cmd == "validate":
        try:
            mgr.validate(mgr.as_dict())
            print("Configuration is valid according to schema.")
            return 0
        except ValidationError as e:
            print(f"Validation Error: {e}", file=sys.stderr)
            return 1

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        print_usage()
        return 1

if __name__ == "__main__":
    sys.exit(main())
