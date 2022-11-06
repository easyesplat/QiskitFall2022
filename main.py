import qiskit
from qiskit import IBMQ
from config import API_KEY

IBMQ.save_account(API_KEY)
IBMQ.load_account()

print(qiskit.__qiskit_version__)
