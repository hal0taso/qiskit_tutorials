# -*- coding: utf-8 -*-

# Check version of Python; supported > 3.5
import sys
if sys.version_info < (3, 5):
    raise Exception('Please use Python version 3.5 or greater.')

from qiskit import QuantumProgram
import Qconfig


# Creating Programs :
# create your first QuantumProgram object instance
qp = QuantumProgram()


# Creating Registers :
# create your first Quantum Register called "qr" with 2 qubits
qr = qp.create_quantum_register('qr', 2)
# create your first Classical Register called "cr" with 2 bits
cr = qp.create_classical_register('cr', 2)


# Creating Circuits
# create your first Quantum Circuit called "qc" involving your Quantum Register "qr"
# and your Classical Register "cr"
qc = qp.create_circuit('Circuit', [qr], [cr])


# another option for creating your QuantumProgram instance:
Q_SPECS = {
    'circuits': [{
        'name': 'Circuit',
        'quantum_registers': [{
            'name': 'qr',
            'size': 4
        }],
        'classical_registers': [{
            'name': 'cr',
            'size': 4
        }]
    }],
}

qp = QuantumProgram(specs=Q_SPECS)


# Get the components:
# get the circuit by Name
circuit = qp.get_circuit('Circuit')

# get the Quantum Register by Name
quantum_r = qp.get_quantum_register('qr')

# get the Classical Register by Name
classical_r = qp.get_classical_register('cr')

# Building your Program: Add Gates to your Circuit !!
# Pauli X gate to qubit 1 in the Quantum Register "qr"
circuit.x(quantum_r[1])

# Pauli Y gate to qubit 2 in the Quantum Register "qr"
circuit.y(quantum_r[2])

# Pauli Z gate to qubit 3 in the Quantum Register "qr"
circuit.z(quantum_r[3])

# CNOT (Controlled-NOT) gate from qubit 3 to qubit 2
circuit.cx(quantum_r[3], quantum_r[2])

# add a barrier to your circuit
circuit.barrier()

# H (Hadamard) gate to qubit 0 in the Quantum Register "qr"
circuit.h(quantum_r[0])

# S Phase gate to qubit 0
circuit.s(quantum_r[0])

# T Phase gate to qubit 1
circuit.t(quantum_r[1])

# identity gate to qubit
circuit.iden(quantum_r[1])

# first physical gete: u1(lambda) to qubit 0
circuit.u1(0.3, quantum_r[0])

# second physical gate: u2(phi, lambda) to qubit 1
circuit.u2(0.3, 0.2, quantum_r[1])

# third physical gate: u3(theta, phi, lambda) to qubit 2
circuit.u3(0.3, 0.2, 0.1, quantum_r[2])

# rotation around the x-axis to qubit 0
circuit.rx(0.2, quantum_r[0])

# rotation aroud the y-axis to qubit 1
circuit.ry(0.2, quantum_r[1])

# rotation aroud the z-acis to qubit 2
circuit.rz(0.2, quantum_r[2])


# Classical if, from qubit2 gate Z to classical bit 1
# circuit.z(quantum_r[2]).c_if(classical_r, 0)

# measure gate drom qubit 0 to classical bit 0
print(circuit.measure(quantum_r[0], classical_r[0]),
      circuit.measure(quantum_r[1], classical_r[1]),
      circuit.measure(quantum_r[2], classical_r[2]),)

QASM_source = qp.get_qasm('Circuit')

print(QASM_source)

import os
import shutil
from qiskit.tools.visualization import latex_drawer
import pdf2image


def circuitImage(circuit, basis="u1,u2,u3,cx"):
    """Obtain the circuit in image format
    Note: Requires pdflatex installed (to compile Latex)
    Note: Required pdf2image Python package (to display pdf as image)
    """
    filename = 'circuit'
    tmpdir = 'tmp/'
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)
    latex_drawer(circuit, tmpdir + filename + ".tex", basis=basis)
    os.system("pdflatex -output-directory {} {}".format(tmpdir, filename + ".tex"))
    images = pdf2image.convert_from_path(tmpdir + filename + ".pdf")
    shutil.rmtree(tmpdir)
    return images[0]


basis = "u1,u2,u3,cx,x,y,z,h,s,t,rx,ry,rz"
# circuitImage(circuit, basis)

## Compile and Run or Execute
# First we need to choose the backend. Lets start with the local simulator
backend = 'local_qasm_simulator'
circuits = ['Circuit']  # Group of circuits to execute

# Next we need to compile the circuits into a quantum object which we call qobj
qobj = qp.compile(circuits, backend)  # Compile your program

# Then you can run your program. Using wait and timeout we can check the execution result every 2 seconds and timeout if the job is not run in 240 seconds.
