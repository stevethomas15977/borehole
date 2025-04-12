import os
import threading
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
)
from flask_autoindex import AutoIndex
from werkzeug.utils import secure_filename
from context import Context
from workflow_manager import WorkflowManager
from datetime import datetime
import shutil

context = Context()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a random secret key for session handling
files_index = AutoIndex(app, browse_root=os.getenv("PROJECTS_PATH"), add_url_rules=False)

# Set the maximum upload file size to 25 MB
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 25 MB

@app.template_filter('timestamp_to_date')
def timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/projects/')
@app.route('/projects/<path:path>/')
def autoindex(path=context.projects_path):
    return files_index.render_autoindex(path)

@app.route('/health')
def health():
    return jsonify(status='ok'), 200

@app.route('/')
def index():
    app = os.getenv('APP')
    env = os.getenv('ENV')
    version = os.getenv('VERSION')
    server = os.getenv('AFE_PROD_DNS')
    return render_template('index.html', app=app.capitalize(), version=version, server=server, env=env)

def run_workflow(workflow_manager: WorkflowManager):
    try:
        workflow_manager.base_workflow()
        workflow_manager.offset_well_identification_workflow()
    except Exception as e:
        print(f"Error occurred during workflow: {e}")

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'project' not in request.form or 'well-data' not in request.files or 'survey-data' not in request.files:
            flash('Missing project name or file part', 'error')
            return redirect(url_for('index'))

        project = request.form['project']
        well_data = request.files['well-data']
        survey_data = request.files['survey-data']

        if project == '':
            flash('Project name is required', 'error')
            return redirect(url_for('index'))
        
        if well_data.filename == '' or survey_data.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('index'))

        context.project = project
        context.project_path = os.path.join(context.projects_path, project)
        os.makedirs(context.project_path, exist_ok=True)
        
        context.well_data_path = os.path.join(context.project_path, 'well_data')
        context.survey_data_path = os.path.join(context.project_path, 'survey_data')

        context.logs_path = os.path.join(context.project_path, 'logs')

        os.makedirs(context.well_data_path, exist_ok=True)
        os.makedirs(context.survey_data_path, exist_ok=True)
        if os.path.exists(context.logs_path):
            shutil.rmtree(context.logs_path)
        os.makedirs(context.logs_path, exist_ok=True)

        context.db_path = os.path.join(context.logs_path, f"{context.project}-{context.version}.db")

        context.well_file = os.path.join(context.well_data_path, secure_filename(well_data.filename))
        context.survey_file = os.path.join(context.survey_data_path, secure_filename(survey_data.filename))

        well_data.save(context.well_file)
        survey_data.save(context.survey_file)

        for state in ['RUNNING', 'COMPLETED', 'ERROR']:
            if os.path.exists(os.path.join(context.project_path, state)):
                os.remove(os.path.join(context.project_path, state))

        workflow_manager = WorkflowManager(context=context)
        try:
            workflow_manager.project_initiation_workflow()
        except (Exception, ValueError) as e:
            shutil.rmtree(context.project_path)
            flash(f'An error occurred during project initiation: {str(e)}')
            return redirect(url_for('index'))
                
        workflow_thread = threading.Thread(name=context.project, target=run_workflow, args=(workflow_manager, ))
        workflow_thread.start()
        return redirect(f"/projects/{context.project}")

    except ValueError as ve:  # Handle ValueError specifically
        shutil.rmtree(context.project_path)
        flash(f'ValueError occurred: {str(ve)}')
        return redirect(url_for('index'))

    except Exception as e:  # Catch all other exceptions
        shutil.rmtree(context.project_path)
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('index'))

# Error handler for file size limit
@app.errorhandler(413)
def request_entity_too_large(error):
    flash('File Too Large', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


