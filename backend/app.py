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
        with open('../blockchain/artifacts/contracts/Examination.sol/Examination.json') as f:
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

@app.route('/create-exam', methods=['POST'])
def create_exam():
    if not CONTRACT_ADDRESS:
        return jsonify({'error': 'Contract not deployed yet.'}), 400
    try:
        data = request.get_json()
        name = data['name']
        total_marks = int(data['totalMarks'])
        passing_marks = int(data['passingMarks'])

        with open('../blockchain/artifacts/contracts/Examination.sol/Examination.json') as f:
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
        with open('../blockchain/artifacts/contracts/Examination.sol/Examination.json') as f:
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

        with open('../blockchain/artifacts/contracts/Examination.sol/Examination.json') as f:
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

if __name__ == '__main__':
    app.run(debug=True)

