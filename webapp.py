from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
	return render_template("get_github.html")


@app.route("/student")
def get_student():
	hackbright_app.connect_to_db()
	student_github = request.args.get("student_github")
	if request.args.get("grade"):
		project = request.args.get("project_title")
		grade = request.args.get("grade")
		enter_grade = hackbright_app.make_new_grade(student_github, project, grade)
	row = hackbright_app.get_student_by_github(student_github)
	grades = hackbright_app.get_student_grades(student_github)
	if row is None:
		html = render_template("student_info.html", first_name="You", last_name="Boo", 
												student_github="No", grade_list=[])	
	else:
		html = render_template("student_info.html", first_name=row[0], last_name=row[1], 
												student_github=row[2], grade_list=grades)
	return html


@app.route("/project")
def get_project_info():
	hackbright_app.connect_to_db()
	project = request.args.get("project")
	row = hackbright_app.get_grades_by_project(project)
	html = render_template("project_info.html", project_list=row)

	return html


@app.route("/create_new_student")
def create_new_student():
	return render_template("create_new_student.html")


@app.route("/new_student")
def new_student():
	hackbright_app.connect_to_db()
	first_name = request.args.get("first_name")
	last_name = request.args.get("last_name")
	github = request.args.get("github")
	create = hackbright_app.make_new_student(first_name, last_name, github)
	row = hackbright_app.get_student_by_github(github)
	html = render_template("new_student.html", first_name=row[0], last_name=row[1], 
												github=row[2])

	return html


@app.route("/create_new_project")
def create_new_project():
	return render_template("create_new_project.html")


@app.route("/new_project")
def new_project():
	hackbright_app.connect_to_db()
	# all args need to be sent together
	title = request.args.get("title")
	description = request.args.get("description")
	grade = request.args.get("number")
	create = hackbright_app.make_new_project(title, description, grade)
	row = hackbright_app.get_project_by_title(title)
	html = render_template("new_project.html", title=row[0], description=row[1], 
												max_grade=row[2])

	return html


@app.route("/enter_student_grade")
def create_student_grade():
	return render_template("enter_student_grade.html")


if __name__ == "__main__":
	app.run(debug=True)