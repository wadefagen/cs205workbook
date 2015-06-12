from flask import Flask, render_template, jsonify, send_file, send_from_directory
from utilities import load_src
import os

# create the application object
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.template_folder = '.'
app.debug = True

# save the starting cwd
basecwd = os.getcwd()


# Route the base URL to the main page
@app.route('/')
def home():
    return render_template('templates/mainPage.html')

@app.route('/<exerciseName>/res/<path:fileName>')
def fetchRes(exerciseName, fileName):
	return send_from_directory(os.path.join(exerciseName, 'res'), fileName)

@app.route('/<exerciseName>/js/<path:fileName>')
def fetchJS(exerciseName, fileName):
	return send_from_directory(os.path.join(exerciseName, 'js'), fileName)

# Route everything else to an exercise:
@app.route('/<exerciseName>/')
def fetchExercise(exerciseName):
	# Change the cwd to be relative to the py directory
	os.chdir(os.path.join(basecwd, exerciseName))

	load_src('exercisePythonFile', os.path.join(exerciseName, 'py', 'compute.py'))
	
	# Run the do_compute() function from compute.py
	from exercisePythonFile import do_compute
	do_compute()

	# Return the cwd to the root of the workbook
	os.chdir(basecwd)
	
	# Render the web template
	result = render_template(exerciseName + '/web/index.html')
	
	return result


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run()

