from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def hello():
	return "<html><h1>Hello World?!</h1></html>"

@app.route("/world")
def world():
	print(dict(request.args))
	if 'world' in request.args:
		return '%s World' % (request.args['world'])
	else:
		return '넌 서강대에 있어야만 해'

@app.route("/form", methods=["GET", "POST"])
def form():
	if request.method == "GET":
		return """
<form action="/form" method="POST">
	<input type="text" name="id" id="id" value="아이디를입력하세요" />
	<input type="submit" />
</form>
"""
	else:
		return "%s님 안녕하세요" % (request.form['id'])


if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")
