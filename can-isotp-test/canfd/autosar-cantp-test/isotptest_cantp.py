import isotp
import logging
import time
import threading

from can.interfaces.vector import VectorBus

class ThreadedApp:
   def __init__(self):
      isotp_params = {
         'stmin' : 0, 
         'blocksize' : 0,
         'wftmax' : 0,
         'll_data_length' : 64,
         'tx_padding' : 0xCC,
         'rx_flowcontrol_timeout' : 1000,
         'rx_consecutive_frame_timeout' : 1000,
         'squash_stmin_requirement' : False,
         'can_fd' : True,
         'tx_data_min_length' : 8,
         'max_frame_size' : 65535
      }
      self.exit_requested = False
      #self.bus = VectorBus(channel='0', bitrate=500000)
      self.bus = VectorBus(channel='0', bitrate=500000, fd=True)
      addr = isotp.Address(isotp.AddressingMode.NormalFixed_29bits, source_address=0xF1, target_address=0x10) 
      self.stack = isotp.CanStack(self.bus, address=addr, params=isotp_params, error_handler=self.my_error_handler)

   def start(self):
      self.exit_requested = False
      self.thread = threading.Thread(target = self.thread_task)
      self.thread.start()

   def stop(self):
      self.exit_requested = True
      if self.thread.isAlive():
         self.thread.join()
   
   def send(self, msg):
      self.stack.send(msg)
   
   def my_error_handler(self, error):
      logging.warning('IsoTp error happened : %s - %s' % (error.__class__.__name__, str(error)))

   def thread_task(self):
      while self.exit_requested == False:
         self.stack.process()                # Non-blocking
         #time.sleep(self.stack.sleep_time()) # Variable sleep time based on state machine state
         time.sleep(0.001) # Variable sleep time based on state machine state

   def shutdown(self):
      self.stop()
      self.bus.shutdown()

def sendrecv( app, msg ):
   print("Send msg : %s" % (msg.hex()))
   app.send(msg)
   t1 = time.time()
   while time.time() - t1 < 5:
      if app.stack.available():
         payload = app.stack.recv()
         print("Recv msg : %s" % (payload.hex()))
         break
      time.sleep(0.2)


if __name__ == '__main__':
   app = ThreadedApp()
   app.start()
   
   datas=[
      bytes([0x22, 0x56, 0x78]),
      bytes([0x22, 0x56, 0x78, 0x56, 0x78, 0x56, 0x78, 0x56, 0x78]),
      bytes([0x22, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34, 0x12, 0x34]),
   ]
   
   for i in range(len(datas)):
      sendrecv(app, datas[i])

   print("Exiting")
   app.shutdown()