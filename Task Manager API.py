from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)
api = Api(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

class TaskResource(Resource):
    def get(self, task_id=None):
        if task_id:
            task = Task.query.get(task_id)
            return jsonify({"id": task.id, "title": task.title, "completed": task.completed}) if task else {"message": "Task not found"}, 404
        tasks = Task.query.all()
        return jsonify([{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks])

    def post(self):
        data = request.json
        new_task = Task(title=data["title"])
        db.session.add(new_task)
        db.session.commit()
        return {"message": "Task created", "id": new_task.id}

    def put(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            return {"message": "Task not found"}, 404
        task.title = request.json.get("title", task.title)
        task.completed = request.json.get("completed", task.completed)
        db.session.commit()
        return {"message": "Task updated"}

    def delete(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            return {"message": "Task not found"}, 404
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted"}

api.add_resource(TaskResource, "/tasks", "/tasks/<int:task_id>")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
