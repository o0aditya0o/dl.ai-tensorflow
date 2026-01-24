import tensorflow as tf
import sys

print(f"TensorFlow Version: {tf.__version__}")

# 1. Check for the specific plugin package availability
try:
    import tensorflow_metal
    print(f"tensorflow-metal is installed? YES (Version: {tensorflow_metal.__version__ if hasattr(tensorflow_metal, '__version__') else 'unknown'})")
except ImportError:
    print("tensorflow-metal is installed? NO")

# 2. Check Physical Devices
devices = tf.config.list_physical_devices()
print("\nPhysical Devices found:")
for d in devices:
    print(f"  - {d.device_type}: {d.name}")

gpus = tf.config.list_physical_devices('GPU')
if not gpus:
    print("\n[FAIL] No GPUs detected. tensorflow-metal might not be initializing correctly.")
    print("Please try: pip install tensorflow-metal")
    sys.exit(1)
else:
    print(f"\n[SUCCESS] {len(gpus)} GPU(s) detected.")
    print("The 'tensorflow-metal' plugin automatically registers these devices when TensorFlow initializes.")
    print("You do NOT need to 'import tensorflow_metal' in your code.")

# 3. Simple Compute Test
print("\nRunning test computation on GPU...")
try:
    with tf.device('/GPU:0'):
        a = tf.constant([1.0, 2.0, 3.0])
        b = tf.constant([4.0, 5.0, 6.0])
        c = a * b
        print(f"Computation Result: {c.numpy()}")
        print("Test computation successful.")
except Exception as e:
    print(f"Computation failed: {e}")
