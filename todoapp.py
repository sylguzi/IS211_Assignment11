from flask import Flask, render_template
from flask import flash, request, redirect, url_for, session
import re
import os
from utils import Map, DBHelper
from custom_object import Priority, ToDo, get_columns
app = Flask(__name__)
conn = None

DATABASE_PATH = 'database.sqlite'
EMAIL_CHECK = re.compile(r"(^[_A-Za-z0-9-\+]+(\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\.[A-Za-z0-9]+)*(\.[A-Za-z0-9]{2,})$)")
PRIORITIES = get_columns(Priority)

@app.route('/')
def index():
	todos = conn.select_todos()
	return render_template('todos.html', todos=todos)

@app.route('/submit', methods=['POST'])
def submit():
	id = str(request.form['id'])
	email = str(request.form['email'])
	priority = str(request.form['priority'])
	task = str(request.form['task'])
	if EMAIL_CHECK.match(email) is None:
		flash('Email format is wrong.')
	elif priority not in PRIORITIES:
		flash('Invalid priority.')
	elif len(task) == 0:
		flash('No task to add')
	else:
		if len(id) > 0:
			conn.update_todo(id, email, priority, task)
		else:
			conn.insert_todo(email, priority, task)
	return redirect('/')

@app.route('/todo/create')
def todo_form():
	return render_template('todo.html', priorities=PRIORITIES)

@app.route('/todo/clear')
def todo_clear_form():
	return render_template('clear.html')

@app.route('/todo/<int:id>/edit')
def todo_edit_form(id):
	todo = conn.select_todo(id)
	if ToDo is None:
		flash('Invalid todo id')
		return redirect('/')
	return render_template('todo.html', priorities=PRIORITIES, id=todo.id, email=todo.email, priority=todo.priority, task=todo.task)

@app.route('/todo/<int:id>/delete')
def todo_delete(id):
	conn.delete_todo(id)
	todos = conn.select_todos()
	return render_template('todos.html', todos=todos)

@app.route('/clear')
def todo_clear():
	conn.delete_todo(0)
	return render_template('todos.html')

if __name__ == '__main__':
	conn = DBHelper(DATABASE_PATH)
	app.secret_key = os.urandom(12)
	app.run(debug = True, use_reloader=True)

