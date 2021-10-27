from flask import Flask, render_template, request, redirect, Response, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from wtforms import StringField, TextField, Form
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(64), index=True)
#     age = db.Column(db.Integer, index=True)
#     address = db.Column(db.String(256))
#     phone = db.Column(db.String(20))
#     email = db.Column(db.String(120))

#     def to_dict(self):
#         return {
#             'title': self.title,
#             'age': self.age,
#             'address': self.address,
#             'phone': self.phone,
#             'email': self.email
#         }


db.create_all()


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.today())
    # date_created = db.Column(db.String(400))
    delivered_status = db.Column(db.String(100))

    def to_dict(self):
        return {
            'title': self.title,
            'desc': self.desc,
            'date_created': self.date_created,
            'delivered_status': self.delivered_status
        }


# class SearchForm(Form):  # create form
#     country = StringField('Country', validators=[DataRequired(), Length(
#         max=40)], render_kw={"placeholder": "country"})


# class Country(db.Model):
#     __tablename__ = 'countries'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(60), unique=True, nullable=False)

#     def as_dict(self):
#         return {'name': self.name}


class Master(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    ics = db.Column(db.String(100))
    mobile = db.Column(db.String(100))

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} - {self.desc} - {self.delivered_status}"


# @app.route('/_autocomplete', methods=['GET'])
# def autocomplete():
#     cities = [
#         "Manish Lall",
#         "Manish lall Amarnani (ICS13968) - 7999492400",
#         "Maa Mati",
#     ]
#     print(cities)
#     return Response(json.dumps(cities), mimetype='application/json')


# @app.route('/das', methods=['GET', 'POST'])
# def das():
#     form = SearchForm(request.form)
#     return render_template("das.html", form=form)


# @app.route('/countries')
# def countrydic():
#     res = Country.query.all()
#     list_countries = [r.as_dict() for r in res]
#     return jsonify(list_countries)


# @app.route('/process', methods=['POST'])
# def process():
#     country = request.form['country']
#     if country:
#         return jsonify({'country': country})
#     return jsonify({'error': 'missing data..'})


@app.route('/add', methods=['GET', 'POST'])
def add():
    # form = SearchForm(request.form)
    return render_template("add.html")


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        delivered_status = request.form['delivered_status']
        todo = Todo(title=title, desc=desc, delivered_status=delivered_status)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


@app.route('/notdelivered', methods=['GET', 'POST'])
def notdelivered():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        delivered_status = request.form['delivered_status']
        each = Todo(title=title, desc=desc, delivered_status=delivered_status)
        db.session.add(each)
        db.session.commit()

    notdelivered = Todo.query.filter(Todo.delivered_status == "No")
    return render_template('notdelivered.html', notdelivered=notdelivered)


@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'


@app.route('/icsupdation', methods=['GET', 'POST'])
def icsupdation():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        delivered_status = request.form['delivered_status']
        todo = Todo(title=title, desc=desc, delivered_status=delivered_status)
        # db.session.add(todo)
        # db.session.commit()

    notDelivered = Todo.query.filter(Todo.delivered_status == "No")
    return render_template('icsupdation.html', notDelivered=notDelivered)

    # notDelivered = Todo.query.all()
    # return render_template('index.html', notDelivered=notDelivered)


@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        delivered_status = request.form['delivered_status']
        todo = Todo(title=title, desc=desc, delivered_status=delivered_status)

    notDelivered = Todo.query.filter(Todo.delivered_status == "Yes")
    return render_template('table.html', notDelivered=notDelivered)


@app.route('/api/data')
def data():
    query = Todo.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Todo.title.like(f'%{search}%'),
            Todo.delivered_status.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['title', 'desc', 'delivered_status']:
            col_name = 'title'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Todo, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        # to_dict
        'data': [todo.to_dict() for todo in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Todo.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@ app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        delivered_status = request.form['delivered_status']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        todo.delivered_status = delivered_status
        db.session.add(todo)
        db.session.commit()
        return redirect("/notdelivered")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


@ app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/notdelivered")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
