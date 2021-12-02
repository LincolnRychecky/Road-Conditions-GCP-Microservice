#!/usr/bin/env python3

#
# The example sends a single JSON formatted request to the worker
# using the RabbitMQ message queues assuming you are port-forwarding
# the requests to the host on which you run this.
#
# The request defines a model and a sentences list containing multiple sentences.
#
import io,os
import sys, platform
import pika
import json
import datetime as date

#
# Unless you have set the RABBITMQ_HOST environment variable, use localhost
#
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

#
# This is the payload format used in the solution. It doesn't specify a callback,
# so you'll need to test that out another way or modify this example.
#

workerJson = {'path': [{'distance': {'text': '6.9 mi', 'value': 11132},
  'duration': {'text': '14 mins', 'value': 846},
  'duration_in_traffic': {'text': '14 mins', 'value': 838},
  'end_address': '6675 Business Center Dr, Highlands Ranch, CO 80130, USA',
  'end_location': {'lat': 39.5614035, 'lng': -104.9120432},
  'start_address': '908 Graland Pl, Littleton, CO 80126, USA',
  'start_location': {'lat': 39.5279359, 'lng': -104.9784726},
  'steps': [{'distance': {'text': '272 ft', 'value': 83},
    'duration': {'text': '1 min', 'value': 10},
    'end_location': {'lat': 39.5284896, 'lng': -104.9791145},
    'html_instructions': 'Head <b>northwest</b> on <b>Graland Pl</b> toward <b>Graland Ln</b>',
    'polyline': {'points': 'shgpFlrv_S?Bw@~@a@h@SP'},
    'start_location': {'lat': 39.5279359, 'lng': -104.9784726},
    'travel_mode': 'DRIVING'},
   {'distance': {'text': '0.2 mi', 'value': 256},
    'duration': {'text': '1 min', 'value': 48},
    'end_location': {'lat': 39.5282081, 'lng': -104.9817812},
    'html_instructions': 'Turn <b>left</b> onto <b>Ridgemont Cir</b>',
    'maneuver': 'turn-left',
    'polyline': {'points': 'algpFlvv_Sb@v@JNn@bBFb@Hj@@P?H?P?~@QhAALKZIVQ^'},
    'start_location': {'lat': 39.5284896, 'lng': -104.9791145},
    'travel_mode': 'DRIVING'},
   {'distance': {'text': '325 ft', 'value': 99},
    'duration': {'text': '1 min', 'value': 14},
    'end_location': {'lat': 39.5275416, 'lng': -104.9822879},
    'html_instructions': 'Turn <b>left</b> onto <b>Pennington St</b>',
    'maneuver': 'turn-left',
    'polyline': {'points': 'ijgpFbgw_SIRHJPPLJDBHFNFVFHBF@ZD'},
    'start_location': {'lat': 39.5282081, 'lng': -104.9817812},
    'travel_mode': 'DRIVING'},
   {'distance': {'text': '3.4 mi', 'value': 5514},
    'duration': {'text': '6 mins', 'value': 356},
    'end_location': {'lat': 39.5426989, 'lng': -104.9354161},
    'html_instructions': 'Turn <b>left</b> at the 1st cross street onto <b>E Wildcat Reserve Pkwy</b>',
    'maneuver': 'turn-left',
    'polyline': {'points': 'cfgpFhjw_SR@@[J_C?KBm@NsDLyDHoB@i@Bo@@Y?Y@i@?[?kA?W?kE?u@?_C@a@?UH}@Fw@BUHa@H_@ReAp@{Cj@aCJi@Lu@Jq@JaAFo@TwCDe@JwADi@Dc@L_AF_@TmAF_@Pu@\\qAb@mADa@z@kCRq@F[ZsATqAT]B_@NqB@WB_@Bs@Bu@?A@wA?eAC_B?WAgAAg@A}AA{ACyEA}A?s@GaH?}@AmAAs@CkC?k@C}DAsBAm@E{DCeEAeAC}CA{CEkDCiBKkBC]Gy@IgA?AY_CQkASgAe@sB[kA_@uAk@}AUk@GMMUWk@k@iAMUUa@c@q@IO]g@cB_Ca@a@QS[[UUEEm@i@MKWUUO_@WmBmAc@So@[k@YEA[Mg@OOG{@Wi@MUEo@Oc@G]EYE_@EQCWAKASAc@CI?YAC?[AC?_@?I?]?M?c@?Q?Q?M?UCQAWEWEc@Ke@QA?_@OMGECKEg@UYMSKOG{@a@{@_@{@a@_Aa@s@[EC{@a@YM[OMEOGOEMEe@I[GWCQAw@K_AIaAK}@Ki@O[KECo@We@Ui@Ug@Sk@UOEMEOFA@WE_@Em@EI?yAEI?u@AGAW?gAC'},
    'start_location': {'lat': 39.5275416, 'lng': -104.9822879},
    'travel_mode': 'DRIVING'},
   {'distance': {'text': '1.2 mi', 'value': 1981},
    'duration': {'text': '2 mins', 'value': 134},
    'end_location': {'lat': 39.5419601, 'lng': -104.9135294},
    'html_instructions': 'Turn <b>right</b> onto <b>S University Blvd</b>',
    'maneuver': 'turn-right',
    'polyline': {'points': '{djpFjen_SBcCByDJeA@_@BcD@YBiC?CBkCAaAE}@Cw@Gy@I{@Eg@SwAyCqS_@eCIm@_@gCYmBCWKw@Ky@C_@Ec@Gu@GsACw@Ay@AY?_@?{@?m@@o@?OB_@@WDkA?EFu@Ba@BWH{@Fi@DW`@gCD[Li@Ps@XcA^mAVs@Tq@Pa@BGHQP_@N]LWP[Xi@NYpBaD'},
    'start_location': {'lat': 39.5426989, 'lng': -104.9354161},
    'travel_mode': 'DRIVING'},
   {'distance': {'text': '1.6 mi', 'value': 2504},
    'duration': {'text': '3 mins', 'value': 190},
    'end_location': {'lat': 39.5605445, 'lng': -104.9043118},
    'html_instructions': 'Turn <b>left</b> onto <b>S Quebec St</b>',
    'maneuver': 'turn-left',
    'polyline': {'points': 'g`jpFp|i_SNWQUaAoA}@gAgAsAsAaBOQKIIIIIGGSQAAYWUQKGCCYSOKi@[ECg@Wk@Uc@OYIi@OEAg@O}@S_@Cy@Ie@CgAAU?m@@C?gBNC?wB^mEt@SBmC\\}OfCaANgAN{@LS@}@D_@COAMCc@GUEkAc@MEA?IGOISOWUSSOQKKOQo@_Au@qBMa@e@gBkAqE[cAk@yBCKg@iBSq@Sk@EIKWQ[S]a@k@w@w@GGGG[USOMGw@_@]OYISEYEK?uAI'},
    'start_location': {'lat': 39.5419601, 'lng': -104.9135294},
    'travel_mode': 'DRIVING'},
   {'distance': {'text': '0.4 mi', 'value': 695},
    'duration': {'text': '2 mins', 'value': 94},
    'end_location': {'lat': 39.5614035, 'lng': -104.9120432},
    'html_instructions': 'Turn <b>left</b> onto <b>Business Center Dr</b><div style="font-size:0.9em">Destination will be on the right</div>',
    'maneuver': 'turn-left',
    'polyline': {'points': 'ktmpF|bh_S[?Al@Bl@@l@?HBbADtALVD|@@\\DbCAv@?\\Cn@Ef@ABI~@ABANIt@CTIh@Gh@CTQlA_@xC}@hGGd@AN'},
    'start_location': {'lat': 39.5605445, 'lng': -104.9043118},
    'travel_mode': 'DRIVING'}],
  'traffic_speed_entry': [],
  'via_waypoint': []}]
            }

rabbitMQ = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitMQHost))
rabbitMQChannel = rabbitMQ.channel()

#
# Define or rabbitMQ queues / exchanges
#
rabbitMQChannel.queue_declare(queue='toWeatherWorker')
rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')
infoKey = f"{platform.node()}.worker.info"
debugKey = f"{platform.node()}.worker.debug"
#
# A helpful function to send a log message
#
def log_debug(message, key=debugKey):
    print("DEBUG:", message, file=sys.stderr)
    rabbitMQChannel.basic_publish(
        exchange='logs', routing_key=key, body=message)

formattedJson = json.dumps(workerJson)
# log_debug(f"Sending request {formattedJson}")
rabbitMQChannel.basic_publish(exchange='',routing_key='toWeatherWorker', body=formattedJson)
