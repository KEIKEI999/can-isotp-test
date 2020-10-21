import can

# バス接続
bus = can.interface.Bus(bustype='vector', channel='0', bitrate=500000)

# 受信
while True:
	recv_msg = bus.recv(timeout=1)
	if recv_msg != None:
		print('Recv msg : %s' % recv_msg)
		break


# 送信データ(CANID 0x222、DLC:6、Data：0A 0B 0C 0D 0E 0F)
send_msg = can.Message(arbitration_id=0x222, data=[0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F])
print('Send msg : %s' % send_msg)

# 送信
bus.send( send_msg )


