# Script to acknowledge a hosts' service alert by accessing MK Livestatus
import socket,string,mklivestatus
import sys,splunk.Intersplunk
from datetime import datetime, timedelta

results = []

try:

    results,dummyresults,settings = splunk.Intersplunk.getOrganizedResults()

    for r in results:
        if "_raw" in r:
            if "src_host" in r:
                if "name" in r:
                    try:
		        PORT = mklivestatus.PORT
			nowepoch = datetime.now()
			nowepoch2 = nowepoch.strftime("%s")
		        content = [ "COMMAND [", nowepoch2, "] ACKNOWLEDGE_SVC_PROBLEM;", (r["src_host"]), ";", (r["name"]), ";1;1;0;nagiosadmin;", (r["comment"]), "\n" ]
    		        query = "".join(content)
		        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		        s.connect(((r["host"]), PORT))
		        s.send(query)
		        s.shutdown(socket.SHUT_WR)
		        data = s.recv(100000000)
		        liveserviceack = string.split(data)
		        s.close()
                        r["liveserviceack"] = "Acknowledged"
                    except:
                        r["liveserviceack"] = "Unknown Error"

except:
    import traceback
    stack =  traceback.format_exc()
    results = splunk.Intersplunk.generateErrorResults("Error : Traceback: " + str(stack))

splunk.Intersplunk.outputResults( results )

