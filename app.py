from flask import Flask, request, jsonify
import os

app = Flask(__name__)

registrations = []

@app.route('/', methods=['GET'])
def get_student_number():
    student_number = {
        'student_number': '200594065'
    }
    return jsonify(student_number)
    
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    intent = req.get('queryResult').get('intent').get('displayName')

    if intent == 'Course Registration Intent':
        return handle_course_registration(req)
    elif intent == 'Track Registration Intent':
        return handle_track_registration(req)
    else:
        return {'fulfillmentText': 'I didn\'t understand that.'}

def handle_course_registration(req):
    params = req.get('queryResult').get('parameters')
    username = params.get('UserName')
    email = params.get('Email')
    course_type = params.get('CourseType')
    day_of_week = params.get('DayOfWeek')
    time_of_day = params.get('TimeOfDay')

    registrations.append({
        'username': username,
        'email': email,
        'course_type': course_type,
        'day_of_week': day_of_week,
        'time_of_day': time_of_day
    })

    return {'fulfillmentText': f'You have been registered for the {course_type} class on {day_of_week} in the {time_of_day}.'}

def handle_track_registration(req):
    params = req.get('queryResult').get('parameters')
    email = params.get('Email')

    user_registrations = [r for r in registrations if r['email'] == email]
    
    if user_registrations:
        response = 'Here are your registered classes:    \n'
        for reg in user_registrations:
            response += f"{reg['course_type']} on {reg['day_of_week']} in the {reg['time_of_day']}    \n"
        return {'fulfillmentText': response}
    else:
        return {'fulfillmentText': 'You have no registered classes.'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

