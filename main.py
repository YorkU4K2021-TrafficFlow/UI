from flask import Flask, render_template, session, request, redirect, url_for
from Path import Paths
import GlobalParams
import data_service as ds

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "some_complex_key"
FIRST = True


# trigger error flags in ui, return error code to getRoute
# TODO we should have this function, before returning, trigger ui elements to tell user whats wrong
def flag_io(src: str, dst: str):
    res = ds.which_valid(src, dst)    
    
    # this case occurs when both are valid, in which this function shouldn't be called
    # just a precaution
    if (res[0] and res[1]):
        return('Something else went very wrong!\n')
    
    # otherwise when source is valid, destination is not
    elif(res[0]):
        return('Destination input faulty with value of: '+src+'\n')
    
    # otherwise when destination is valid, source is not
    elif(res[1]):
        return('Source input faulty with value of: '+dst+'\n')

    # otherwise they both aren't valid
    else:
        return('Source and destination inputs faulty with values of:\n'+src+'\n'+dst+'\n')

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
        if(ds.valid_input(source,dest)):
            paths = Paths(source, dest)
            paths.plot()
            session['layer2'] = False
            FIRST = False if FIRST else FIRST
        else:
            res = flag_io()
            raise Exception(res)
    except Exception as e:
        print("ERROR in getResult! " + str(e))

    return redirect(url_for("home"))



@app.route('/back_to_search', methods=['GET', 'POST'])
def back_to_search():
    session['layer2'] = True
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)


