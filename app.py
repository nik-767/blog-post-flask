
from flask import Flask, render_template, session, request, Response, redirect, url_for , flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "mysecretkey"


db = SQLAlchemy(app)


class BlogPost(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    content = db.Column(db.Text, nullable=False)

    date_created = db.Column(db.DateTime, default=db.func.now())

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    email = db.Column(db.String(150), nullable=False)

    password = db.Column(db.String(200), nullable=False)

    date_created = db.Column(db.DateTime, default=db.func.now())



@app.route("/")
def home():
    return render_template("register.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        new_user = User(name=name, email=email, password=password )

        db.session.add(new_user)
        db.session.commit()

        return render_template("login.html")
    else:
        return render_template("register.html")
    

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session["user_id"] = user.id
            return redirect(url_for("create"))
    else:
        return render_template("login.html")
    

@app.route("/create",methods=["GET","POST"])
def create():

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        print(title, content)

        new_post = BlogPost(title=title, content=content)

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("post", id=new_post.id))
    else:
        return render_template("create.html")
    
@app.route("/blogpost")
def blogpost():
    posts = BlogPost.query.order_by(BlogPost.date_created.desc()).all()
    
    return render_template("post.html",posts=posts)

@app.route("/post/<id>")
def post(id):
    single = BlogPost.query.get(id)

    return render_template("single.html", single=single)



with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)                      