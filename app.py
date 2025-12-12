from flask import Flask, jsonify, redirect, render_template,request, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Add a secret key for sessions

db=mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="#Deepti2003",
    database="assignment"
    )

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        hashed_password=generate_password_hash(password)
        cursor=db.cursor()
        cursor.execute("INSERT INTO users (username,email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        db.commit()
        return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        cursor=db.cursor()
        cursor.execute("SELECT id, password FROM users WHERE email=%s", (email,))
        user=cursor.fetchone()
        if user and check_password_hash(user[1], password):
            session['user_id']=user[0]
            return redirect('/courses')
        else:
            return "Invalid credentials", 401
    return render_template("login.html")

@app.route('/courses', methods=['GET'])
def courses():
    if 'user_id' not in session:
        return redirect('/login')
    cursor = db.cursor()
    cursor.execute("SELECT id, title, description FROM courses")
    courses_data = cursor.fetchall()
    user_id = session['user_id']
    cursor.execute("SELECT COUNT(*) FROM enrollments WHERE user_id = %s", (user_id,))
    has_enrollments = cursor.fetchone()[0] > 0
    return render_template('courses.html', courses=courses_data, has_enrollments=has_enrollments)

@app.route('/courses/<int:id>')
def get_course(id):
    cursor = db.cursor()
    cursor.execute("SELECT id, title, description FROM courses WHERE id = %s", (id,))
    course = cursor.fetchone()
    if not course:
        return "Course not found", 404
    if 'user_id' in session:
        user_id = session['user_id']
        # Check enrollment
        cursor.execute("SELECT id FROM enrollments WHERE user_id = %s AND course_id = %s", (user_id, id))
        enrolled = cursor.fetchone() is not None
        # Check user rating
        cursor.execute("SELECT rating, comment FROM ratings WHERE user_id = %s AND course_id = %s", (user_id, id))
        user_rating = cursor.fetchone()
        # Average rating
        cursor.execute("SELECT AVG(rating), COUNT(*) FROM ratings WHERE course_id = %s", (id,))
        avg_result = cursor.fetchone()
        avg_rating = avg_result[0] or 0
        total_ratings = avg_result[1]
    else:
        enrolled = False
        user_rating = None
        avg_rating = 0
        total_ratings = 0
    return render_template('course_detail.html', course=course, enrolled=enrolled, user_rating=user_rating, avg_rating=avg_rating, total_ratings=total_ratings)
    
@app.route('/courses/<int:course_id>/enroll', methods=['POST'])
def enroll(course_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    cursor = db.cursor()
    cursor.execute("INSERT INTO enrollments (user_id, course_id) VALUES (%s, %s)", (user_id, course_id))
    db.commit()
    return redirect('/mycourses')
    # cursor.execute("SELECT id, title, description FROM courses WHERE id = %s", (course_id,))
    # course = cursor.fetchone()
    # return jsonify({'message': 'Enrolled successfully'})

@app.route('/mycourses')
def mycourses():
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    cursor = db.cursor()
    cursor.execute("SELECT c.id, c.title, c.description FROM courses c JOIN enrollments e ON c.id = e.course_id WHERE e.user_id = %s", (user_id,))
    my_courses = cursor.fetchall()
    return render_template('mycourses.html', courses=my_courses)

@app.route('/users/<int:user_id>/courses/<int:course_id>/progress')
def get_progress(user_id, course_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    cursor = db.cursor()
    # Total lessons
    cursor.execute("SELECT COUNT(*) FROM lessons WHERE course_id = %s", (course_id,))
    total = cursor.fetchone()[0]
    # Completed
    cursor.execute("SELECT COUNT(*) FROM user_progress WHERE user_id = %s AND course_id = %s", (user_id, course_id))
    completed = cursor.fetchone()[0]
    progress_percent = (completed / total * 100) if total > 0 else 0
    return jsonify({
        'course_id': course_id,
        'total_lessons': total,
        'completed_lessons': completed,
        'progress_percent': progress_percent
    })

@app.route('/courses/<int:course_id>/progress')
def course_progress_page(course_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    cursor = db.cursor()
    # Total lessons
    cursor.execute("SELECT COUNT(*) FROM lessons WHERE course_id = %s", (course_id,))
    total = cursor.fetchone()[0]
    # Completed
    cursor.execute("SELECT COUNT(*) FROM user_progress WHERE user_id = %s AND course_id = %s", (user_id, course_id))
    completed = cursor.fetchone()[0]
    progress = (completed / total * 100) if total > 0 else 0
    return render_template('progress.html', course_id=course_id, progress=progress, completed=completed, total=total)

@app.route('/courses/<int:course_id>/lessons')
def course_lessons(course_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    cursor = db.cursor()
    cursor.execute("SELECT id FROM enrollments WHERE user_id = %s AND course_id = %s", (user_id, course_id))
    if not cursor.fetchone():
        return "Forbidden", 403
    cursor.execute("SELECT id, title FROM lessons WHERE course_id = %s", (course_id,))
    lessons = cursor.fetchall()
    cursor.execute("SELECT lesson_id FROM user_progress WHERE user_id = %s AND course_id = %s", (user_id, course_id))
    completed = [row[0] for row in cursor.fetchall()]
    return render_template('lessons.html', course_id=course_id, lessons=lessons, completed=completed)

@app.route('/courses/<int:course_id>/lessons/<int:lesson_id>/complete', methods=['POST'])
def complete_lesson(course_id, lesson_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    cursor = db.cursor()
    cursor.execute("SELECT id FROM user_progress WHERE user_id = %s AND course_id = %s AND lesson_id = %s", (user_id, course_id, lesson_id))
    if cursor.fetchone():
        return redirect(f'/courses/{course_id}/lessons')
    cursor.execute("INSERT INTO user_progress (user_id, course_id, lesson_id, completed_at) VALUES (%s, %s, %s, NOW())", (user_id, course_id, lesson_id))
    db.commit()
    return redirect(f'/courses/{course_id}/lessons')

@app.route('/courses/<int:course_id>/rating', methods=['POST'])
def rate_course(course_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    user_id = session['user_id']
    cursor = db.cursor()
    # Check if enrolled
    cursor.execute("SELECT id FROM enrollments WHERE user_id = %s AND course_id = %s", (user_id, course_id))
    if not cursor.fetchone():
        return jsonify({'error': 'Not enrolled in this course'}), 403
    # Check if already rated
    cursor.execute("SELECT id FROM ratings WHERE user_id = %s AND course_id = %s", (user_id, course_id))
    if cursor.fetchone():
        return jsonify({'error': 'Already rated this course'}), 400
    # Get rating from form
    rating = request.form.get('rating')
    comment = request.form.get('comment', '')
    if not rating or not (1 <= int(rating) <= 5):
        return jsonify({'error': 'Invalid rating'}), 400
    cursor.execute("INSERT INTO ratings (user_id, course_id, rating, comment) VALUES (%s, %s, %s, %s)", (user_id, course_id, int(rating), comment))
    db.commit()
    return redirect(f'/courses/{course_id}')

@app.route('/courses/<int:course_id>/rating')
def get_course_rating(course_id):
    cursor = db.cursor()
    cursor.execute("SELECT AVG(rating), COUNT(*) FROM ratings WHERE course_id = %s", (course_id,))
    result = cursor.fetchone()
    avg_rating = result[0] or 0
    count = result[1]
    return jsonify({'course_id': course_id, 'average_rating': float(avg_rating), 'total_ratings': count})

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)