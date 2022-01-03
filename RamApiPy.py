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

def get_pt_systems(model):
    """
    Get the pt systems defined in the model
    
    returns: pt_systems (dict)
    """
    #get the model pt systems
    pt_systems={};
    for pt in model.pt_systems.pt_systems:
        pt_name=pt.name;
        Aps=pt.Aps;
        Eps=pt.Eps;
        Fpu=pt.Fpu;
        Fpy=pt.Fpy;
        Fse=pt.Fse;
        anchor_friction=pt.anchor_friction;
        angular_friction=pt.angular_friction;
        duct_width=pt.duct_width;
        jack_stress=pt.jack_stress;
        long_term_losses=pt.long_term_losses;
        min_curvature_radius=pt.min_curvature_radius;
        seating_distance=pt.seating_distance;
        strands_per_duct=pt.strands_per_duct;
        system_type=pt.system_type.name;
        wobble_friction=pt.wobble_friction;
        pt_systems[pt_name]={'Aps':Aps,
                             'Eps':Eps,
                             'Fpu':round(Fpu,2),
                             'Fpy':Fpy,
                             'Fse':Fse,
                             'anchor_friction':anchor_friction,
                             'angular_friction':angular_friction,
                             'duct_width':duct_width,
                             'jack_stress':jack_stress,
                             'long_term_losses':long_term_losses,
                             'min_curvature_radius':min_curvature_radius,
                             'seating_distance':seating_distance,
                             'strands_per_duct':strands_per_duct,
                             'system_type':system_type,
                             'wobble_friction':wobble_friction};
    return pt_systems;

def get_all_layers(model):
    layer_enum=['structure_layer',
                'element_layer',
                'force_loading_layer',
                'load_combo_layer',
                'tendon_layer']
    layers={};
    for layer in model.cad_manager._get_all_layers():
        uid=layer.uid;
        layer_name=layer.name;
        layer_type='None Found';
        for enum in layer_enum:
            if(enum in str(layer)):
                layer_type=enum;
                continue;
        layers[uid]={'name':layer_name,
                     'layer_type':layer_type,
                     'object':layer};
    #Get the strength layers
    strength={};
    for layer in layers:
        if('Ultimate LC' in layers[layer]['name']):
            lay_point=layers[layer]['object'];
            #get envelope results layer
            erl=rc.result_layers.EnvelopeResultLayer(layer,model);
            layer_data=rc.data.Data(layer,model)
            #get the data name and number
            data_name=layer_data.name;
            data_number=layer_data.number;
            #get the childre on the data
            for item in layer_data._get_children():
                print(item.name);
            
            
            
    return None;

def get_slab_elements(model,min_output=False):
    """
    get the slab elements from the elements layer
    
    returns slab_elements (dict)
    """
    #get the element layer
    element_layer=model.cad_manager.element_layer;
    #initiate the slab elements dictionary
    slab_elements={};
    slab_elements_error=[];
    #loop thru the slab elements
    for slab_element in element_layer.slab_elements:
        try:
            #get the unique id
            uid=slab_element.uid;
            #get the data from slab element
            if(min_output==False):
                kFr=rc.elements.SlabElement(uid,model).kFr;
                kFs=rc.elements.SlabElement(uid,model).kFs;
                kMr=rc.elements.SlabElement(uid,model).kMr;
                kMrs=rc.elements.SlabElement(uid,model).kMrs;
                kMs=rc.elements.SlabElement(uid,model).kMs;
                kVrs=rc.elements.SlabElement(uid,model).kVrs;
                r_axis=rc.elements.SlabElement(uid,model).r_axis;
                toc=rc.elements.SlabElement(uid,model).toc;
            else:
                kFr,kFs,kMr,kMrs,kMs,kVrs,r_axis,toc=1.0,1.0,1.0,1.0,1.0,1.0,0,0;
            location=rc.elements.SlabElement(uid,model).location;
            thickness=rc.elements.SlabElement(uid,model).thickness;
            concrete_mix=slab_element.concrete.name;
            if('Polygon2D' in str(type(location))):
                point_count=location.point_count;
                points=location.points;
                point_coords=[];
                for pt in points:
                    point_coords.append((pt.x,pt.y));
                point_coords=tuple(point_coords);
            #add the slab area to the dictionary
            slab_elements[uid]={'uid':uid,'concrete_mix':concrete_mix,
                                'thickness':thickness,'toc':toc,
                                'kMr':kMr,'kMs':kMs,'kMrs':kMrs,
                                'kFr':kFr,'kFs':kFs,'kVrs':kVrs,
                                'r_axis':r_axis,
                                'location':location,
                                'point_count':point_count,
                                'points':points,
                                'point_coords':point_coords};
        except:
            print('Error occurred for slab uid: {}'.format(uid));
            slab_elements_error.append(uid);
    return slab_elements;

