from flask import Flask, request, jsonify, render_template, url_for, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from EKKOcopy import summarizer
import json

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ekko.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    
    def __repr__(self):
        return f"Task {self.id}"
    
    
@app.route('/', methods = ['POST', 'GET'])

def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return "Issue Met"
    else:
        try:
            tasks = Todo.query.order_by(Todo.date_created).all()
        except:
            pass
        
        return render_template('index.html')

@app.route("/receiver", methods=["POST"])
def postME():
   data = request.get_json()
   data = json.loads(json.dumps(data))
   jsonurl = data["url"]
   summary = summarizer(jsonurl)
   newdata = {jsonurl: summary}
   new_task = Todo(content = summary, url = jsonurl)
   try:
        db.session.add(new_task)
        db.session.commit()
        return newdata
   except Exception as err:
        print (err)
        return newdata

if __name__ == "__main__": 
   app.run(debug=True)
   
