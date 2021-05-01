from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL
import csv


def hello_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
    Bootstrap(app)

    return app

app = hello_app()


class CafeForm(FlaskForm):
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('URL Location', validators=[DataRequired(), URL(message='Invalid URL.')])
    open = StringField('Opening Hour (e.g. 5:30AM)', validators=[DataRequired()])
    close = StringField('Closing Hour (e.g. 10:30PM)', validators=[DataRequired()])
    quality = SelectField('Coffee Quality', choices=[('☕',1),('☕☕',2),('☕☕☕',3), ('☕☕☕☕',4), ('☕☕☕☕☕',5)])
    wifi = SelectField('Wifi Strength', choices=[('✘',0), ('💪',1),('💪💪',2),('💪💪💪',3), ('💪💪💪💪',4), ('💪💪💪💪💪',5)])
    outlets = SelectField('Outlet Equity', choices=[('✘',0),('🔌',1),('🔌🔌',2),('🔌🔌🔌',3), ('🔌🔌🔌🔌',4), ('🔌🔌🔌🔌🔌',5)])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', 'a') as file:
            file.write("\n" + form.cafe.data + "," + form.location.data + "," + form.open.data +
                       "," + form.close.data + "," + form.quality.data + "," + form.wifi.data +
                       "," + form.outlets.data)
            file.close()
        return redirect(url_for('add_cafe'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return render_template('cafes.html', cafes=data)


if __name__ == '__main__':
    app.run(debug=True)
