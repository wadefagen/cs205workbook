from flask import Flask, render_template, jsonify, send_file, send_from_directory
from utilities import load_src
import os
import json

# create the application object
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.template_folder = '.'
app.debug = True

# save the starting cwd
basecwd = os.getcwd()

# Set up the navigation global variable, to be used by the templates when
# rendering the HTML
navigation = { "demos": [], "labs": [], "mps": [], "personal": [] }

def constructNavigation():
    # Reset the navigation global variable state
    navigation["demos"] = []
    navigation["labs"] = []
    navigation["mps"] = []
    navigation["personal"] = []
    
    # Scan all of the directories
    for rpath in os.listdir(basecwd):
        path = os.path.join(basecwd, rpath)
        if os.path.isdir(path):
            projectType = ""
            project_data = {}

            project_data["href"] = "/" + rpath + "/"
            
            # Attempt to infer the type of project:
            if rpath.startswith("demo_"):
                projectType = "Demo"
                
            if rpath.startswith("lab_"):
                projectType = "Lab"

            if rpath.startswith("mp_"):
                projectType = "MP"

            if rpath.startswith("personal_"):
                projectType = "Personal"

            project_data["title"] = rpath[ (len(projectType) + 1):: ]
                
            # Check for the project.json
            json_file_path = os.path.join(path, "project.json")
            if os.path.isfile( json_file_path ):
                with open(json_file_path) as json_file:
                    json_data = json.load(json_file)
                
                if "title" in json_data:
                     project_data["title"] = json_data["title"]

                if "projectType" in json_data:
                     projectType = json_data["projectType"]
                
            # Populate the global dictionary for templates
            if projectType == "Demo":
                navigation["demos"].append(project_data)
            if projectType == "Lab":
                navigation["labs"].append(project_data)
            if projectType == "MP":
                navigation["mps"].append(project_data)
            if projectType == "Personal":
                navigation["personal"].append(project_data)


# Route the base URL to the main page
@app.route('/')
def home():
    constructNavigation()
    return render_template('templates/mainPage.html', navigation=navigation)

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
	constructNavigation()
	result = render_template(exerciseName + '/web/index.html', navigation=navigation)
	
	return result


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))
