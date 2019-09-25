# this is a mail generator for the application
def generate_mail(degi, who, mess, to):

	body = f"""\
			<!doctype html>
			<html>
			<head>
				Message from the {degi} : {who}
			</head>
			<body>
				<h1>Hello mr. {to}</h1>
				<hr/>
				<h2>{degi}.{who} send a message to you<h2>
				<hr/>
				<p>
				{mess}
				<p>

				<br/>
				<br/>
				<br/>
				<hr/>
				<h2>
					Please visit our app for predict you health info.
				</h2>

			</body>
			</html>
			"""

	return body
