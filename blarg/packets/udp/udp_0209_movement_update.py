from collections import deque
from blarg.utils.utils import *

class udp_0209_movement_update:
    def __init__(self):
        pass

    def serialize(self, data: deque):
    	results = {}

    	results['r1'] = data.popleft() # Rotation 1
    	results['cam1_y'] = int(data.popleft(), 16)
    	results['cam1_x'] = int(data.popleft(), 16)
    	results['vcam1_y'] = data.popleft() # Vehicle camera rotation y
    	results['r2'] = data.popleft()
    	results['cam2_y'] = int(data.popleft(), 16)
    	results['cam2_x'] = int(data.popleft(), 16)
    	results['vcam2_y'] = data.popleft() # Vehicle camera rotation y
    	results['r3'] = data.popleft()
    	results['cam3_y'] = int(data.popleft(), 16)
    	results['cam3_x'] = int(data.popleft(), 16)
    	results['v_drv'] = data.popleft() # 1 if the driver of the vehicle, 0 if passenger
    	results['r4'] = data.popleft()
    	results['cam4_y'] = int(data.popleft(), 16)
    	results['cam4_x'] = int(data.popleft(), 16)
    	results['buffer'] = data.popleft()

    	x = short_bytes_to_int(data.popleft(), data.popleft())
    	y = short_bytes_to_int(data.popleft(), data.popleft())
    	z = short_bytes_to_int(data.popleft(), data.popleft())
    	results['coord'] = [x,y,z]

    	results['packet_num'] = int(data.popleft(), 16)
    	results['flush_type'] = int(data.popleft(), 16) # flush type -- if there are buttons or total flush
    	results['last'] = ''.join([data.popleft() for i in range(8)])
    	# Tests
    	# assert results['buffer'] == '00'
    	#assert results['last'] == '8080808080808080'


    	## Parse the button and flush
    	#
    	if results['flush_type'] != 0: # when it's zero, there's no flush or button
    		if len(data) > 17:
    			results['button'] = ''.join([data.popleft() for i in range(len(data)-17)])
    			results['flush'] = ''.join([data.popleft() for i in range(17)])
    		elif len(data) < 17:
    			results['button'] = ''.join([data.popleft() for i in range(len(data))])
    		elif len(data) == 17:
    			results['flush'] = ''.join([data.popleft() for i in range(17)])

    	elif results['flush_type'] == 1:
    		# standard flush
    		results['flush'] = ''.join([data.popleft() for i in range(17)])

    	if results['cam4_x'] == 0 and results['cam4_y'] == 0:
    		results['type'] = 'vehicle movement'
    	else:
    		results['type'] = 'movement'

    	return results
