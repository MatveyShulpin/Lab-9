from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'cities.db')

db = SQLAlchemy(app)


# ----- Модель -----
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String(100), nullable=False)
    visit_date = db.Column(db.Date, nullable=False)

# создаём таблицы перед первым запросом
@app.before_request
def create_tables():
    db.create_all()


# ----- Маршруты -----
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        town = request.form.get('town')
        visit_date_str = request.form.get('visit_date')

        if town and visit_date_str:
            visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
            new_visit = Visit(town=town, visit_date=visit_date)
            db.session.add(new_visit)
            db.session.commit()

        return redirect(url_for('index'))

    visits = Visit.query.order_by(Visit.visit_date.desc()).all()
    return render_template('index.html', visits=visits)


if __name__ == '__main__':
    app.run()