from flask_app import app
from flask_app.controllers import users_controller

# if __name__ == '__main__':
#     app.run(debug=True, host='localhost', port=8000)
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)