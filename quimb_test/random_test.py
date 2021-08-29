import random
import quimb as qu
import quimb.tensor as qtn
import time
import nvidia_smi
import sys

qtn.set_contract_backend('cupy')
qtn.set_tensor_linop_backend('cupy')

N = int(sys.argv[1])
circ = qtn.Circuit(N)

# randomly permute the order of qubits
regs = list(range(N))
random.shuffle(regs)

depth = 20

# hamadard on one of the qubits
for i in range(N):
    circ.apply_gate('H', regs[i])
    circ.apply_gate('X', regs[i])

# chain of cnots to generate GHZ-state
for i in range(N - 1):
    circ.apply_gate('CNOT', regs[i], regs[i + 1])

start_time = time.time()
count = N*3-1
for i in range(depth-3):
    for idx in range(N):
        if random.random() > 0.1:
            which = random.random()
            count += 1
            if which < 0.25:
                circ.apply_gate('H', regs[idx])
            elif which < 0.5 and which >= 0.25:
                circ.apply_gate('X', regs[idx])
            elif which < 0.75 and which >= 0.5:
                circ.apply_gate('U3', random.random(), random.random(), random.random(), regs[idx])
            else:
                circ.apply_gate('CNOT', regs[idx], regs[(idx + 1) % N])

#circ.amplitude('1'*N)
for b in circ.sample(1, backend='cupy'):
    print(b)
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


