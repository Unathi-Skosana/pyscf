# Copyright 2014-2019 The PySCF Developers. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Samragni Banerjee <samragnibanerjee4@gmail.com>
#         Alexander Sokolov <alexander.y.sokolov@gmail.com>
#

import unittest
import numpy
from pyscf import gto
from pyscf import scf
from pyscf import adc

def setUpModule():
    global mol, mf, myadc
    r = 1.098
    mol = gto.Mole()
    mol.atom = [
        ['N', ( 0., 0.    , -r/2   )],
        ['N', ( 0., 0.    ,  r/2)],]
    mol.basis = {'N':'aug-cc-pvdz'}
    mol.verbose = 0
    mol.build()
    mf = scf.RHF(mol)
    mf.conv_tol = 1e-12
    mf.kernel()
    myadc = adc.ADC(mf)

def tearDownModule():
    global mol, mf, myadc
    del mol, mf, myadc

class KnownValues(unittest.TestCase):

    def test_ip_adc2(self):
  
        e, t_amp1, t_amp2 = myadc.kernel_gs()
        self.assertAlmostEqual(e, -0.32201692499346535, 6)

        e,v,p,x,es = myadc.ip_adc(nroots=3)
        es.analyze()

        self.assertAlmostEqual(e[0], 0.5434389910483670, 6)
        self.assertAlmostEqual(e[1], 0.6240296243595950, 6)
        self.assertAlmostEqual(e[2], 0.6240296243595956, 6)

        self.assertAlmostEqual(p[0], 1.7688097076459075, 6)
        self.assertAlmostEqual(p[1], 1.8192921131700284, 6)
        self.assertAlmostEqual(p[2], 1.8192921131700293, 6)

    def test_ip_adc2_oneroot(self):
  
        e,v,p,x = myadc.kernel()

        self.assertAlmostEqual(e[0], 0.5434389910483670, 6)

        self.assertAlmostEqual(p[0], 1.7688097076459075, 6)

    def test_ip_adc2x(self):
  
        myadc.method = "adc(2)-x"

        e,v,p,x = myadc.kernel(nroots=3)
        e_corr = myadc.e_corr 

        self.assertAlmostEqual(e_corr, -0.32201692499346535, 6)

        self.assertAlmostEqual(e[0], 0.5405255360673243, 6)
        self.assertAlmostEqual(e[1], 0.6208026698756092, 6)
        self.assertAlmostEqual(e[2], 0.6208026698756107, 6)

        self.assertAlmostEqual(p[0], 1.7513284912002309, 6)
        self.assertAlmostEqual(p[1], 1.8152869633769022, 6)
        self.assertAlmostEqual(p[2], 1.8152869633769015, 6)

    def test_ip_adc3(self):
  
        myadc.method = "adc(3)"
        myadc.method_type = "ip"

        e,v,p,x = myadc.kernel(nroots=3)
        e_corr = myadc.e_corr

        self.assertAlmostEqual(e_corr, -0.31694173142858517 , 6)

        self.assertAlmostEqual(e[0], 0.5667526829981027, 6)
        self.assertAlmostEqual(e[1], 0.6099995170092525, 6)
        self.assertAlmostEqual(e[2], 0.6099995170092529, 6)

        self.assertAlmostEqual(p[0], 1.8173191958988848, 6)
        self.assertAlmostEqual(p[1], 1.8429224413853840, 6)
        self.assertAlmostEqual(p[2], 1.8429224413853851, 6)
      
if __name__ == "__main__":
    print("IP calculations for different RADC methods for nitrogen molecule")
    unittest.main()
