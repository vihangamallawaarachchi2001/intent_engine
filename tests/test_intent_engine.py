import unittest
import tempfile
import os
from intent_engine.arbitration import Arbitrator, IntentData
from intent_engine.blockchain_logger import BlockchainLogger

class TestArbitrator(unittest.TestCase):
    def test_scoring(self):
        arb = Arbitrator()
        intent = IntentData("stop", "safety", "sensor", 1.0, {})
        self.assertEqual(arb.score_intent(intent), 100)

        intent = IntentData("move", "motion", "planner", 0.9, {"obstacle_near": True})
        self.assertEqual(arb.score_intent(intent), 30)

        intent = IntentData("move", "motion", "planner", 0.9, {"obstacle_near": False})
        self.assertEqual(arb.score_intent(intent), 70)

    def test_arbitration(self):
        arb = Arbitrator()
        intents = [
            IntentData("move", "motion", "planner", 0.9, {}),
            IntentData("stop", "safety", "lidar", 1.0, {})
        ]
        winner = arb.arbitrate(intents)
        self.assertEqual(winner.id, "stop")

class TestLogger(unittest.TestCase):
    def test_ledger_chain(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = BlockchainLogger(tmpdir)
            logger.log({"test": 1})
            logger.log({"test": 2})

            ledger_file = os.path.join(tmpdir, "ledger.jsonl")
            with open(ledger_file) as f:
                lines = f.readlines()
            self.assertEqual(len(lines), 2)

            first = eval(lines[0].replace('false', 'False').replace('true', 'True'))
            second = eval(lines[1].replace('false', 'False').replace('true', 'True'))

            self.assertEqual(second["prev_hash"], first["hash"])

if __name__ == '__main__':
    unittest.main()