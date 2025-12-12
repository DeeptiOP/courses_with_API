# Course Platform API

A comprehensive Flask-based course management platform with user authentication, course enrollment, lesson tracking, and progress monitoring with better skillls.

## 🚀 Features

- **User Authentication**: Secure login and registration system
- **Course Management**: Browse and enroll in available courses
- **Lesson System**: Structured lessons for each course with completion tracking
- **Progress Tracking**: Visual progress bars and completion statistics
- **Rating System**: Course rating and review functionality
- **Modern UI**: Responsive design with gradient backgrounds and smooth animations
- **RESTful APIs**: JSON endpoints for programmatic access

## 🛠 Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, Jinja2 templates
- **Security**: Werkzeug (password hashing), Flask sessions
- **Styling**: Custom CSS with gradients and animations

## 📋 Prerequisites

- Python 3.8+
- MySQL Server
- Git

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Biswapriti/Api_integration.git
cd Api_integration
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install flask mysql-connector-python werkzeug
```

### 4. Database Setup

#### Create Database
```sql
CREATE DATABASE assignment;
```

#### Create Tables
```sql
USE assignment;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Courses table
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT
);

-- Enrollments table
CREATE TABLE enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    course_id INT,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- Lessons table
CREATE TABLE lessons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- User progress table
CREATE TABLE user_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    course_id INT,
    lesson_id INT,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (lesson_id) REFERENCES lessons(id)
);

-- Ratings table
CREATE TABLE ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    course_id INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    UNIQUE KEY unique_user_course_rating (user_id, course_id)
);
```

#### Insert Sample Data
```sql
-- Insert sample courses
INSERT INTO courses (title, description) VALUES
('FULL STACK DEVELOPER', 'Complete full stack development course covering frontend and backend technologies'),
('FRONTEND DEVELOPER', 'Master modern frontend development with HTML, CSS, and JavaScript frameworks'),
('BACKEND DEVELOPER', 'Learn server side development with Python, databases, and APIs'),
('DATA SCIENCE', 'Learn Python, machine learning, statistics, and real world data analysis'),
('MACHINE LEARNING', 'Build ML models, train datasets, and deploy intelligent applications'),
('CYBER SECURITY', 'Understand vulnerabilities, network security, and ethical hacking basics'),
('DEVOPS ENGINEER', 'Learn CI/CD, Docker, Kubernetes, and automation tools'),
('UI UX DESIGN', 'Design user friendly interfaces with Figma, prototyping, and usability testing'),
('MOBILE APP DEVELOPMENT', 'Build Android and iOS apps using Flutter and React Native'),
('CLOUD COMPUTING', 'Master AWS, Azure, and cloud infrastructure fundamentals'),
('DATABASE ADMINISTRATION', 'Learn MySQL, PostgreSQL, indexing, and database optimization'),
('AI ENGINEERING', 'Understand neural networks, transformers, and AI system development');
```

### 5. Configure Database Connection

Update the database credentials in `app.py`:
```python
db=mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="your_mysql_password",  # Change this
    database="assignment"
)
```

### 6. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 🎯 Usage

### User Flow
1. **Register**: Create a new account
2. **Login**: Access your account
3. **Browse Courses**: View available courses
4. **Enroll**: Join courses you're interested in
5. **Complete Lessons**: Mark lessons as completed
6. **Track Progress**: Monitor your learning progress
7. **Rate Courses**: Provide feedback on completed courses

### API Endpoints

#### Authentication
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

#### Courses
- `GET /courses` - List all courses
- `GET /courses/<id>` - Get course details
- `POST /courses/<id>/enroll` - Enroll in a course
- `GET /mycourses` - List enrolled courses

#### Lessons & Progress
- `GET /courses/<id>/lessons` - Get course lessons
- `POST /courses/<id>/lessons/<lesson_id>/complete` - Mark lesson complete
- `GET /courses/<id>/progress` - Get course progress
- `GET /users/<user_id>/courses/<course_id>/progress` - Get user progress (API)

#### Ratings
- `POST /courses/<id>/rating` - Rate a course
- `GET /courses/<id>/rating` - Get course rating statistics

## 📁 Project Structure

```
Api_integration/
├── app.py                      # Main Flask application
├── add_lessons.py             # Script to populate lessons
├── README.md                  # Project documentation
├── templates/                 # Jinja2 templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── courses.html
│   ├── course_detail.html
│   ├── lessons.html
│   ├── mycourses.html
│   └── progress.html
└── static/
    └── css/                   # Stylesheets
        ├── index.css
        ├── login.css
        ├── register.css
        ├── courses.css
        ├── course_detail.css
        ├── lessons.css
        ├── mycourses.css
        └── progress.css
```

## 🔒 Security Features

- Password hashing using Werkzeug
- Session-based authentication
- SQL injection prevention with parameterized queries
- CSRF protection through Flask-WTF (recommended for production)
- Input validation and sanitization

## 🚀 Deployment

### Local Development
```bash
python app.py
```
## 🎉 Acknowledgments

- Flask framework for the robust web development
- MySQL for reliable data storage
- Modern CSS techniques for beautiful UI
- Open source community for inspiration and tools

---

**Happy Learning! 🚀**

