import can

# バス接続
bus = can.interface.Bus(bustype='vector', channel='0', bitrate=500000)

# 受信
while True:
	recv_msg = bus.recv(timeout=1)
	if recv_msg != None:
		print('Recv msg : %s' % recv_msg)
		break


send_msg = can.Message(arbitration_id=0x18daF110, extended_id=1, data=[0x30, 0x00, 0x0A, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC])
print('Send msg : %s' % send_msg)

# 送信
bus.send( send_msg )

