import qgate
from qgate.script import *
import numpy as np
import random
import time
import nvidia_smi
import sys

n_qregs = int(sys.argv[1])
qregs = new_qregs(n_qregs)
empty = new_qregs(3)

cregs = new_references(n_qregs)

depth = 10000
circuit = []
circuit.append([H(qreg) for qreg in qregs])
circuit.append([X(qreg) for qreg in qregs])
circuit.append([ctrl(qregs[idx]).X(qregs[idx + 1]) for idx in range(0, n_qregs - 1)])
count = n_qregs*3-1
for i in range(depth-3):
    g = []
    for idx, qreg in enumerate(qregs):
        choices = [X(qreg), 
                   H(qreg), 
                   U3(random.random(), random.random(), random.random()).Adj(qreg),
                   ctrl(qregs[idx]).X(qregs[(idx + random.randint(1, n_qregs-1)) % n_qregs])]
        if random.random() > 0.1:
            g.append(random.choice(choices))
            count += 1
            break
    circuit.append(g)

#qgate.dump(circuit)


start_time = time.time()
sim = qgate.simulator.cuda()
sim.run(circuit)
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


if False :
    # get reduced prob array.
    class DummySamplingPool :
        def __init__(self, prob, empty_lanes, qreg_ordering) :
            self.prob = prob
            self.empty_lanes = empty_lanes
            self.qreg_ordering = qreg_ordering

    spool = sim.qubits.create_sampling_pool(qregs[2:], DummySamplingPool)
    print(len(spool.prob))

np.random.seed(0)

spool = sim.qubits.create_sampling_pool(qregs[2:])
obslist = spool.sample(1024)
#print(obslist)

#print('histgram:')
#print(obslist.histgram())

#qgate.dump(obslist)
#qgate.dump(obslist.histgram())
