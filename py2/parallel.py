#!usr/bin/python2.7

#################################
#
# Parallel programming examples
#
#################################

from __future__ import print_function
from multiprocessing import Pool, Process
import multiprocessing as mp
import numpy as np

import pathos.pools as pp

def sqrt(x):
    return np.sqrt(x)

def call_pool_map(processes=4):
    pool = Pool(processes=processes)
    roots = pool.map(sqrt, range(100))
    print(roots)

def call_pool_async(processes=4):
    pool = Pool(processes=processes)
    results = [pool.apply_async(sqrt, (x,)) for x in range(100)]
    roots = [r.get() for r in results]
    print(roots)

class RootHolder():
    """ Holdings a list of numbers with class methods to return the square roots """
    def __init__(self, num_list):
        self.num_list = num_list
        print("RootHolder class initiated.")

    def get_sqrts_basic(self):
        """ Not using parallel """
        return np.sqrt(self.num_list)

    def get_sqrts_parallel_outside(self, processes=4):
        """ Uses parallel, but calls the sqrt function defined outside of the class, so no problems occur """
        print("\nCalling sqrt function defined outside of the class.")
        pool = Pool(processes=processes)
        results = [pool.apply_async(sqrt, (x,)) for x in self.num_list]
        roots = [r.get() for r in results]
        return roots

    def _sqrt(self, x):
        """ Bound class method for parallel example """
        return np.sqrt(x)

    def get_sqrts_parallel_bound(self, processes=4):
        """ Uses parallel, but runs into error with bound class method _sqrt(x) """
        print("\nCalling sqrt function defined as a bound class method.  Results in a pickling error with Py2.")
        pool = Pool(processes=processes)
        roots = pool.map(self._sqrt, self.num_list)
        return roots

    def get_sqrts_parallel_bound_soln(self, processes=4):
        """ Uses parallel and resolves pickling error by using pathos package, which provides serialization of the bound class method """
        print("\nCalling sqrt function defined as a bound class method.  Treat with pathos.multiprocessing.")
        pool = pp.ProcessPool(processes)
        roots = pool.map(self._sqrt, self.num_list)
        return roots


if __name__ == '__main__':
    print("CPU Count: {0}\n".format(str(mp.cpu_count())))

    print("Simple multiprocessing calls:\n")
    call_pool_map()
    call_pool_async()

    print("Multiprocessing calls via a class:")
    tst = RootHolder(range(20))

    print(tst.get_sqrts_parallel_outside())

    try:
        print(tst.get_sqrts_parallel_bound())
    except Exception, error:
        print(error)

    print(tst.get_sqrts_parallel_bound_soln())