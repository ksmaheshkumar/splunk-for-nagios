# Script to request services with UNKNOWN status and total services by accessing MK Livestatus
# Required field to be passed to this script from Splunk: host (mk-livestatus/nagios server)
import socket,string,sys,re,splunk.Intersplunk,mklivestatus

results = []

try:

    results,dummyresults,settings = splunk.Intersplunk.getOrganizedResults()

    for r in results:
        if "_raw" in r:
            if "host" in r:
                    try:
			HOST = mklivestatus.HOST
		        PORT = mklivestatus.PORT
			s = None 
		        liveservicesunknown = 0
		        liveservicestotal = 0
    			for h in HOST:
			    content = [ "GET services\nStats: state = 3\nStats: state != 9999\n" ]
			    query = "".join(content)
    			    try:
			        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			        s.connect((h, PORT))
    			    except socket.error, (value,message): 
        			if s: 
			            s.close() 
			            #Error: Could not open socket: connection refused (MK Livestatus not setup in xinetd?)
			            break
			    s.send(query)
			    s.shutdown(socket.SHUT_WR)
			    data = s.recv(100000000)
    			    data2 = (re.findall(r'(No UNIX socket)', data))
			    if data2:
			        #Error: MK Livestatus module not loaded?
			        s.close()
			    else:
			        liveservices2 = data.strip()
			        liveservices = liveservices2.split(";")
			        s.close()
			        liveservicesunknownind = int(liveservices[0])
			        liveservicestotalind = int(liveservices[1])
			        liveservicesunknown = liveservicesunknown + liveservicesunknownind
			        liveservicestotal = liveservicestotal + liveservicestotalind
                        r["liveserviceunknownstatus"] = liveservicesunknown
                        r["liveservicetotalstatus"] = liveservicestotal
                    except:
                        r["liveserviceunknownstatus"] = "0"
                        r["liveservicetotalstatus"] = "0"

except:
    import traceback
    stack =  traceback.format_exc()
    results = splunk.Intersplunk.generateErrorResults("Error : Traceback: " + str(stack))

splunk.Intersplunk.outputResults( results )

