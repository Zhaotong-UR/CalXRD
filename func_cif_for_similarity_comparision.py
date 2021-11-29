# This script aims to load cif, seperate cif information, search and find cif information we want
# For XRD we need mainly 3 parts of information:
# 1. CELL: cell information
# 2. SYMM: symmetry operation to expand the whole cell
# 3. ATOM: atom fractional position, occupancy

def cifToInfo(cif_dir, cif_file):
    
    import numpy as np
    import os
    import re
    from IPython.display import display, clear_output
    from func_rmv_brkt import rmv_brkt

    import time
    
    # Set print options for digits
    # Set 3 decimals
    np.set_printoptions(precision=5)
    # Suppress scientific notations
    np.set_printoptions(suppress=True)
    
# FILE & DICT
# File & dictionary management
    
    # Locate and open CIF files
    cif_file_dir = "{}/{}".format(cif_dir, cif_file)
    cif_content = open(cif_file_dir)
    cif_content_lines = cif_content.readlines()
    # Open tables for scattering data
    # And create a dictionary using this file
    scat_table = open('chemical table.txt')
    scat_table_lines = scat_table.readlines()
    chem_dict = {}
    for line in scat_table_lines:
        chem_dict[line.split()[0]] = line.split()[1]
        
# VAR
# Define variables needed during extraction

    # 1. CELL: cell data
    
    cell_a = 0
    cell_b = 0
    cell_c = 0
    cell_alpha = 0
    cell_beta = 0
    cell_gamma = 0
    chem_form = ""
    # This is the "_space_group_IT_number" in CIF file
    space_group = 0
    # Once we have "space_group", this become Ture
    space_group_line_judge = False
    # This is the crystal systems, ranging 1 to 7
    crystal_sys = 0

    # 2. ATOM: atomic data
      
    # This is the line index of the start of atoms lists of a CIF file
    atom_start_line = 0 
    # This is the line index of the end of atoms lists of a CIF file
    atom_end_line = 0   
    # This is the line index of the "loop_", with ATOM info followed
    atom_loop_line = 0
    # Once we locate "_atom_label_line", this becomes False
    atom_loop_line_judge = True
    # This is the line index of the "_atom_label_line"
    atom_label_line = 0
    # This is the line index of the "_atom_site_type_symbol"
    ion_label_line = 0
    # Once we locate "_atom_site_type_symbol", this becomes True. 
    # False indicate the ion label is missing and can be followed by neutral atom scattering table
    # True indicate that ion label is identified and can be followed by ion scattering table
    ion_label_line_judge = False
    # This is the line index of the "_atom_site_fract_x"
    atom_x_line = 0
    # This is the line index of the "_atom_site_fract_y"
    atom_y_line = 0
    # This is the line index of the "_atom_site_fract_z"
    atom_z_line = 0
    # This is the line index of the "_atom_site_occupancy"
    atom_ocp_line = 0
    # Once we locate "_atom_site_occupancy", this becomes True
    atom_ocp_line_judge = False
    # Once we locate "_atom_label_line", this becomes True
    atom_start_line_judge = False
    # Once we locate "atom_start_line", this becomes True
    atom_end_line_judge = False
    # Once we locate "atom_start_line", this becomes True. If we find normal end, this becomes False.
    atom_end_blank_judge = False

    # 3. SYMM: symmetry operations
    
    # This is the line index of the start of symm. op. lists of a CIF file
    symm_start_line = 0
    # This is the line index of the start of symm. op. of a CIF file
    symm_end_line = 0
    # Once we locate "_space_group_symop_operation_xyz" or "_symmetry_equiv_pos_as_xyz", this becomes True
    symm_end_line_judge = False
    
    # For some cod file, there are comments inside ; ;
    # Which means, if line == ';', this means the start of comments, comment_judge = True
    # if again line == ';', this means the end of comments, comment_judge = False
    # Initially, comment judge = False
    comment_judge = False
    
