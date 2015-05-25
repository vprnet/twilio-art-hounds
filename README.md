# twilio-listener pitches

This is a very simple Python/WSGI app created to serve dynamic TwiML/XML files for VPR's Twilio Art Hounds call-in line

## Installation

Log in to the WebFaction dashboard, and create a new Python 2.7/WSGI application.

Create a new Website in the dashboard, and link your new WebFaction Application to it.

SSH into WebFaction, and make your way to you new Application's directory.

Empty the Application's directory (if it is not already empty), and clone this repository within it. 
(Note the '.' parameter which specifies the current directory rather creating a new one.)
	
	git clone https://github.com/vprnet/twilio-art-hounds .

That's it! The application should be up and running at the URL you assigned to this Application.
