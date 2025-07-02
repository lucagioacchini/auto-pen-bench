from flask import Flask, request, jsonify, abort
import logging
import os
from dotenv import load_dotenv
from autopenbench.utils import load_data, load_milestones
from autopenbench.driver import PentestDriver
from autopenbench.evaluation import Evaluator
from autopenbench.tools import ExecuteBash, SSHConnect, WriteFile, FinalAnswer

load_dotenv()

app = Flask(__name__)

# Setup logging to file
log_path = os.path.join(os.path.dirname(__file__), 'server.log')
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s %(message)s')

def log_interaction(endpoint, data):
    logging.info(f'Endpoint: {endpoint} | Data: {data}')

# Global state for demonstration (not thread-safe, for demo only)
driver = None
evaluator = None
game = None
IS_EVALUATE_AFTER_STEP = False  # Toggle evaluation after each step

@app.route('/load_task', methods=['POST'])
def load_task():
    """Load a specific task by category, id, and initialize driver/evaluator."""
    global driver, evaluator, game
    data = request.json
    category = data.get('category', 'in-vitro')
    subcat = data.get('subcat', 'access_control')
    idx = int(data.get('id', 0))
    api_key = data.get('api_key') or os.environ.get('GEMINI_API_KEY')
    log_interaction('/load_task', data)
    game = load_data(category)[subcat][idx]
    driver = PentestDriver(game['task'], game['flag'], game['target'])
    observation, done = driver.reset()
    command_milestones = load_milestones('command', category, subcat, idx)
    stage_milestones = load_milestones('stage', category, subcat, idx)
    evaluator = Evaluator(api_key, command_milestones, stage_milestones)
    
    return jsonify({'task': game['task'], 'target': game['target'], 'observation': observation, 'done': done})

@app.route('/step', methods=['POST'])
def step():
    """Input step name and arguments, instantiate tool, output observation."""
    global driver, evaluator, IS_EVALUATE_AFTER_STEP
    data = request.json
    step_name = data.get('step_name')
    arguments = data.get('arguments', {})
    # If arguments is a string, try to parse as JSON
    if isinstance(arguments, str):
        import json as _json
        try:
            arguments = _json.loads(arguments)
        except Exception as e:
            return jsonify({'error': f'Could not parse arguments as JSON: {str(e)}'}), 400
    log_interaction('/step', {'step_name': step_name, 'arguments': arguments})

    # Map step name to tool class
    tool_map = {
        'ExecuteBash': ExecuteBash,
        'SSHConnect': SSHConnect,
        'WriteFile': WriteFile,
        'FinalAnswer': FinalAnswer
    }
    if step_name not in tool_map:
        return jsonify({'error': f'Unknown step_name: {step_name}'}), 400

    tool_class = tool_map[step_name]
    try:
        tool_instance = tool_class(**arguments)
    except Exception as e:
        return jsonify({'error': f'Error instantiating {step_name}: {str(e)}'}), 400

    observation, done = driver.step(tool_instance)

    # Evaluate immediately if enabled
    if IS_EVALUATE_AFTER_STEP and evaluator is not None:
        step_str = f'Action:{step_name}({arguments})\nObservation: {observation}'
        evaluator.evaluate_step(step_str)
        log_interaction('/evaluate_after_step', {'step': step_str})

    return jsonify({'observation': observation, 'done': done})

@app.route('/step/<step_name>', methods=['POST'])
def step_direct(step_name):
    """Direct endpoint for each tool: /step/ExecuteBash, /step/FinalAnswer, etc."""
    global driver, evaluator, IS_EVALUATE_AFTER_STEP
    # Always get arguments from request
    if request.is_json:
        arguments = request.get_json() or {}
    else:
        arguments = request.data.decode('utf-8')
    # If arguments is a string, try to parse as JSON
    if isinstance(arguments, str):
        import json as _json
        try:
            arguments = _json.loads(arguments)
        except Exception as e:
            return jsonify({'error': f'Could not parse arguments as JSON: {str(e)}'}), 400
    log_interaction(f'/step/{step_name}', {'step_name': step_name, 'arguments': arguments})
    tool_map = {
        'ExecuteBash': ExecuteBash,
        'SSHConnect': SSHConnect,
        'WriteFile': WriteFile,
        'FinalAnswer': FinalAnswer
    }
    if step_name not in tool_map:
        return jsonify({'error': f'Unknown step_name: {step_name}'}), 400
    tool_class = tool_map[step_name]
    try:
        tool_instance = tool_class(**arguments)
    except Exception as e:
        return jsonify({'error': f'Error instantiating {step_name}: {str(e)}'}), 400
    observation, done = driver.step(tool_instance)
    # Evaluate immediately if enabled
    if IS_EVALUATE_AFTER_STEP and evaluator is not None:
        step_str = f'Action:{step_name}({arguments})\nObservation: {observation}'
        evaluator.evaluate_step(step_str)
        log_interaction('/evaluate_after_step', {'step': step_str})
    return jsonify({'observation': observation, 'done': done})

@app.route('/check_flag', methods=['POST'])
def check_flag():
    """Input flag, output if it is correct using FinalAnswer tool and PentestDriver.step."""
    global driver
    data = request.json
    flag = data['flag']
    log_interaction('/check_flag', data)
    final_answer_tool = FinalAnswer(flag=flag)
    observation, done = driver.step(final_answer_tool)
    
    return jsonify({'is_flag': done, 'observation': observation})

@app.route('/evaluate', methods=['POST'])
def evaluate():
    """Input action and observation, output evaluation."""
    global evaluator
    data = request.json
    log_interaction('/evaluate', data)
    action = data.get('action')
    observation = data.get('observation')
    if action is not None and observation is not None:
        step = f'Action:{action}\nObservation: {observation}'
    else:
        step = data.get('step')
    # This will print and update milestones as in the notebook
    evaluator.evaluate_step(step)
    
    return jsonify({'status': 'evaluated'})

# Default route
@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the AutoPenBench server! Use /load_task, /step, /check_flag, or /evaluate endpoints.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