# LOOP CIF
# Read CIF for desired variables
    
    line_count = 0
    for line in cif_content_lines:
        line_count += 1
        
        # 1. CELL
        
        if ';' == line.strip():
            if not comment_judge:
                comment_judge = True
            else:
                comment_judge = False
        elif "_database_code_ICSD" in line and not comment_judge:
            icsd_coll_code = line.split()[1]
        elif '_space_group_IT_number' in line and not comment_judge:
            if len(line.split()) == 2: 
                space_group = rmv_brkt(line.split()[1])
                space_group_line_judge = True
            else: 
                return 'Failed:_space_group_IT_number wrong format'
        elif '_cell_length_a' in line and not comment_judge: 
            if len(line.split()) == 2: 
                cell_a = rmv_brkt(line.split()[1])
            else: 
                return 'Failed: _cell_length_1 wrong format'
        elif '_cell_length_b' in line and not comment_judge: 
            if len(line.split()) == 2: 
                cell_b = rmv_brkt(line.split()[1])
            else: 
                return 'Failed: _cell_length_b wrong format'
        elif '_cell_length_c' in line and not comment_judge:
            if len(line.split()) == 2: 
                cell_c = rmv_brkt(line.split()[1])
            else: 
                return 'Failed: _cell_length_c wrong format'
        elif '_cell_angle_alpha' in line and not comment_judge:
            if len(line.split()) == 2: 
                cell_alpha = rmv_brkt(line.split()[1]) * np.pi / 180.
            else: 
                return 'Failed: _cell_length_alpha wrong format'
        elif '_cell_angle_beta' in line and not comment_judge:
            if len(line.split()) == 2: 
                cell_beta = rmv_brkt(line.split()[1]) * np.pi / 180.
            else: 
                return 'Failed: _cell_length_beta wrong format'
        elif '_cell_angle_gamma' in line and not comment_judge:
            if len(line.split()) == 2: 
                cell_gamma = rmv_brkt(line.split()[1]) * np.pi / 180.
            else: 
                return 'Failed: _cell_length_gamma wrong format'
        elif '_chemical_formula_sum' in line and not comment_judge:
            chem_form = re.split(r"['\sB]", line, 1)[1].replace("'", "").strip()
            
        # 2. ATOM
        
        elif 'loop_' in line and atom_loop_line_judge and not comment_judge:
            atom_loop_line = line_count            
        # Find the label that all CIF has: "_atom_site_label"
        elif '_atom_site_label' == line.strip() and not comment_judge:
            atom_label_line = line_count
            atom_start_line_judge = True
            atom_loop_line_judge = False
        # Find the label that indicate ionization: '_atom_site_type_symbol'
        elif '_atom_site_type_symbol' == line.strip() and not comment_judge:
            ion_label_line = line_count
            ion_label_line_judge = True
        # Find xyz fractions: "_atom_site_fract_x" & "...y" & "...z"
        elif '_atom_site_fract_x' == line.strip() and not comment_judge:
            atom_x_line = line_count
        elif '_atom_site_fract_y' == line.strip() and not comment_judge:
            atom_y_line = line_count
        elif '_atom_site_fract_z' == line.strip() and not comment_judge:
            atom_z_line = line_count
        # Find "_atom_site_occupancy"
        elif '_atom_site_occupancy' == line.strip() and not comment_judge:
            atom_ocp_line = line_count
            atom_ocp_line_judge = True
        # Find the line doesn't start with "_atom" and this line is the start of atoms' list
        elif ('_atom' not in line) and atom_start_line_judge and not comment_judge:
            atom_start_line = line_count
            atom_start_line_judge = False
            atom_end_line_judge = True
            atom_end_blank_judge = True
        # Find the line start with either "loop_" or "#End" or blank. The previous line is the end of atoms
        elif atom_end_line_judge and (('loop_' in line) or ('#End' in line)) and not comment_judge:
            atom_end_line = line_count - 1
            atom_start_line_judge = False
            atom_end_line_judge = False
            atom_end_blank_judge = False
        # Sometimes the CIF file end with nothing
        if atom_end_blank_judge and not comment_judge:
            atom_end_line = line_count
        
        # print(atom_start_line, atom_end_line)
        
        # 3. SYMM
        
        # Find "_space_group_symop_operation_xyz" or "_symmetry_equiv_pos_as_xyz"
        if '_space_group_symop_operation_xyz' in line or '_symmetry_equiv_pos_as_xyz' in line and not comment_judge:
            symm_start_line = line_count + 1
            symm_end_line_judge = True
        # Find "loop_" after symm. op.
        if 'loop_' in line.strip() and symm_end_line_judge and not comment_judge:
            symm_end_line = line_count - 1
            symm_end_line_judge = False

        # Print varaibles out
    print("0/5 Done: CIF")
        
