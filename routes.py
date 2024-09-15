from datetime import datetime, timezone
from flask import render_template, request, redirect, url_for
from app import app, db
from models import User, Task, Project

# Home route
@app.route('/')
def home():
    return "Welcome to the Task Management System!"

@app.before_request
def create_test_data():
    db.create_all()

    if Project.query.count() == 0:  # Insert test data if the database is empty
        project1 = Project(name='Project Alpha', description='This is Project Alpha', start_date=datetime.now(timezone.utc))
        project2 = Project(name='Project Beta', description='This is Project Beta', start_date=datetime.now(timezone.utc))

        task1 = Task(title='Task 1 for Alpha', description='Details for Task 1', project_id=project1.id, user_id=0, priority="Low")
        task2 = Task(title='Task 2 for Alpha', description='Details for Task 2', project_id=project1.id, user_id=0, priority="Low")
        task3 = Task(title='Task for Beta', description='Details for Beta Task', project_id=project2.id, user_id=0, priority="Low")

        db.session.add_all([project1, project2, task1, task2, task3])
        db.session.commit()

# User route (list users)
@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

# Create new user
@app.route('/user/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        new_user = User(name=name, email=email, password=password, role='Member')
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('new_user.html')

# Project route (list projects)
@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data['title']
    priority = data['priority']
    description = data.get('description', '')
    deadline = data.get('deadline')
    project_id = data['project_id']

    # Convert deadline from string to datetime if provided
    due_date_obj = datetime.strptime(deadline, '%Y-%m-%dT%H:%M') if deadline else None

    # Create the new task
    new_task = Task(title=title, description=description, deadline=due_date_obj, project_id=project_id)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        'success': True,
        'task': {
            'id': new_task.id,
            'title': new_task.title,
            'description': new_task.description
        }
    })

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    # Fetch the project by ID, or return 404 if not found
    project = Project.query.get_or_404(project_id)
    
    # Fetch tasks associated with this project
    tasks = Task.query.filter_by(project_id=project.id).all()

    return render_template('project.html', project=project, tasks=tasks)

# Task route (list tasks)
@app.route('/tasks')
def tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

# Add new task
@app.route('/task/new', methods=['GET', 'POST'])
def new_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_task = Task(title=title, description=description, priority='Medium', status='Pending')
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('tasks'))
    return render_template('new_task.html')