def get_column_elements(model):
    """
    get the column elements from the elements layer
    
    returns column_elements (dict)
    """
    #get the element layer
    element_layer=model.cad_manager.element_layer;
    #initiate the column elements dictionary
    column_elements={};
    #loop thru the column elements below
    for col_element in element_layer.column_elements_below:
        #get the unique id
        uid=col_element.uid;
        #get the data from slab element
        angle=rc.elements.ColumnElement(uid,model).angle;
        b=rc.elements.ColumnElement(uid,model).b;
        d=rc.elements.ColumnElement(uid,model).d;
        i_factor=rc.elements.ColumnElement(uid,model).i_factor;
        location=rc.elements.ColumnElement(uid,model).location;
        roller=rc.elements.ColumnElement(uid,model).roller;
        below_slab=rc.elements.ColumnElement(uid,model).below_slab;
        compressible=rc.elements.ColumnElement(uid,model).compressible;
        fixed_far=rc.elements.ColumnElement(uid,model).fixed_far;
        fixed_near=rc.elements.ColumnElement(uid,model).fixed_near;
        height=rc.elements.ColumnElement(uid,model).height;
        llr_max_reduction=rc.elements.ColumnElement(uid,model).llr_max_reduction;
        specified_LLR_levels=rc.elements.ColumnElement(uid,model).specified_LLR_levels;
        specified_influence_area=rc.elements.ColumnElement(uid,model).specified_influence_area;
        specified_trib_area=rc.elements.ColumnElement(uid,model).specified_trib_area;
        use_specified_LLR_parameters=rc.elements.ColumnElement(uid,model).use_specified_LLR_parameters;
        concrete_mix=col_element.concrete.name;
        number=rc.elements.ColumnElement(uid,model).number;
        name=rc.elements.ColumnElement(uid,model).name;
        point_coords=[location.x,location.y];
        #add the slab area to the dictionary
        column_elements[uid]={'uid':uid,'concrete_mix':concrete_mix,
                              'number':number,'name':name,
                              'b':b,'d':d,'i_factor':i_factor,'angle':angle,
                              'roller':roller,'below_slab':below_slab,
                              'compressible':compressible,
                              'location':location,'fixed_far':fixed_far,
                              'fixed_near':fixed_near,'height':height,
                              'llr_max_reduction':llr_max_reduction,
                              'specified_LLR_levels':specified_LLR_levels,
                              'specified_influence_area':specified_influence_area,
                              'specified_trib_area':specified_trib_area,
                              'use_specified_LLR_parameters':use_specified_LLR_parameters,
                              'point_coords':point_coords};
    #loop thru the column elements above
    for col_element in element_layer.column_elements_above:
        #get the unique id
        uid=col_element.uid;
        #get the data from slab element
        angle=rc.elements.ColumnElement(uid,model).angle;
        b=rc.elements.ColumnElement(uid,model).b;
        d=rc.elements.ColumnElement(uid,model).d;
        i_factor=rc.elements.ColumnElement(uid,model).i_factor;
        location=rc.elements.ColumnElement(uid,model).location;
        roller=rc.elements.ColumnElement(uid,model).roller;
        below_slab=rc.elements.ColumnElement(uid,model).below_slab;
        compressible=rc.elements.ColumnElement(uid,model).compressible;
        fixed_far=rc.elements.ColumnElement(uid,model).fixed_far;
        fixed_near=rc.elements.ColumnElement(uid,model).fixed_near;
        height=rc.elements.ColumnElement(uid,model).height;
        llr_max_reduction=rc.elements.ColumnElement(uid,model).llr_max_reduction;
        specified_LLR_levels=rc.elements.ColumnElement(uid,model).specified_LLR_levels;
        specified_influence_area=rc.elements.ColumnElement(uid,model).specified_influence_area;
        specified_trib_area=rc.elements.ColumnElement(uid,model).specified_trib_area;
        use_specified_LLR_parameters=rc.elements.ColumnElement(uid,model).use_specified_LLR_parameters;
        concrete_mix=col_element.concrete.name;
        number=rc.elements.ColumnElement(uid,model).number;
        name=rc.elements.ColumnElement(uid,model).name;
        point_coords=[location.x,location.y];
        #add the slab area to the dictionary
        column_elements[uid]={'uid':uid,'concrete_mix':concrete_mix,
                              'number':number,'name':name,
                              'b':b,'d':d,'i_factor':i_factor,'angle':angle,
                              'roller':roller,'below_slab':below_slab,
                              'compressible':compressible,
                              'location':location,'fixed_far':fixed_far,
                              'fixed_near':fixed_near,'height':height,
                              'llr_max_reduction':llr_max_reduction,
                              'specified_LLR_levels':specified_LLR_levels,
                              'specified_influence_area':specified_influence_area,
                              'specified_trib_area':specified_trib_area,
                              'use_specified_LLR_parameters':use_specified_LLR_parameters,
                              'point_coords':point_coords};
    return column_elements;

