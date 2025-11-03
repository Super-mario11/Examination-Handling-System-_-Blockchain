# Examination Handling System with Blockchain

This project implements an Examination Handling System using Flask for the backend and Hardhat for blockchain integration. The system allows for the creation and management of examinations on a decentralized ledger.

## Project Structure

- `backend/`: Contains the Flask application, including Python scripts, HTML templates, and static assets.
- `blockchain/`: Contains the Hardhat project for smart contract development and deployment.

## Getting Started

### Prerequisites

- Python 3.x
- Node.js and npm

### Backend Setup (Flask)

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
   The application will be accessible at `http://127.0.0.1:5000`.

### Blockchain Setup (Hardhat)

1. Navigate to the `blockchain` directory:
   ```bash
   cd blockchain
   ```
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Compile the smart contracts:
   ```bash
   npx hardhat compile
   ```
4. Deploy the smart contracts (example, you might need to configure your deployment script):
   ```bash
   npx hardhat run scripts/deploy.js --network localhost
   ```

## Usage

- Open your web browser and go to `http://127.0.0.1:5000`.
- Click the "Deploy Contract" button to interact with the blockchain (currently a placeholder).

## Future Enhancements

- Implement full contract deployment and interaction logic in the Flask backend.
- Develop a more comprehensive frontend for managing exams.
- Add user authentication and authorization.
- Integrate with a real blockchain network (e.g., Sepolia, Polygon).
