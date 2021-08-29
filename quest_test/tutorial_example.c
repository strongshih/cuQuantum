/** @file 
 * A demo of QuEST
 *
 * @author Ania Brown
 * @author Tyson Jones
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>
#include "QuEST.h"

int main (int narg, char *varg[]) {

    srand( time(NULL) );

    /*
     * PREPARE QuEST environment
     * (Required only once per program)
     */

    QuESTEnv env = createQuESTEnv();

    printf("-------------------------------------------------------\n");
    printf("Running QuEST tutorial:\n\t Basic circuit involving a system of 3 qubits.\n");
    printf("-------------------------------------------------------\n");



    /*
     * PREPARE QUBIT SYSTEM
     */

	int n_qregs = atoi(varg[1]);
	int depth = 10000;
    Qureg qubits = createQureg(n_qregs, env);
    initZeroState(qubits);



    /*
     * REPORT SYSTEM AND ENVIRONMENT
     */
    printf("\nThis is our environment:\n");
    reportQuregParams(qubits);
    reportQuESTEnv(env);



    /*
     * APPLY CIRCUIT
     */
    struct timeval begin, end;
    gettimeofday(&begin, 0);

    for (int i = 0; i < n_qregs; i++) {
        hadamard(qubits, i);
        pauliX(qubits, i);
	}
    for (int i = 0; i < n_qregs-1; i++)
        controlledNot(qubits, i, i+1);

    int count = 0;
    for (int i = 0; i < depth-3; i++) {
        for (int j = 0; j < n_qregs; j++) {
		    double x = (double) rand() / (RAND_MAX + 1.0);
            if (x > 0.1) {
		        double y = (double) rand() / (RAND_MAX + 1.0);
                count += 1;
				if (y < 0.25) 
                    pauliX(qubits, j);
                else if (y < 0.5 && y >= 0.25)
                    hadamard(qubits, j);
                else if (y < 0.75 && y >= 0.5) {
		            double zz = (double) rand() / (RAND_MAX + 1.0);
                    double angle = (double) rand() / (RAND_MAX + 1.0);
                    if (zz < 0.333)
                        rotateX(qubits, j, angle);
                    else if (zz < 0.666 && zz >= 0.333)					
                        rotateY(qubits, j, angle);
                    else
                        rotateZ(qubits, j, angle);
				}
                else {
                    controlledNot(qubits, j, (j+1)%n_qregs);
                }
			}			
		}
	} 

    gettimeofday(&end, 0);
    long seconds = end.tv_sec - begin.tv_sec;
    long microseconds = end.tv_usec - begin.tv_usec;
    double elapsed = seconds + microseconds*1e-6;

    printf("--- Depth %d ---\n", depth);
    printf("--- Gate count %d ---\n", count);
    printf("--- Sec/gate %lf ---\n", elapsed/(double)count);
    printf("--- Total %lf seconds ---\n", elapsed);
    
    /*
     * STUDY QUANTUM STATE
     */
    /*
    printf("\nCircuit output:\n");

    qreal prob;
    prob = getProbAmp(qubits, 7);
    printf("Probability amplitude of |111>: %g\n", prob);

    prob = calcProbOfOutcome(qubits, 2, 1);
    printf("Probability of qubit 2 being in state 1: %g\n", prob);

    int outcome = measure(qubits, 0);
    printf("Qubit 0 was measured in state %d\n", outcome);

    outcome = measureWithStats(qubits, 2, &prob);
    printf("Qubit 2 collapsed to %d with probability %g\n", outcome, prob);
    */


    /*
     * FREE MEMORY
     */

    destroyQureg(qubits, env); 


    /*
     * CLOSE QUEST ENVIRONMET
     * (Required once at end of program)
     */
    destroyQuESTEnv(env);
    return 0;
}
