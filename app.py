from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    return render_template("index.html")



@app.route('/create-trash', methods=('POST', 'GET'))
def addT():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        try:
            article = Article(title=title, text=text)
            db.session.add(article)
            db.session.flush()
            db.session.commit()
            return redirect('/blog')
        except:
            return "err"
    else:
        return render_template("addTrash.html")


@app.route('/blog')
def blog():
    articles = Article.query.order_by(Article.date).all()
    return render_template("Blog.html", articles=articles)


@app.route('/add')
def add():
    return render_template("add.html")

@app.route('/acc')
def acc():
    return render_template("user.html")


@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User: " + name + "--" + str(id)


if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()
