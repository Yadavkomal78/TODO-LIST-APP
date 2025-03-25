
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config_settings import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
        mysql.connection.commit()
        cur.close()
        flash("Task Added Successfully", "success")
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tasks SET title=%s, description=%s, status=%s WHERE id=%s", (title, description, status, task_id))
        mysql.connection.commit()
        cur.close()
        flash("Task Updated Successfully", "success")
        return redirect(url_for('index'))

    return render_template('update_task.html', task=task)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    mysql.connection.commit()
    cur.close()
    flash("Task Deleted Successfully", "danger")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)