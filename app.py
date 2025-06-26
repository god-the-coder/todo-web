from flask import Flask , render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Todo.db"
app.config['AQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    with app.app_context():
       db.create_all()
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
      return f"{self.sno} - {self.title}"    


@app.route('/' , methods = ['GET', 'POST'])
def hello():
  if request.method == 'POST':
      title = request.form['title']
      desc = request.form['desc']
      todo = Todo(title=title, desc=desc)
      db.session.add(todo)
      db.session.commit()
  allTodo = Todo.query.all()
  return render_template("index.html", allTodo=allTodo)

@app.route('/about')
def about():
  alltodo = Todo.query.all()
  print(alltodo)
  return "this ia about page"

 

@app.route('/delete/<int:sno>')
def delete(sno):
  alltodo = Todo.query.filter_by(sno=sno).first()
  db.session.delete(alltodo)
  db.session.commit()
  
  return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
   if request.method == 'POST':
      title = request.form['title']
      desc = request.form['desc']
      todo = Todo.query.filter_by(sno=sno).first()
      todo.title = title
      todo.desc = desc
      db.session.commit()
      return redirect('/')
   todo = Todo.query.filter_by(sno=sno).first()
   return render_template('update.html', todo=todo)

if __name__ == '__main__':
  app.run(debug=True)

