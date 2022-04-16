from flask import Flask, render_template, session, request, redirect, url_for
from Path import Paths
import GlobalParams

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "some_complex_key"
FIRST = True

@app.route("/")
def home():
    global FIRST

    if FIRST:
        session['layer2'] = True
        FIRST = False
    print("session['layer2']=",session['layer2'])
    return render_template("layer1.html")



@app.route('/map')
def map():
    return render_template(GlobalParams.RESULTS)


@app.route('/getResult', methods=['GET', 'POST'])
def getResult():
    global FIRST

    try:
        source = request.args['from']
        dest = request.args['to']
        paths = Paths(source, dest)
        paths.plot()
        session['layer2'] = False
        FIRST = False if FIRST else FIRST
    except Exception as e:
        print("ERROR in getResult! " + str(e))

    return redirect(url_for("home"))


@app.route('/back_to_search', methods=['GET', 'POST'])
def back_to_search():
    session['layer2'] = True
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)


