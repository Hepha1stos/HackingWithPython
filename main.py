from flask import Flask
from flask import render_template
from flask import request

from funcs.names import low

app = Flask(__name__)

@app.route("/main")
def main():
  vars = ["Thorsten","Johannah","Fabian"]
  newVars = [low(name) for name in vars]

  name = request.args.get("name","Test")
  return render_template("main.html", vars = newVars, name=name)

if __name__ == "__main__":
  app.run(debug=True)