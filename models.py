from app import db

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Admin, Member
    tasks = db.relationship('Task', backref='assigned_user', lazy=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)

    def __repr__(self):
        return f'<User {self.name}>'

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    deadline = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    comments = db.relationship('Comment', backref='task', lazy=True)
    tags = db.relationship('Tag', backref='task', lazy=True)
    
    def __repr__(self):
        return f'<Task {self.title}>'

# Project Model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    members = db.relationship('User', backref='project', lazy=True)
    tasks = db.relationship('Task', backref='project', lazy=True)
    
    def __repr__(self):
        return f'<Project {self.name}>'

# Comment Model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comment {self.content}>'

# Team Model
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    members = db.relationship('User', backref='team', lazy=True)

# Tag Model
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

# Notification Model
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

# Priority Model
class Priority(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(10), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

# Attachment Model
class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(200), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# AuditLog Model
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
