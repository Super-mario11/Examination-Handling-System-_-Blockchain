from flask import Flask, render_template, jsonify, request
import os
import json
from web3 import Web3

app = Flask(__name__)

# Connect to Ganache/Hardhat local blockchain
# Ensure Hardhat node is running (npx hardhat node)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Check if connected
if not w3.is_connected():
    print("Not connected to Web3 provider!")
else:
    print("Connected to Web3 provider!")

# Load contract ABI and bytecode
CONTRACT_ADDRESS = None # This will be set after deployment

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deploy-contract', methods=['POST'])
def deploy_contract():
    global CONTRACT_ADDRESS
    try:
        with open('/home/shadower/Desktop/Blockchain V2/blockchain/artifacts/contracts/Examination.sol/Examination.json') as f:
            contract_json = json.load(f)
        abi = contract_json['abi']
        bytecode = contract_json['bytecode']

        Examination = w3.eth.contract(abi=abi, bytecode=bytecode)

        # Get the default account (usually the first one from Hardhat node)
        acct = w3.eth.accounts[0]

        # Build transaction
        tx_hash = Examination.constructor().transact({'from': acct})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        CONTRACT_ADDRESS = tx_receipt.contractAddress
        print(f"Contract deployed at: {CONTRACT_ADDRESS}")

        return jsonify({'message': f'Contract deployed successfully at {CONTRACT_ADDRESS}'})
    except Exception as e:
        print(f"Error deploying contract: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/assign-role', methods=['POST'])
def assign_role():
    if not CONTRACT_ADDRESS:
        return jsonify({'error': 'Contract not deployed yet.'}), 400
    try:
        data = request.get_json()
        user_address = w3.to_checksum_address(data['userAddress'])
        role = int(data['role']) # 1 for Teacher, 2 for Student

        with open('/home/shadower/Desktop/Blockchain V2/blockchain/artifacts/contracts/Examination.sol/Examination.json') as f:
            contract_json = json.load(f)
        abi = contract_json['abi']
        
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
        acct = w3.eth.accounts[0]

        tx_hash = contract.functions.assignRole(user_address, role).transact({'from': acct})
        w3.eth.wait_for_transaction_receipt(tx_hash)

        return jsonify({'message': 'Role assigned successfully.'})
    except Exception as e:
        print(f"Error assigning role: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get-role/<string:user_address>', methods=['GET'])
def get_role(user_address):
    user_address = w3.to_checksum_address(user_address)
    if not CONTRACT_ADDRESS:
        return jsonify({'error': 'Contract not deployed yet.'}), 400
    try:
        with open('/home/shadower/Desktop/Blockchain V2/blockchain/artifacts/contracts/Examination.sol/Examination.json') as f:
            contract_json = json.load(f)
        abi = contract_json['abi']
        
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
        
        role_id = contract.functions.getRole(user_address).call()
        roles = {0: "None", 1: "Teacher", 2: "Student"}
        role_name = roles.get(role_id, "Unknown")

        return jsonify({'role': role_name})
    except Exception as e:
        print(f"Error getting role: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/create-exam', methods=['POST'])
def create_exam():
    if not CONTRACT_ADDRESS:
        return jsonify({'error': 'Contract not deployed yet.'}), 400
    try:
        data = request.get_json()
        name = data['name']
        total_marks = int(data['totalMarks'])
        passing_marks = int(data['passingMarks'])

        with open('/home/shadower/Desktop/Blockchain V2/blockchain/artifacts/contracts/Examination.sol/Examination.json') as f:
            contract_json = json.load(f)
        abi = contract_json['abi']
        
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
        acct = w3.eth.accounts[0]

        tx_hash = contract.functions.createExam(name, total_marks, passing_marks).transact({'from': acct})
        w3.eth.wait_for_transaction_receipt(tx_hash)

        return jsonify({'message': 'Exam created successfully.'})
    except Exception as e:
        print(f"Error creating exam: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get-exam/<int:exam_id>', methods=['GET'])
def get_exam(exam_id):
    if not CONTRACT_ADDRESS:
        return jsonify({'error': 'Contract not deployed yet.'}), 400
    try:
        with open('/home/shadower/Desktop/Blockchain V2/blockchain/artifacts/contracts/Examination.sol/Examination.json') as f:
            contract_json = json.load(f)
        abi = contract_json['abi']
        
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
        
        exam = contract.functions.getExam(exam_id).call()
        
        if exam[0] == 0: # Check if exam exists (id is 0 if not found)
            return jsonify({'error': 'Exam not found.'}), 404

        exam_data = {
            'id': exam[0],
            'name': exam[1],
            'totalMarks': exam[2],
            'passingMarks': exam[3],
            'active': exam[4]
        }
        return jsonify(exam_data)
    except Exception as e:
        print(f"Error getting exam: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/update-exam', methods=['POST'])
def update_exam():
    if not CONTRACT_ADDRESS:
        return jsonify({'error': 'Contract not deployed yet.'}), 400
    try:
        data = request.get_json()
        _id = int(data['id'])
        name = data['name']
        total_marks = int(data['totalMarks'])
        passing_marks = int(data['passingMarks'])
        active = bool(data['active'])

        with open('/home/shadower/Desktop/Blockchain V2/blockchain/artifacts/contracts/Examination.sol/Examination.json') as f:
            contract_json = json.load(f)
        abi = contract_json['abi']
        
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
        acct = w3.eth.accounts[0]

        tx_hash = contract.functions.updateExam(_id, name, total_marks, passing_marks, active).transact({'from': acct})
        w3.eth.wait_for_transaction_receipt(tx_hash)

        return jsonify({'message': 'Exam updated successfully.'})
    except Exception as e:
        print(f"Error updating exam: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/submit-exam', methods=['POST'])
def submit_exam():
    if not CONTRACT_ADDRESS:
        return jsonify({'error': 'Contract not deployed yet.'}), 400
    try:
        data = request.get_json()
        exam_id = int(data['examId'])
        answers_hash = data['answersHash']
        student_address_from_frontend = w3.to_checksum_address(data['studentAddress'])

        with open('/home/shadower/Desktop/Blockchain V2/blockchain/artifacts/contracts/Examination.sol/Examination.json') as f:
            contract_json = json.load(f)
        abi = contract_json['abi']
        
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
        # Use the student's address from the frontend as the sender
        tx_hash = contract.functions.submitExam(exam_id, answers_hash).transact({'from': student_address_from_frontend})
        w3.eth.wait_for_transaction_receipt(tx_hash)

        return jsonify({'message': 'Exam submitted successfully.'})
    except Exception as e:
        print(f"Error submitting exam: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/grade-exam', methods=['POST'])
def grade_exam():
    if not CONTRACT_ADDRESS:
        return jsonify({'error': 'Contract not deployed yet.'}), 400
    try:
        data = request.get_json()
        exam_id = int(data['examId'])
        student_address = w3.to_checksum_address(data['studentAddress'])
        grade = int(data['grade'])

        with open('/home/shadower/Desktop/Blockchain V2/blockchain/artifacts/contracts/Examination.sol/Examination.json') as f:
            contract_json = json.load(f)
        abi = contract_json['abi']
        
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
        acct = w3.eth.accounts[0]

        # Log the role of the account attempting to grade
        contract_instance = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
        current_role_id = contract_instance.functions.getRole(acct).call()
        roles = {0: "None", 1: "Teacher", 2: "Student"}
        current_role_name = roles.get(current_role_id, "Unknown")
        print(f"Account {acct} has role: {current_role_name}")

        tx_hash = contract.functions.gradeExam(exam_id, student_address, grade).transact({'from': acct})
        w3.eth.wait_for_transaction_receipt(tx_hash)

        return jsonify({'message': 'Exam graded successfully.'})
    except Exception as e:
        print(f"Error grading exam: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get-submission/<int:exam_id>/<string:student_address>', methods=['GET'])
def get_submission(exam_id, student_address):
    student_address = w3.to_checksum_address(student_address)
    if not CONTRACT_ADDRESS:
        return jsonify({'error': 'Contract not deployed yet.'}), 400
    try:
        with open('/home/shadower/Desktop/Blockchain V2/blockchain/artifacts/contracts/Examination.sol/Examination.json') as f:
            contract_json = json.load(f)
        abi = contract_json['abi']
        
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
        
        submission = contract.functions.getSubmission(exam_id, student_address).call()
        
        if submission[0] == 0: # Check if submission exists
            return jsonify({'error': 'Submission not found.'}), 404

        submission_data = {
            'examId': submission[0],
            'studentAddress': submission[1],
            'answersHash': submission[2],
            'grade': submission[3],
            'graded': submission[4]
        }
        return jsonify(submission_data)
    except Exception as e:
        print(f"Error getting submission: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get-exam-id-counter', methods=['GET'])
def get_exam_id_counter():
    if not CONTRACT_ADDRESS:
        return jsonify({'error': 'Contract not deployed yet.'}), 400
    try:
        with open('/home/shadower/Desktop/Blockchain V2/blockchain/artifacts/contracts/Examination.sol/Examination.json') as f:
            contract_json = json.load(f)
        abi = contract_json['abi']
        
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
        
        counter = contract.functions.examIdCounter().call()
        return jsonify({'examIdCounter': counter})
    except Exception as e:
        print(f"Error getting exam ID counter: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

