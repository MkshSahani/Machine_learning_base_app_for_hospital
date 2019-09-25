def gen_patient_mail(degi,dept,mess, to):
	body = f"""\
			<!doctype html>
			<html>
			<head>
				Tips From System.
			</head>
			<body>
				<h1>Hello mr. {to}</h1>
				<hr/>
				<h2>Some Health Tips by {dept} Department<h2>
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
