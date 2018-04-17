from flask import *
import os



UPLOAD_FOLDER = 'meshes'
mesh_name = None


def init_app(app):
    "Initialize app object. Create upload folder if it does not exist."
    if not os.path.isabs(app.config['UPLOAD_FOLDER']):
        folder = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])
        app.config['UPLOAD_FOLDER'] = folder
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

app = Flask(__name__)
app.config.from_object(__name__)
init_app(app)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/start/", methods=['POST'])
def start_scan():
	global mesh_name
	
	mesh_name = request.form['mesh_name']
	if not mesh_name:
		return render_template('index.html', error='Bad Mesh Name!')
	mesh_name = mesh_name + "..." #add file extension

	#SCANNING CODE
	print("Finished Scanning" + "\n")


	print("Uploading Mesh" + "\n")
	#Place output files in directory scan/meshes


	return render_template('index.html')

@app.route("/pause/", methods=['POST'])
def pause_scan():
	#PAUSE CODE
	return render_template('index.html')

@app.route("/reset/", methods=['POST'])
def reset_scan():
	#RESET CODE
	print("Scanner Reset")
	return render_template('index.html')



@app.route("/download/", methods=['POST'])
def download_scan():
    # return render_template('index.html')
    if not mesh_name:
    	return render_template('index.html', error='Not Object Scanned Yet!')

    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=mesh_name)




