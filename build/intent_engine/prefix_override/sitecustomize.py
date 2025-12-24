import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/vk/ros2_ws/src/intent_engine/install/intent_engine'
