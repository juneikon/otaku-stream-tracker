from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anime.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    episodes_watched = db.Column(db.Integer, default=0)
    total_episodes = db.Column(db.Integer)
    status = db.Column(db.String(20), default='Watching')
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

@app.route('/')
def index():
    anime_list = Anime.query.order_by(Anime.last_updated.desc()).all()
    return render_template('index.html', anime_list=anime_list)

@app.route('/add', methods=['GET', 'POST'])
def add_anime():
    if request.method == 'POST':
        anime = Anime(
            title=request.form['title'],
            episodes_watched=request.form.get('episodes_watched', 0),
            total_episodes=request.form['total_episodes'],
            status=request.form['status'],
            notes=request.form.get('notes', '')
        )
        db.session.add(anime)
        db.session.commit()
        flash('Anime added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_anime(id):
    anime = Anime.query.get_or_404(id)
    if request.method == 'POST':
        anime.title = request.form['title']
        anime.episodes_watched = request.form['episodes_watched']
        anime.total_episodes = request.form['total_episodes']
        anime.status = request.form['status']
        anime.notes = request.form['notes']
        anime.last_updated = datetime.utcnow()
        db.session.commit()
        flash('Anime updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', anime=anime)

@app.route('/delete/<int:id>')
def delete_anime(id):
    anime = Anime.query.get_or_404(id)
    db.session.delete(anime)
    db.session.commit()
    flash('Anime deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)