def get_wall_elements(model):
    """
    get the wall elements from the elements layer
    
    returns wall_elements (dict)
    """
    #get the element layer
    element_layer=model.cad_manager.element_layer;
    #initiate the wall elements dictionary
    wall_elements={};
    #loop thru the column elements below
    for wall_element in element_layer.wall_elements_below:
        #get the unique id
        uid=wall_element.uid;
        #get the data from wall element
        location=rc.elements.WallElement(uid,model).location;
        shear_wall=rc.elements.WallElement(uid,model).shear_wall;
        thickness=rc.elements.WallElement(uid,model).thickness;
        below_slab=rc.elements.WallElement(uid,model).below_slab;
        compressible=rc.elements.WallElement(uid,model).compressible;
        fixed_far=rc.elements.WallElement(uid,model).fixed_far;
        fixed_near=rc.elements.WallElement(uid,model).fixed_near;
        height=rc.elements.WallElement(uid,model).height;
        llr_max_reduction=rc.elements.WallElement(uid,model).llr_max_reduction;
        specified_LLR_levels=rc.elements.WallElement(uid,model).specified_LLR_levels;
        specified_influence_area=rc.elements.WallElement(uid,model).specified_influence_area;
        specified_trib_area=rc.elements.WallElement(uid,model).specified_trib_area;
        use_specified_LLR_parameters=rc.elements.WallElement(uid,model).use_specified_LLR_parameters;
        concrete_mix=wall_element.concrete.name;
        number=rc.elements.WallElement(uid,model).number;
        name=rc.elements.WallElement(uid,model).name;
        points=[location.start_point,location.end_point];
        point_coords=((points[0].x,points[0].y),(points[1].x,points[1].y));
        #add the wall element to the dictionary
        wall_elements[uid]={'uid':uid,'concrete_mix':concrete_mix,
                            'number':number,'name':name,
                            'shear_wall':shear_wall,'thickness':thickness,
                            'below_slab':below_slab,'compressible':compressible,
                            'location':location,'fixed_far':fixed_far,
                            'fixed_near':fixed_near,'height':height,
                            'llr_max_reduction':llr_max_reduction,
                            'specified_LLR_levels':specified_LLR_levels,
                            'specified_influence_area':specified_influence_area,
                            'specified_trib_area':specified_trib_area,
                            'use_specified_LLR_parameters':use_specified_LLR_parameters,
                            'points':points,'point_coords':point_coords};
    #loop thru the wall elements above
    for wall_element in element_layer.wall_elements_above:
        #get the unique id
        uid=wall_element.uid;
        #get the data from wall element
        location=rc.elements.WallElement(uid,model).location;
        shear_wall=rc.elements.WallElement(uid,model).shear_wall;
        thickness=rc.elements.WallElement(uid,model).thickness;
        below_slab=rc.elements.WallElement(uid,model).below_slab;
        compressible=rc.elements.WallElement(uid,model).compressible;
        fixed_far=rc.elements.WallElement(uid,model).fixed_far;
        fixed_near=rc.elements.WallElement(uid,model).fixed_near;
        height=rc.elements.WallElement(uid,model).height;
        llr_max_reduction=rc.elements.WallElement(uid,model).llr_max_reduction;
        specified_LLR_levels=rc.elements.WallElement(uid,model).specified_LLR_levels;
        specified_influence_area=rc.elements.WallElement(uid,model).specified_influence_area;
        specified_trib_area=rc.elements.WallElement(uid,model).specified_trib_area;
        use_specified_LLR_parameters=rc.elements.WallElement(uid,model).use_specified_LLR_parameters;
        concrete_mix=wall_element.concrete.name;
        number=rc.elements.WallElement(uid,model).number;
        name=rc.elements.WallElement(uid,model).name;
        points=[location.start_point,location.end_point];
        point_coords=((points[0].x,points[0].y),(points[1].x,points[1].y));
        #add the wall element to the dictionary
        wall_elements[uid]={'uid':uid,'concrete_mix':concrete_mix,
                            'number':number,'name':name,
                            'shear_wall':shear_wall,'thickness':thickness,
                            'below_slab':below_slab,'compressible':compressible,
                            'location':location,'fixed_far':fixed_far,
                            'fixed_near':fixed_near,'height':height,
                            'llr_max_reduction':llr_max_reduction,
                            'specified_LLR_levels':specified_LLR_levels,
                            'specified_influence_area':specified_influence_area,
                            'specified_trib_area':specified_trib_area,
                            'use_specified_LLR_parameters':use_specified_LLR_parameters,
                            'points':points,'point_coords':point_coords};
    return wall_elements;