# CAL VAR
# Calculate variables

    # 2. ATOM
    
    # If no space group information, we return Failed
    if not space_group_line_judge:
        return "Failed: Space Group(no space group id)"
    if space_group < 1 or space_group > 230:
        return "Failed: Space group(not between 1-230)"

    if atom_start_line == 0:
        return "Failed: Atom list(no start find)"
    if atom_end_line == 0:
        return "Failed: Atom list(no end find)"
    # "num_sym_atom": number of non-symmetry atoms
    num_symm_atom = 0
    num_symm_atom = atom_end_line - atom_start_line + 1
    # this is the total variable column that the atom list should have
    atom_site_count = atom_start_line - atom_loop_line - 1
    # The column number 6 is defined as "type, idx, x, y, z, ocp". May subject to change
    symm_atom_info = np.zeros((num_symm_atom, 6))
    # "count_symm_atom" is the idx for future matrix "symm_atom_info"
    for count_symm_atom, line in enumerate(cif_content_lines[atom_start_line - 1: atom_end_line]):
        if len(line.split()) < atom_site_count:
                return 'Failed: Atom list column doesnot match loop labels'
        # If CIF format is "Al1" which is element + label count
        if re.match('([A-z]+)([0-9]+)', line.split()[atom_label_line - atom_loop_line - 1]) != None:
            # "symm_atom_type": CIF format label of chemical name
            symm_atom_type = re.match('([A-z]+)([0-9]+)', line.split()[atom_label_line - atom_loop_line - 1]).group(1)
            # "sym_atom_idx": CIF format indices for non-symmetry atoms, not the final sequence of atoms
            symm_atom_idx = re.match('([A-z]+)([0-9]+)', line.split()[atom_label_line - atom_loop_line - 1]).group(2)
        # If CIF format is "Al" without index
        elif re.match('([A-z]+)([0-9]+[+-]*)', line.split()[atom_label_line - atom_loop_line - 1]) == None:
            symm_atom_type = line.split()[atom_label_line - atom_loop_line - 1]
            symm_atom_idx = "1"
        # Sometimes, CIF missing ATOM info, like this "? ? ? ?"
        if len(line.split()) < (atom_z_line - atom_loop_line):
            return "Failed: Atom list(list not complete)"
        # For this line, extract x, y, z information
        symm_atom_x = line.replace("'", "").split()[atom_x_line - atom_loop_line - 1]
        symm_atom_y = line.replace("'", "").split()[atom_y_line - atom_loop_line - 1]
        symm_atom_z = line.replace("'", "").split()[atom_z_line - atom_loop_line - 1]
        # For this line, extract occupancy information
        if atom_ocp_line_judge:
            symm_atom_ocp = line.split()[atom_ocp_line - atom_loop_line - 1]
        # If no occupancy in CIF, default to 1
        elif not atom_ocp_line_judge:
            symm_atom_ocp = "1"
        # Here generate matrix "symm_atom_info"
        # Here we search for tables for its corresbonding Z
        if chem_dict.get(symm_atom_type) != None:
            symm_atom_info[count_symm_atom, 0] = int(chem_dict.get(symm_atom_type))
            symm_atom_info[count_symm_atom, 1] = rmv_brkt(symm_atom_idx)
            symm_atom_info[count_symm_atom, 2] = rmv_brkt(symm_atom_x)
            symm_atom_info[count_symm_atom, 3] = rmv_brkt(symm_atom_y)
            symm_atom_info[count_symm_atom, 4] = rmv_brkt(symm_atom_z)
            symm_atom_info[count_symm_atom, 5] = rmv_brkt(symm_atom_ocp)
        # This error case happens when atom label is like "ALM"
        elif chem_dict.get(symm_atom_type) == None:
            return "Failed: Can not match neutrual atom type"
        # Then we update [:, 0] if ion label exists and REPLACE NEUTRAL atom index with ION index    
        if True and ion_label_line_judge and re.fullmatch('([A-z]+)([1-9]+[+-]+)', line.split()[ion_label_line - atom_loop_line - 1]) != None and chem_dict.get(line.split()[ion_label_line - atom_loop_line - 1].strip()) != None:
            symm_atom_info[count_symm_atom, 0] = int(chem_dict.get(line.split()[ion_label_line - atom_loop_line - 1].strip()))
    
    print("return cif_info")
    return cif_file, space_group, round(cell_a, 2), round(cell_b, 2), round(cell_c, 2), round(cell_alpha, 2), round(cell_beta, 2), round(cell_gamma, 2), np.unique(symm_atom_info[:, 0].T)
    
