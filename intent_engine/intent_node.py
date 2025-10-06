import rclpy
from rclpy.executors import ExternalShutdownException  # ← Add this import
from rclpy.node import Node
from std_msgs.msg import String
import json
from .arbitration import Arbitrator, IntentData
from .blockchain_logger import BlockchainLogger

class IntentEngineNode(Node):
    def __init__(self):
        super().__init__('intent_engine_node')
        self.arbitrator = Arbitrator()
        self.logger = BlockchainLogger()
        self.active_intents = []

        self.subscription = self.create_subscription(
            String,
            '/supun/intents',
            self.intent_callback,
            10
        )
        self.publisher = self.create_publisher(String, '/robot/command', 10)
        self.get_logger().info("Intent Engine Node started. Listening on /supun/intents")

    def intent_callback(self, msg):
        try:
            data = json.loads(msg.data)
            intent = IntentData(
                id=data["id"],
                type=data.get("type", "unknown"),
                source=data.get("source", "unknown"),
                confidence=float(data.get("confidence", 1.0)),
                meta=data.get("meta", {})
            )
            self.get_logger().debug(f"Type of intent: {type(intent)}")
            self.active_intents.append(intent)
            self.get_logger().debug(f"Received intent: {intent.id}")

            # Arbitrate immediately
            winner = self.arbitrator.arbitrate(self.active_intents)
            if winner:
                cmd_msg = String()
                cmd_msg.data = json.dumps({
                    "command": winner.id,
                    "source_intent": winner.id,
                    "score": winner.priority_score
                })
                self.publisher.publish(cmd_msg)
                self.logger.log({
                    "intent": winner.__dict__,
                    "command_issued": winner.id
                })
                # Clear for next cycle (simple model)
                self.active_intents = []

        except Exception as e:
            self.get_logger().error(f"Failed to process intent: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = IntentEngineNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except ExternalShutdownException:
        # ROS 2 context was shut down externally (e.g., by `kill` or Ctrl+C)
        # This is normal during demo shutdown — no action needed.
        pass
    finally:
        node.destroy_node()
        try:
            rclpy.shutdown()
        except:
            pass

if __name__ == '__main__':
    main()