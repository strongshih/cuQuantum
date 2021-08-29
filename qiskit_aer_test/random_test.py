import qiskit
from qiskit import IBMQ
from qiskit.providers.aer import AerSimulator
import random
import time
import nvidia_smi
import sys

# Generate 3-qubit GHZ state
n_qregs = int(sys.argv[1])
depth = 10000

circ = qiskit.QuantumCircuit(n_qregs)
for idx in range(n_qregs):
    circ.h(idx)
    circ.x(idx)
for idx in range(0, n_qregs - 1):
    circ.cx(idx, idx+1)
count = n_qregs*3-1

for i in range(depth-3):
    for idx in range(n_qregs):
        if random.random() > 0.1:
            which = random.random()
            count += 1
            if which < 0.25:
                circ.x(idx)
            elif which < 0.5 and which >= 0.25:
                circ.h(idx)
            elif which < 0.75 and which >= 0.5:
                circ.u(random.random(), random.random(), random.random(), idx)
            else:
                circ.cx(idx, (idx + random.randint(1, n_qregs-1)) % n_qregs)

circ.measure_all()

# Construct an ideal simulator
aersim = AerSimulator()

# Perform an ideal simulation
start_time = time.time()
result_ideal = qiskit.execute(circ, aersim).result()
cur = (time.time() - start_time)
print("--- Depth %s ---" % str(depth))
print("--- Gate count %s ---" % count)
print("--- Sec/gate %s ---" % str(float(cur)/float(count)))
print("--- Total %s seconds ---" % cur)

nvidia_smi.nvmlInit()
handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
print("Device {}: {}, Memory : ({:.2f}% free): {}(total), {} (free), {} (used)".format(0, nvidia_smi.nvmlDeviceGetName(handle), 100*info.free/info.total, info.total, info.free, info.used))
nvidia_smi.nvmlShutdown()


# counts_ideal = result_ideal.get_counts(0)
# print('Counts(ideal):', counts_ideal)
# Counts(ideal): {'000': 493, '111': 531}

# Construct a noisy simulator backend from an IBMQ backend
# This simulator backend will be automatically configured
# using the device configuration and noise model 
# provider = IBMQ.load_account()
# backend = provider.get_backend('ibmq_athens')
# aersim_backend = AerSimulator.from_backend(backend)

# Perform noisy simulation
# result_noise = qiskit.execute(circ, aersim_backend).result()
# counts_noise = result_noise.get_counts(0)

# print('Counts(noise):', counts_noise)
