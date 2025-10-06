#!/bin/bash
set -e

echo "Starting demo..."

# Start node
python3 -m intent_engine.intent_node > node.log 2>&1 &
PID=$!
sleep 2

if ! kill -0 $PID 2>/dev/null; then
    echo "ERROR: Node failed to start!"
    cat node.log
    exit 1
fi

echo "Injecting intents..."
python3 -m intent_engine.cli inject move --meta '{"obstacle_near": false}'
sleep 1
python3 -m intent_engine.cli inject stop
sleep 1
python3 -m intent_engine.cli inject call_nurse

sleep 2
kill $PID 2>/dev/null || true

echo "=== NODE LOG ==="
cat node.log

echo -e "\n=== LEDGER (last 3 entries) ==="
python3 -m intent_engine.cli tail -n 3

echo "Demo completed successfully!"