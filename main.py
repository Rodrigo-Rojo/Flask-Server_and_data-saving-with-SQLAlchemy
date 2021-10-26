from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
db.create_all()

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
all_rating = []
for num in numbers:
    for number in numbers:
        all_rating.append(float(f"{num}.{number}"))


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Books %r>' % self.title


class MyForm(FlaskForm):
    name = StringField('Book Name', validators=[DataRequired()])
    author = StringField('Book Author', validators=[DataRequired()])
    rating = SelectField('Rating', validators=[DataRequired()], choices=all_rating)
    add_button = SubmitField('Add Book')


class EditForm(FlaskForm):
    rating = SelectField('Rating', validators=[DataRequired()], choices=all_rating)
    add_button = SubmitField('Edit Rating')


@app.route('/')
def home():
    books = db.session.query(Books).all()
    return render_template("index.html", books=books)


@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit(id):
    form = EditForm()
    book = Books.query.get(id)
    if form.validate_on_submit():
        book.rating = form.rating.data
        db.session.commit()
        return redirect("/")
    return render_template("edit.html", form=form, book=book)


@app.route('/delete/<id>')
def delete(id):
    book = Books.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect("/")


@app.route("/add", methods=['POST', 'GET'])
def add():
    form = MyForm()
    name = form.name.data
    author = form.author.data
    rating = form.rating.data

    if form.validate_on_submit():
        new_book = Books(title=name, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect("/")
    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
