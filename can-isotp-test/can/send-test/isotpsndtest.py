import isotp
import time

from can.interfaces.vector import VectorBus

isotp_params = {
	#'stmin' : 0,                          # Will request the sender to wait 32ms between consecutive frame. 0-127ms or 100-900ns with values from 0xF1-0xF9
	#'blocksize' : 0,                       # Request the sender to send 8 consecutives frames before sending a new flow control message
	#'wftmax' : 0,                          # Number of wait frame allowed before triggering an error
	#'ll_data_length' : 8,                  # Link layer (CAN layer) works with 8 byte payload (CAN 2.0)
	#'ll_data_length' : 64,                  # Link layer (CAN layer) works with 8 byte payload (CAN 2.0)
	#'tx_padding' : 0xCC,                      # Will pad all transmitted CAN messages with byte 0x00. None means no padding
	#'rx_flowcontrol_timeout' : 1000,        # Triggers a timeout if a flow control is awaited for more than 1000 milliseconds
	#'rx_consecutive_frame_timeout' : 1000, # Triggers a timeout if a consecutive frame is awaited for more than 1000 milliseconds
	#'squash_stmin_requirement' : False,     # When sending, respect the stmin requirement of the receiver. If set to True, go as fast as possible.
	#'can_fd' : True,
	#'tx_data_min_length' : 8
}


bus = VectorBus(channel=0, bitrate=500000)
addr = isotp.Address(isotp.AddressingMode.NormalFixed_29bits, source_address=0xF1, target_address=0x10)
stack = isotp.CanStack(bus, address=addr, params=isotp_params)

#stack.send(b'\x01\x02\x03\x04\x05\x06\x07') 
stack.send(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10') 

while stack.transmitting():
   stack.process()
   time.sleep(0.0001)

bus.shutdown()