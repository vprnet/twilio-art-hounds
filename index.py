import sys


# UNCOMMENT THE FOLLOWING 2 LINES TO DISPLAY ERRORS (not sure this actually works at the moment - config issue??? display errors???)
#import cgitb
#cgitb.enable()




# THE LANDING PAGE - COMPLETE INTRODUCTION, INSTRUCTIONS, THEN RECORD
def welcomeResponse():
	return """
<Response>
	<Play>twilio-welcome.mp3</Play>
	<Record maxLength="60" transcribe="true" action="playback.xml" />
	<Hangup/>
</Response>"""


# THE PLAYBACK PAGE: INSTRUCTIONS, THEN PLAY THEIR MESSAGE BACK
def playBackResponse(filename):
	return """
<Response>
	<Gather numDigits="1" method="POST" action="rerecord.xml?filename="""+filename+"""" >
		<Play>twilio-playback-1.mp3</Play>
		<Pause />
		<Play>""" + filename + """</Play>
		<Pause />
		<Play>twilio-playback-2.mp3</Play>
	</Gather>
</Response>"""


# THE RERECORD PAGE: DELETE THE PREVIOUS RECORDING VIA THE API, THEN RECORD NEW MESSAGE
#	Twilio apparently already deletes or records over this file... [only one recording per call on Twilio???]
#	so there is no need for the above code to delete the file via the API
def rerecordResponse():
	return """
<Response>
	<Play>twilio-rerecord.mp3</Play>
	<Record maxLength="60" transcribe="true" action="playback.xml" />
</Response>"""


	
#
##
### RUN THE APPLICATION
##
#
def application(environ, start_response):
	query = environ.get("QUERY_STRING", "")
	filename = query.split('&')[0]
	if filename=="welcome.xml":
		content = welcomeResponse()	

	elif filename=="playback.xml":
		try:
			request_body_size = int(environ.get('CONTENT_LENGTH', 0))
		except (ValueError):
			request_body_size = 0
		
		from cgi import parse_qs
		request_body = environ['wsgi.input'].read(request_body_size)
		d = parse_qs(request_body)
		filename = d.get('RecordingUrl',[''])[0]
		content = playBackResponse(filename)

	elif filename=="rerecord.xml":
		content = rerecordResponse()

	else:
		content = 'error'


# IF THERE IS NOT A FILENAME MATCH, RETURN A 404	
	if content=='error':
		content = ''
		response_headers = [
			('Content-Length', str(len(content))),
			('Content-Type', 'text/plain'),
		]

		start_response('404 not found', response_headers)
		return [content]
		
# IF THERE IS AN APPROPRIATE FILENAME, RETURN A 200 OK, AN XML HEADER, AND THE CONTENT		
	else:
		response_headers = [
			('Content-Length', str(len(content))),
			('Content-Type', 'text/xml'),
		]

		start_response('200 OK', response_headers)
		return [content]

# DONE!!!