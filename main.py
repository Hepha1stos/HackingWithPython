from flask import Flask
from flask import render_template
from flask import request

from funcs.names import low

app = Flask(__name__)

@app.route("/main")
def main():
  vars= [low("Thorsten"),low("Johannah"),low("Fabian")]


  name = request.args.get("name","Test")
  return render_template("main.html", vars = vars, name=name)

if __name__ == "__main__":
  app.run(debug=True)