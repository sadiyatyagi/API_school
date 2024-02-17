from flask import Flask, jsonify, request
from data import school

app = Flask(__name__)

#Get all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(school)

#Get students by roll number
@app.route('/students/<int:roll_no>', methods = ['GET'])
def get_student(roll_no):
    student = next((student for student in school if student['roll_no'] == roll_no ), None)
    if student:
        return jsonify(student)
    else:
        return jsonify({'message':'Student not found'}), 404
    

@app.route('/student', methods = ['GET'])
def get_student_byquery():

    roll_no = request.args.get('roll_no', type=int)

    pass_status = request.args.get('pass', type=bool)
    
    if roll_no is not None:
         student = next((student for student in school if student['roll_no'] == roll_no ), None)

         if student is not None:   
            if pass_status:
                return jsonify({'student': student, "pass": "Student is passed."})
            else:
                return jsonify({'student': student, "pass": "Student not passed."})
    return jsonify({'message': 'Task not found'}), 404

@app.route('/students/add-student', methods=['POST'])
def add_student_bydata():
   
    # Get data from request body
    new_student = request.json

    #Check if all required field are peresent
    if 'roll_no' not in new_student or 'name' not in new_student or 'class' not in new_student or 'pass' not in new_student:
        return jsonify({'error': 'Missing required fields'}), 404
    
    # Extract data

    roll_no = new_student['roll_no']
    name = new_student['name']
    student_class = new_student['class']
    student_pass = new_student['pass']

    #Add new student
    student = {
        'roll_no': roll_no,
        'name': name,
        'class': student_class,
        'pass': student_pass
    }

    school.append(student)
    return jsonify({'student_added': student})    


@app.route('/students/<int:roll_no>', methods=['PUT'])
def update_student(roll_no):

    student = next((student for student in school if student['roll_no'] == roll_no ), None)   
    if student is not None:

        new_student = request.json
        # Check if all required fields are present
        if 'roll_no' not in new_student or 'name' not in new_student or 'class' not in new_student or 'pass' not in new_student:
         return jsonify({'error': 'Missing required fields'}), 400

        student.update(new_student)

        #return response
        return jsonify({"message": "Student updated successfully"
                        ,"student": new_student}), 201
    
    else:
        return jsonify({"message": "Student not found"}), 404
        

@app.route('/students/delete-student/<int:roll_no>', methods=['DELETE'])
def delete_student(roll_no):
    
     global school
     student = next((student for student in school if student['roll_no'] == roll_no ), None)   
     if student is not None:
        school = [student for student in school if student['roll_no']!= roll_no]

        return jsonify({"message": "Student is deleted"}), 201
     else:
         return jsonify({'message': 'student not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)