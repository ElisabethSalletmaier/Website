from flask_wtf import FlaskForm
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import os
import gunicorn

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
db = SQLAlchemy()
db.init_app(app)


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    subject = StringField("Subject", validators=[DataRequired()])
    message = TextAreaField("Your Message", widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField("Send Message")


# Create a table for the messages
class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    message = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_message = Message(
            name=form.name.data,
            message=form.message.data
        )
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("contact.html", form=form)


@app.route("/credits")
def credits():
    return render_template("credits.html")


if __name__ == "__main__":
    app.run(debug=False)
