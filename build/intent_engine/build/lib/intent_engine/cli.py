import argparse
import json
import subprocess
from pathlib import Path

def inject_intent(args):
    intent = {
        "id": args.id,
        "type": args.type,
        "source": "cli",
        "confidence": args.confidence,
        "meta": json.loads(args.meta) if args.meta else {}
    }

    # Wrap in 'data' field for std_msgs/String
    message = {"data": json.dumps(intent)}
    cmd = [
        "ros2", "topic", "pub", "--once", "/supun/intents",
        "std_msgs/msg/String",
        json.dumps(message)
    ]
    subprocess.run(cmd)

def tail_ledger(args):
    ledger = Path("logs/ledger.jsonl")
    if not ledger.exists():
        print("Ledger not found. Run the node first.")
        return
    with open(ledger, "r") as f:
        lines = f.readlines()
        for line in lines[-args.n:]:
            print(json.dumps(json.loads(line), indent=2))

def main():
    parser = argparse.ArgumentParser(prog="intent_cli")
    subparsers = parser.add_subparsers()

    # inject
    p_inject = subparsers.add_parser("inject", help="Publish an intent")
    p_inject.add_argument("id", help="Intent ID (e.g., stop, move)")
    p_inject.add_argument("--type", default="motion")
    p_inject.add_argument("--confidence", type=float, default=1.0)
    p_inject.add_argument("--meta", default="{}")
    p_inject.set_defaults(func=inject_intent)

    # tail
    p_tail = subparsers.add_parser("tail", help="Show last N ledger entries")
    p_tail.add_argument("-n", type=int, default=5)
    p_tail.set_defaults(func=tail_ledger)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()