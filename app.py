from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo2.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(500), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.DateTime)
    done=db.Column(db.Boolean,default=False)
    

@app.route('/')
def index():
    return render_template('front.html')

@app.route('/start')
def start():
    return render_template('index.html')
    
@app.route('/todo',methods=['GET','POST'])
def collect():
    if request.method=='POST':
        todo = request.form['todo']
        domain = request.form['domain']
        deadline = request.form['deadline']
        deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
        todo = Todo(todo=todo,domain=domain,deadline=deadline_date)
        db.session.add(todo)
        db.session.commit()
 
    return redirect(url_for('show'))
@app.route('/view')
def show():
    allTodo = Todo.query.all() 
    return render_template('show.html', allTodo=allTodo)

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        todo=request.form['todo']
        domain=request.form['domain']
        deadline=request.form['deadline']
        deadline_date= datetime.strptime(deadline, '%Y-%m-%d')
        obj=Todo.query.filter_by(sno=sno).first()
        obj.todo=todo
        obj.domain=domain
        obj.deadline=deadline_date
        db.session.add(obj)
        db.session.commit()
        return redirect(url_for('show'))
    
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('show'))

@app.route('/toggle/<int:sno>', methods=['POST'])
def toggle_status(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        todo.done = not todo.done  # Toggle the 'done' status
        db.session.commit()
    return redirect(url_for('show'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


