from flask import Flask,request,redirect,url_for,render_template # this looks inside templates folder

## Jinja2 template engine
"""
{{ }} expressions to print output on html
{%...%} conditions,loops - we have to close conditions at the end[endfor,endif, etc]
{#...#} single line comments
"""

'''
It creates an instance of Flask class,
which will be our WSGI(web server gateway interface) applicaiton
'''

''' Basic Template '''
# app = Flask(__name__)

# if __name__=="__main__":
#     app.run()

app = Flask(__name__)


@app.route("/") # Home page
def welcome():
    return "Welcome to my Home Page"

@app.route("/index") # Index page
def index():
    return render_template("Index.html")

@app.route("/about") # About page
def about():
    return render_template("about.html")

# Variable Rule
@app.route('/success/<int:score>') # default variable type is str
def success(score):
    res = ""
    if score>=50:
        res = "PASSED"
    else:
        res = "FAILED"
    return render_template('result.html',results=res)

@app.route('/successfor/<int:score>') 
def successfor(score):
    res = ""
    if score>=50:
        res = "PASSED"
    else:
        res = "FAILED"

    exp = {"Score":score,"Result":res}
    return render_template('result1.html',results=exp)

@app.route('/successif/<int:score>') 
def successif(score):
    return render_template('result.html',results=score)

@app.route('/submit',methods=["GET","POST"])
def submit():
    total_score = 0
    if request.method=="POST":
        science = float(request.form['science'])
        maths = float(request.form['maths'])
        c = float(request.form['c'])
        datascience = float(request.form['datascience'])

        total_score = (science+maths+c+datascience)/4
    else:
        return render_template("getresult.html")

    return redirect(url_for("successfor",score=total_score))

if __name__=="__main__": # Entry Point
    app.run(debug=True)# debug restarts the server automatically after saving