from flask import Flask,request,render_template # this looks inside templates folder
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

@app.route("/form",methods=['GET','POST'])
def form():
    if request.method=='POST':
        name = request.form['name']
        return f"Hello {name}!"
    return render_template('form.html')

# @app.route("/submit",methods=['GET','POST'])
# def submit():
#     if request.method=='POST':
#         name = request.form['name']
#         return f"Hello {name}!"
#     return render_template('form.html')


if __name__=="__main__": # Entry Point
    app.run(debug=True)# debug restarts the server automatically after saving