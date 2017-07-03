
# coding: utf-8

# # Real Time Myo
# 
# Display myo data in real time
# 
# ## Notes
# * Need to have Myo Connect running otherwise you get random errors

# In[1]:


from __future__ import print_function
import collections
import myo
import threading
import time

myo.init()  # Init doesn't like being rerun


# In[10]:


class MyListener(myo.DeviceListener):
    def __init__(self, queue_size=200):
        self.lock = threading.Lock()
        self.emg_data_queue = collections.deque(maxlen=queue_size)
        
    def on_pair(self, myo, *args):
        print("Paired")

    def on_connect(self, device, timestamp, firmware_version):
        device.set_stream_emg(myo.StreamEmg.enabled)
        print("Connected")
        
    def on_arm_sync(self, myo, *args):
        print("Arm Synced")

    def on_emg_data(self, device, timestamp, emg_data):
        with self.lock:
            self.emg_data_queue.append((timestamp, emg_data))

    def get_emg_data(self):
        with self.lock:
            return list(self.emg_data_queue)


hub = myo.Hub()
try:
    listener = MyListener()
    hub.run(100, listener)
    while True:
        print(len(listener.get_emg_data()))
        time.sleep(1.0)
finally:
    hub.shutdown()

