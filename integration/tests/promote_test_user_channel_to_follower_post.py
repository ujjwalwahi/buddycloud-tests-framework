import string
from api_utils import subscribe_to_user_channel, subscribe_to_topic_channel, has_subscriber_role_in_user_channel, has_subscriber_role_in_topic_channel, change_user_channel_subscriber_role, change_topic_channel_subscriber_role, approve_user_channel_subscription_request, approve_topic_channel_subscription_request
from find_api_location import findAPILocation

PUBLISHER_USERNAME = "test_user_channel_follower2"
FOLLOWED_USER_CHANNELS = [ "test_user_channel_open", "test_user_channel_closed" ]
FOLLOWED_TOPIC_CHANNEL = "test_topic_channel_open"

def testFunction(domain_url):

	CLASSIFIED = { 'SUBSCRIBED' : [],
		'PROBLEM_SUBSCRIBING_ASKING' : [],
		'PROBLEM_SUBSCRIBING_APPROVING' : [],
		'PROBLEM_CHANGING_SUBSCRIBER_ROLE' : [],
		'PROBLEM_DID_NOT_PROMOTE' : []}

	api_location = findAPILocation(domain_url)[3]

	for followed_channel in FOLLOWED_USER_CHANNELS:

		if subscribe_to_user_channel(domain_url, api_location, PUBLISHER_USERNAME, followed_channel, "member"):
			
			if approve_user_channel_subscription_request(domain_url, api_location, followed_channel, [PUBLISHER_USERNAME]):

				if change_user_channel_subscriber_role(domain_url, api_location, followed_channel, PUBLISHER_USERNAME, "publisher"):

					if has_subscriber_role_in_user_channel(domain_url, api_location, PUBLISHER_USERNAME, followed_channel, "publisher"):
						CLASSIFIED['SUBSCRIBED'].append(followed_channel + "@" + domain_url)
					else:
						CLASSIFIED['PROBLEM_DID_NOT_PROMOTE'].append(followed_channel + "@" + domain_url)

				else:
					CLASSIFIED['PROBLEM_CHANGING_SUBSCRIBER_ROLE'].append(followed_channel + "@" + domain_url)

			else:
				CLASSIFIED['PROBLEM_SUBSCRIBING_APPROVING'].append(followed_channel + "@" + domain_url)

		else:
			CLASSIFIED['PROBLEM_SUBSCRIBING_ASKING'].append(followed_channel + "@" + domain_url)

	for followed_channel in [FOLLOWED_TOPIC_CHANNEL]:

		if subscribe_to_topic_channel(domain_url, api_location, PUBLISHER_USERNAME, followed_channel, "member"):
	
			if approve_topic_channel_subscription_request(domain_url, api_location, followed_channel, FOLLOWED_USER_CHANNELS[0], [PUBLISHER_USERNAME]):

				if change_topic_channel_subscriber_role(domain_url, api_location, FOLLOWED_USER_CHANNELS[0], PUBLISHER_USERNAME, followed_channel, "publisher"):

					if has_subscriber_role_in_topic_channel(domain_url, api_location, PUBLISHER_USERNAME, followed_channel, "publisher"):
						CLASSIFIED['SUBSCRIBED'].append(followed_channel + "@" + domain_url)
					else:
						CLASSIFIED['PROBLEM_DID_NOT_PROMOTE'].append(followed_channel + "@" + domain_url)

				else:
					CLASSIFIED['PROBLEM_CHANGING_SUBSCRIBER_ROLE'].append(followed_channel + "@" + domain_url)

			else:
				CLASSIFIED['PROBLEM_SUBSCRIBING_APPROVING'].append(followed_channel + "@" + domain_url)

		else:
			CLASSIFIED['PROBLEM_SUBSCRIBING_ASKING'].append(followed_channel + "@" + domain_url)

	status = 0

	if ( ( len(CLASSIFIED.get('PROBLEM_SUBSCRIBING_ASKING', [])) > 0)
	or ( len(CLASSIFIED.get('PROBLEM_SUBSCRIBING_APPROVING', [])) > 0 )
	or ( len(CLASSIFIED.get('PROBLEM_CHANGING_SUBSCRIBER_ROLE', [])) > 0 )
	or ( len(CLASSIFIED.get('PROBLEM_DID_NOT_PROMOTE', [])) > 0 ) ):

		problematic_channels = string.join(CLASSIFIED.get('PROBLEM_SUBSCRIBING_ASKING', []) + CLASSIFIED.get('PROBLEM_SUBSCRIBING_APPROVING', []) + CLASSIFIED.get('PROBLEM_CHANGING_SUBSCRIBER_ROLE', []) + CLASSIFIED.get('PROBLEM_DID_NOT_PROMOTE', []), " | ")

		status = 1
		briefing = "Could not have some of these test channels promote <strong>%s@%s</strong> to <em>follower+post</em>: <br/><br/>" % (PUBLISHER_USERNAME, domain_url)
		briefing += "<strong>%s</strong>" % problematic_channels
		message = "Something weird happened while we tried having some test channels promote <strong>%s@%s</strong> to <em>follower+post</em> for testing purposes." % (PUBLISHER_USERNAME, domain_url)
		message += "<br/>The following test channels were problematic: <br/><br/>"
		message += "<strong>%s</strong>" % problematic_channels
		message += "<br/><br/>It seems like your HTTP API is problematic."

	else:

		briefing = "Could successfully have these test channels promote <strong>%s@%s</strong> to <em>follower+post</em>: " % (PUBLISHER_USERNAME, domain_url)
		briefing += "<strong>%s</strong>" % string.join(CLASSIFIED.get('SUBSCRIBED', []), " | ")
		message = "We could assert that these user channels which will be used later for testing purposes"
		message += " could successfully promote <strong>%s@%s</strong> to <em>follower+post</em>:" % (PUBLISHER_USERNAME, domain_url)
		message += "<br/><br/><strong>%s</strong>" % string.join(CLASSIFIED.get('SUBSCRIBED', []), "<br/>")

	return (status, briefing, message, None)