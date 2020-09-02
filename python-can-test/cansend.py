import can

# バス接続
bus = can.interface.Bus(bustype='vector', channel='0', bitrate=500000)

# 送信データ(CANID 0x111、DLC:8、Data：01 02 03 04 05 06 07 08)
send_msg = can.Message(arbitration_id=0x111, extended_id=1, data=[0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])
print('Send msg : %s' % send_msg)
# 送信
bus.send( send_msg )

# 受信
recv_msg = bus.recv(timeout=1)
print('Recv msg : %s' % recv_msg)

