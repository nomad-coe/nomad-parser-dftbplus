import setup_paths
from nomadcore.simple_parser import SimpleMatcher as SM, mainFunction
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
import os, sys, json

# description of the input
mainFileDescription = SM(
    name = 'root',
    weak = True,
    forwardMatch = True,
    startReStr = "",
    subMatchers = [
        SM(name = 'newRun',
           startReStr = r"\s*Fermi distribution function",
           #repeats = True,
           required = True,
           forwardMatch = True,
           sections   = ['section_run'],
           subMatchers = [
               SM(name = 'header',
                  startReStr = r"\s*Fermi distribution function",
                  #forwardMatch = True,
                  #subMatchers=[ ]
             ),
               SM(name = 'coordinates',
                  startReStr = r"\s*Coordinates of moved atoms\s*\(?(au)?\)?:",
                  #forwardMatch = True,
                  sections   = ['section_system','section_molecule_type'],
                  subMatchers = [
                      SM(r"\s*Coordinates of moved atoms\s*\(?(au)?\)?:"),
                      SM(r"\s*(?P<atom>\d+)\s*(?P<x_dftbp_atom_positions_X>[+-]?\d+\.\d+)\s*(?P<x_dftbp_atom_positions_Y>[+-]?\d+\.\d+)\s*(?P<x_dftbp_atom_positions_Z>[+-]?\d+\.\d+)\s*", repeats = True),
                 ],
             ),
               SM(name = 'charges',
                  startReStr = r"\s*Net atomic charges .e.",
                  #endReStr = r"\s*",
                  #forwardMatch = True,
                  sections   = ['section_molecule_type'],
                  subMatchers = [
                      SM(r"\s*Atom\s*Net charge"),
                      SM(r"\s*(?P<atom>\d+)\s*(?P<atom_in_molecule_charge>[+-]?\d+\.\d+)\s*", repeats = True),
                                 #SM(r"\s*")
                  ],
             ),
               SM(name = 'eigenvalues_H',
                  startReStr = r"\s*Eigenvalues /H",
                  #forwardMatch = True,
                  sections   = ['section_eigenvalues'],
                  subMatchers = [
                      SM(r"\s*Eigenvalues /H"),
                      SM(r"\s*(?P<eigenvalues_values__hartree>[+-]?\d+\.\d+)\s*", repeats = True),
                  ],
             ),
                 SM(name = 'eigenvalues_eV',
                    startReStr = r"\s*Eigenvalues /eV",
                    #forwardMatch = True,
                    sections   = ['section_eigenvalues'],
                    subMatchers = [
                        SM(r"\s*Eigenvalues /eV"),
                        SM(r"\s*(?P<eigenvalues_values>[+-]?\d+\.\d+)\s*", repeats = True),
                  ],
             ),
                  SM(name = 'Occupations',
                     startReStr = r"\s*Fillings",
                     #forwardMatch = True,
                     sections   = ['section_eigenvalues'],
                     subMatchers = [
                        SM(r"\s*Fillings"),
                        SM(r"\s*(?P<eigenvalues_occupation>\d+\.\d+)\s*", repeats = True),
                  ],
             ),
               SM(name = 'energies',
                  startReStr = r"\s*Fermi energy:.*",
                  sections   = ['section_single_configuration_calculation'],
                  subMatchers = [
                     SM(r"\s*Fermi energy:.*"),
                     #SM(r"\s*Band energy:.*"),
                     SM(r"\s*Total energy:\s*(?P<energy_total__hartree>[+-]?\d+\.\d+)\s*H.*"),
                     SM(r"\s*Total Mermin free energy:\s*(?P<energy_free__hartree>[+-]?\d+\.\d+)\s*H.*"),
                   ],
                  #forwardMatch = True,
                  #required = True,
             ),
               SM(name = 'forces',
                  startReStr = r"\s*Total Forces",
                  sections   = ['section_single_configuration_calculation'],
                  subMatchers = [
                     SM(r"\s*Total Forces*"),
                     SM(r"\s*(?P<x_dftbp_atom_forces_X>[+-]?\d+\.\d+E?[+-]?\d+)\s*(?P<x_dftbp_atom_forces_Y>[+-]?\d+\.\d+E?[+-]?\d+)\s*(?P<x_dftbp_atom_forces_Z>[+-]?\d+\.\d+E?[+-]?\d+)\s*", repeats = True),
                     SM(r"\s*Maximal force component:\s*(?P<x_dftbp_force_max>[+-]?\d+\.\d+E?[+-]?\d+)\s*"),
                     SM(r"\s*Max force for moved atoms::\s*(?P<x_dftbp_force_max>[+-]?\d+\.\d+E?[+-]?\d+)\s*(au)?"),
                   ],

             ),
           ])
        ])

# loading metadata from nomad-meta-info/meta_info/nomad_meta_info/dftb-plus.nomadmetainfo.json

parserInfo = {
  "name": "parser_dftb+",
  "version": "1.0"
}

metaInfoPath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../../../../nomad-meta-info/meta_info/nomad_meta_info/dftb-plus.nomadmetainfo.json"))
metaInfoEnv, warnings = loadJsonFile(filePath = metaInfoPath, dependencyLoader = None, extraArgsHandling = InfoKindEl.ADD_EXTRA_ARGS, uri = None)

if __name__ == "__main__":
    mainFunction(mainFileDescription, metaInfoEnv, parserInfo)
