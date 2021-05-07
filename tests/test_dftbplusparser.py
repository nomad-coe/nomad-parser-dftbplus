#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
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

import pytest
import numpy as np

from nomad.datamodel import EntryArchive
from dftbplusparser import DFTBPlusParser


def approx(value, abs=0, rel=1e-6):
    return pytest.approx(value, abs=abs, rel=rel)


@pytest.fixture(scope='module')
def parser():
    return DFTBPlusParser()


def test_basic(parser):
    archive = EntryArchive()
    parser.parse('tests/data/detailed.out', archive, None)

    sec_system = archive.section_run[0].section_system[0]
    assert np.shape(sec_system.atom_positions) == (114, 3)
    assert sec_system.atom_positions[78][2].magnitude == approx(-8.56177558e-09)

    sec_scc = archive.section_run[0].section_single_configuration_calculation[0]
    assert sec_scc.energy_total.magnitude == approx(-9.74752048e-16)
    assert sec_scc.energy_reference_fermi[0].magnitude == approx(-6.54344613e-19)
    assert sec_scc.atom_forces[108][1].magnitude == approx(-1.65415666e-12)
