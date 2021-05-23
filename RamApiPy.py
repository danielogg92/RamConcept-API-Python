# -*- coding: utf-8 -*-
import os;
import sys;
from pathlib import Path

api_path='File_path_to_ramconcept_install\\RAM Concept CONNECT Edition\\RAM Concept CONNECT Edition V8\\python';
if(api_path not in sys.path):
    sys.path.append(api_path);
    
import ram_concept as rc;
from ram_concept.concept import Concept
from ram_concept.model import DesignCode
from ram_concept.model import Model
from ram_concept.model import StructureType

#define the file path that is to be used
file_path='file_path_of_ramconcept_model_to_use\\BLD E - LEVEL 09 - 201124 - IFC.cpt';

def attachToInstanceRam(model_path,headless=False):
    """
    attach to RamConcept model
    """
    #check that the file path exists
    if(os.path.isfile(model_path)==False):
        print('File {} does not exists'.format(model_path));
        return False;
    #attach to the model, every call will be thru concept
    concept=rc.concept.Concept.start_concept(headless);
    #open the model
    model=concept.open_file(model_path);
    return model,concept;

def close_model(model_concept):
    """
    close the model
    """
    #Close the model
    model_concept.shut_down();
    print('Model shut down');

def get_materials_concrete(model):
    """
    Get the concrete mixes in the model
    
    returns: conc_mixes (dict)
    """
    #get the model mixes
    conc_mixes={};#[['Mix Name','Density','Density for Loading','fci','fc','fcui','fcu',
                 #'Poissons','Thermal','Ec Calc','User Eci','User Ec']];
    for mix in model.concretes.concretes:
        mix_name=mix.name;
        coefficient_of_thermal_expansion=mix.coefficient_of_thermal_expansion;
        fc_initial=mix.fc_initial;
        fc_final=mix.fc_final;
        fcu_initial=mix.fcu_initial;
        fcu_final=mix.fcu_final;
        poissons_ratio=mix.poissons_ratio;
        unit_mass=mix.unit_mass;
        unit_unit_mass_for_loads=mix.unit_unit_mass_for_loads;
        if(unit_unit_mass_for_loads>10**4):
            unit_unit_mass_for_loads='Density';
        user_Ec_initial=mix.user_Ec_initial;
        user_Ec_final=mix.user_Ec_final;
        use_code_Ec=mix.use_code_Ec;
        conc_mixes[mix_name]={'unit_mass':unit_mass,
                              'unit_unit_mass_for_loads':unit_unit_mass_for_loads,
                              'fc_initial':fc_initial,
                              'fc_final':fc_final,
                              'fcu_initial':fcu_initial,
                              'fcu_final':fcu_final,
                              'poissons_ratio':poissons_ratio,
                              'coefficient_of_thermal_expansion':coefficient_of_thermal_expansion,
                              'use_code_Ec':use_code_Ec,
                              'user_Ec_initial':user_Ec_initial,
                              'user_Ec_final':user_Ec_final};
    return conc_mixes;
