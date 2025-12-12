import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="#Deepti2003",
    database="assignment"
)

cursor = db.cursor()

# Lessons for FULL STACK DEVELOPER (course_id=1)
fullstack_lessons = [
    "Introduction to Web Development",
    "HTML Fundamentals",
    "CSS Styling and Layout",
    "JavaScript Basics",
    "Python Programming",
    "Flask Framework",
    "MySQL Database Integration",
    "Deployment and Hosting"
]

# Lessons for FRONTEND DEVELOPER (course_id=2)
frontend_lessons = [
    "HTML Structure and Semantics",
    "CSS Advanced Techniques",
    "JavaScript DOM Manipulation",
    "Responsive Design with Media Queries",
    "Version Control with Git",
    "React.js Fundamentals",
    "State Management in React",
    "Frontend Testing"
]

# Lessons for BACKEND DEVELOPER (course_id=3)
backend_lessons = [
    "Python Programming Basics",
    "Data Structures and Algorithms",
    "Flask Web Framework",
    "REST API Development",
    "Database Design with MySQL",
    "Authentication and Security",
    "API Testing and Documentation",
    "Deployment Strategies"
]

# Insert lessons
for lesson in fullstack_lessons:
    cursor.execute("INSERT INTO lessons (title, course_id) VALUES (%s, %s)", (lesson, 1))

for lesson in frontend_lessons:
    cursor.execute("INSERT INTO lessons (title, course_id) VALUES (%s, %s)", (lesson, 2))

for lesson in backend_lessons:
    cursor.execute("INSERT INTO lessons (title, course_id) VALUES (%s, %s)", (lesson, 3))

db.commit()
print("Lessons added successfully!")