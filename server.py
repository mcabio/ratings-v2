"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)

from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!

@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')

@app.route('/users')
def users():
    """View all users"""

    users = crud.all_users()

    return render_template('users.html', users=users)

@app.route('/users/<user_id>')
def show_user(user_id):
    """Show details on a particular movie"""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)

@app.route('/users', methods=["POST"])
def register_user():
    """Create new user"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    return redirect('/')

@app.route('/login', methods=['POST'])
def log_in():
    """User log in"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    
    if user.password == password:
        session['user'] = user.user_id
        flash('Logged In!')
    return redirect('/')

@app.route('/movies')
def all_movies():
    """View all movies"""

    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details on a particular movie"""

    movie = crud.get_movie_by_id(movie_id)


    return render_template('movie_details.html', movie=movie)


# @app.route('/movies/<movie_id>', methods=['POST'])
# def rating():
#     rated = request.form.get('ratings')
#     rating = crud.create_rating(rated, User.query.get(session['user']))
#     flash('rating added')
    
#     return redirect('/movies/<movie_id')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
