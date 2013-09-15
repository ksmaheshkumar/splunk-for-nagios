# Script to request hosts with DOWN status and total hosts by accessing MK Livestatus
# Required field to be passed to this script from Splunk: host (mk-livestatus/nagios server)
import socket,string,sys,splunk.Intersplunk,mklivestatus

results = []

try:

    results,dummyresults,settings = splunk.Intersplunk.getOrganizedResults()

    for r in results:
        if "_raw" in r:
            if "host" in r:
                    try:
			HOST = mklivestatus.HOST
		        PORT = mklivestatus.PORT
		        livehostsdown = 0
		        livehoststotal = 0
    			for h in HOST:
			    content = [ "GET hosts\nStats: state = 1\nStats: state != 9999\n" ]
			    query = "".join(content)
			    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			    s.connect((h, PORT))
			    s.send(query)
			    s.shutdown(socket.SHUT_WR)
			    data = s.recv(100000000)
			    livehosts2 = data.strip()
			    livehosts = livehosts2.split(";")
			    s.close()
			    livehostsdownind = int(livehosts[0])
			    livehoststotalind = int(livehosts[1])
			    livehostsdown = livehostsdown + livehostsdownind
			    livehoststotal = livehoststotal + livehoststotalind
                        r["livehostsdownstatus"] = livehostsdown
                        r["livehoststotalstatus"] = livehoststotal
                    except:
                        r["livehostsdownstatus"] = "0"
                        r["livehoststotalstatus"] = "0"

except:
    import traceback
    stack =  traceback.format_exc()
    results = splunk.Intersplunk.generateErrorResults("Error : Traceback: " + str(stack))

splunk.Intersplunk.outputResults( results )

