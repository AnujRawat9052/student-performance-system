from flask import Flask, render_template, request
import csv
import os
import pandas as pd 
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        student_id = request.form["student_id"]
        name = request.form["name"]
        attendance = request.form["attendance"]
        study_hours = request.form["study_hours"]
        assignment_marks = request.form["assignment_marks"]
        internal_marks = request.form["internal_marks"]
        practical_marks = request.form["practical_marks"]
        previous_marks = request.form["previous_marks"]

        file_exists = os.path.isfile("students.csv")

        with open("students.csv", "a", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "Student ID",
                    "Name",
                    "Attendance",
                    "Study Hours",
                    "Assignment Marks",
                    "Internal Marks",
                    "Practical Marks",
                    "Previous Marks"
                ])

            writer.writerow([
                student_id,
                name,
                attendance,
                study_hours,
                assignment_marks,
                internal_marks,
                practical_marks,
                previous_marks
            ])

        return "Student Added Successfully!"

    return render_template("add_student.html")


@app.route("/students")
def students():
    students = []

    if os.path.isfile("students.csv"):
        with open("students.csv", "r", newline="") as file:
            reader = csv.DictReader(file)
            students = list(reader)

    return render_template("students.html", students=students)

@app.route("/analysis")
def analysis():

    df = pd.read_csv("students.csv")

    # Average student data

    average_attendance = df["Attendance"].mean()

    average_study_hours = df["Study Hours"].mean()

    average_assignment = df["Assignment"].mean()

    average_internal = df["Internal"].mean()

    average_practical = df["Practical"].mean()

    average_previous = df["Previous Marks"].mean()


    # -----------------------------
    # Graph 1: Average Marks
    # -----------------------------

    subjects = [
        "Assignment",
        "Internal",
        "Practical",
        "Previous"
    ]

    average = [
        average_assignment,
        average_internal,
        average_practical,
        average_previous
    ]


    plt.figure(figsize=(8, 5))

    plt.bar(subjects, average)

    plt.title("Average Students Marks")

    plt.xlabel("Assignment Type")

    plt.ylabel("Average Marks")

    plt.tight_layout()

    plt.savefig("static/average_marks.png")

    plt.close()


    # -----------------------------
    # Graph 2: Attendance vs Study Hours
    # -----------------------------

    plt.figure(figsize=(8, 5))

    plt.scatter(
        df["Study Hours"],
        df["Attendance"]
    )

    plt.title("Attendance vs Study Hours")

    plt.xlabel("Study Hours")

    plt.ylabel("Attendance")

    plt.tight_layout()

    plt.savefig("static/attendance_study.png")

    plt.close()


    # -----------------------------
    # Send data to HTML
    # -----------------------------

    return render_template(
        "analysis.html",

        average_attendance=round(
            average_attendance, 2
        ),

        average_study_hours=round(
            average_study_hours, 2
        ),

        average_assignment=round(
            average_assignment, 2
        ),

        average_internal=round(
            average_internal, 2
        ),

        average_practical=round(
            average_practical, 2
        ),

        average_previous=round(
            average_previous, 2
        )
    )


   

@app.route("/prediction", methods=["GET", "POST"])
def prediction():

    if request.method == "POST":

        attendance = float(request.form["attendance"])
        study_hours = float(request.form["study_hours"])
        assignment = float(request.form["assignment_marks"])
        internal = float(request.form["internal_marks"])
        practical = float(request.form["practical_marks"])
        previous = float(request.form["previous_marks"])

        # Convert study hours to a score out of 100
        study_score = min((study_hours / 10) * 100, 100)

        # Calculate performance score
        score = (
            attendance * 0.20
            + study_score * 0.10
            + assignment * 0.20
            + internal * 0.20
            + practical * 0.15
            + previous * 0.15
        )

        score = round(score, 2)

        # Prediction
        if score >= 85:
            prediction_result = "Excellent"
        elif score >= 70:
            prediction_result = "Good"
        elif score >= 50:
            prediction_result = "Average"
        else:
            prediction_result = "Needs Improvement"

        return render_template(
            "prediction.html",
            prediction=prediction_result,
            score=score
        )

    return render_template("prediction.html")
    

if __name__ == "__main__":
    app.run(debug=True)