def get_load_cases_and_combos(model):
    """
    get the load cases and combos from the model
    """
    #get the force loading layer
    force_loading_layer=model.cad_manager.force_loading_layers;
    #initiate the load patters holder
    load_patterns={};
    for pattern in force_loading_layer:
        uid=pattern.uid;
        number=pattern.number;
        name=pattern.name;
        #get the properties
        area_loads=pattern.area_loads;
        line_loads=pattern.line_loads;
        point_loads=pattern.point_loads;
        #
        analysis_type=pattern.analysis_type.value;
        loading_type=pattern.loading_type;
        cause=loading_type.cause.name;
        #
        load_patterns[name]={'uid':uid,'number':number,'name':name,
                             'area_loads':area_loads,'line_loads':line_loads,
                             'point_loads':point_loads,
                             'analysis_type':analysis_type,
                             'cause':cause};
    #Get the load combinations
    load_combo_layer=model.cad_manager.load_combo_layers;
    #initiate the load combos holder
    load_combos={};
    for combo in load_combo_layer:
        uid=combo.uid;
        number=combo.number;
        name=combo.name;
        analysis_type=combo.analysis_type.name;
        group_alternate_envelope_load_factor=combo.group_alternate_envelope_load_factor;
        group_loading_type=combo.group_loading_type.name;
        group_standard_load_factor=combo.group_standard_load_factor;
        summing_type=combo.summing_type.name;
        #load factor
        load_factors=combo.load_factors;
        lfs={};
        for lf in load_factors:
            loading=lf.loading;
            lf_uid=lf.uid;
            lf_number=lf.number;
            lf_name=lf.name;
            loading_name=loading.name;
            standard_load_factor=lf.standard_load_factor;
            alternate_envelope_load_factor=lf.alternate_envelope_load_factor;
            if(standard_load_factor!=0 or alternate_envelope_load_factor!=0):
                lfs[loading_name]={'standard_load_factor':standard_load_factor,
                                   'alternate_envelope_load_factor':alternate_envelope_load_factor}
        load_combos[name]={'uid':uid,'number':number,'name':name,
                           'analysis_type':analysis_type,
                           'group_alternate_envelope_load_factor':group_alternate_envelope_load_factor,
                           'group_standard_load_factor':group_standard_load_factor,
                           'summing_type':summing_type,
                           'load_factors':lfs};
    return load_patterns,load_combos;
