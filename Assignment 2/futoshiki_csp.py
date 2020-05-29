#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only 
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary 
      all-different constraints for both the row and column constraints. 

'''
from cspbase import *
import itertools

def futoshiki_csp_model_1(futo_grid):
    ##IMPLEMENT
    #Variables Initialization
    vars = [] #For CSP object
    var_array = []
    ineq_array = []
    dom = []

    row_num = len(futo_grid)
    if row_num > 0:
        col_num = len(futo_grid[0])

    #Create domain for unassigned slots
    for d in range(0, row_num):
        dom.append(d+1)

    #Get Variables and Inequalities
    for i in range(0, row_num):
        row = []
        row_ineq = []
        for j in range(0, col_num):
            #Check value at variable slots
            if j % 2 == 0:
                #If value is 0, create variable with domain of all possible values
                if futo_grid[i][j] == 0:
                    var = Variable("Variable{}{}".format(i, j//2), dom)
                #If already has a value, create a variable with the value
                else:
                    value_list = []
                    value_list.append(futo_grid[i][j])
                    var = Variable("Variable{}{}".format(i, j//2), value_list)

                #Put all variables into the one row list and all variables list (CSP)
                row.append(var)
                vars.append(var)

            else:
                row_ineq.append(futo_grid[i][j])

        #Put each row into the total variable array (list of list) and each row of inequalities into
        #total inequality array
        var_array.append(row)
        ineq_array.append(row_ineq)

    #Create constraints
    constr = []
    #Check for adjacent column constraints
    for i in range(0, len(var_array)):
        for j in range(0, len(var_array)):
            #k is the j+1 column
            for k in range(j+1, len(var_array)):
                #Check for row constraints
                #Also inequalities between adjacent slots need to be satisfied if applicable
                var_1 = var_array[i][j]
                var_2 = var_array[i][k]
                c = Constraint("Constraint(Variable{}{}, Variable{}{})".format(i, j, i, k), [var_1, var_2])
                tup_sat = []  # Constraint-satisfying tuples
                for l in itertools.product(var_1.cur_domain(), var_2.cur_domain()):
                    #Will execute if values are not the same and inequalities are satisfied
                    if check(ineq_array[i][j], (i, j), (i, k), l[0], l[1]):
                        tup_sat.append(l)
                #Add all satisfying tuples to specified constraint
                c.add_satisfying_tuples(tup_sat)
                #Add specified constraint to constraints list
                constr.append(c)

                #Get the column variables
                var_1 = var_array[j][i]
                var_2 = var_array[k][i]
                c = Constraint("Constraint(Variable{}{}, Variable{}{})".format(j, i, k, i), [var_1, var_2])
                tup_sat = []  # Constraint-satisfying tuples
                for l in itertools.product(var_1.cur_domain(), var_2.cur_domain()):
                    #Will execute if values are not the same
                    if check('.', (j, i), (k, i), l[0], l[1]):
                        tup_sat.append(l)
                #Add all satisfying tuples to specified constraint
                c.add_satisfying_tuples(tup_sat)
                #Add specified constraint to constraints list
                constr.append(c)

    #Create CSP object
    csp = CSP("Futoshiki_Solver for {} by {} Board".format(len(var_array), len(var_array)), vars)
    #Add in all constraints
    for c in constr:
        csp.add_constraint(c)

    return csp, var_array


def futoshiki_csp_model_2(futo_grid):
    #IMPLEMENT
    # Variables Initialization
    vars = []  # For CSP object
    var_array = []
    ineq_array = []
    dom = []

    row_num = len(futo_grid)
    if row_num > 0:
        col_num = len(futo_grid[0])

    # Create domain for unassigned slots
    for d in range(0, row_num):
        dom.append(d+1)

    # Get Variables and Inequalities
    for i in range(0, row_num):
        row = []
        row_ineq = []
        for j in range(0, col_num):
            # Check value at variable slots
            if j % 2 == 0:
                # If value is 0, create variable with domain of all possible values
                if futo_grid[i][j] == 0:
                    var = Variable("Variable{}{}".format(i, j // 2), dom)
                # If already has a value, create a variable with the value
                else:
                    value_list = []
                    value_list.append(futo_grid[i][j])
                    var = Variable("Variable{}{}".format(i, j // 2), value_list)

                # Put all variables into the one row list and all variables list (CSP)
                row.append(var)
                vars.append(var)

            else:
                row_ineq.append(futo_grid[i][j])

        # Put each row into the total variable array (list of list) and each row of inequalities into
        # total inequality array
        var_array.append(row)
        ineq_array.append(row_ineq)

    #Create Constraints
    constr = []
    for i in range(0, len(var_array)):
        vars_row = list(var_array[i])
        vars_col = [] #Get column variables
        vars_row_dom = [] #Get domain for all row variables
        vars_col_dom = [] #Get domain for all column variables
        for j in range(0, len(var_array)):
            vars_row_dom.append(var_array[i][j].cur_domain())
            vars_col.append(var_array[j][i])
            vars_col_dom.append(var_array[j][i].cur_domain())
            #Check inequalities between adjacent slots constraints
            if j < len(ineq_array[i]):
                var_1 = var_array[i][j]
                var_2 = var_array[i][j+1]
                #Will execute if there are inequalities between adjacent slots
                if ineq_array[i][j] != '.':
                    c = Constraint("Constraint(Variable{}{}, Variable{}{})".format(i, j, i, j+1), [var_1, var_2])
                    tup_sat = []  # Constraint-satisfying tuples
                    for l in itertools.product(var_1.cur_domain(), var_2.cur_domain()):
                        #Will execute if values are not the same and inequalities are satisfied
                        if check_ineq(ineq_array[i][j], l[0], l[1]):
                            tup_sat.append(l)
                    #Add all satisfying tuples to specified constraint
                    c.add_satisfying_tuples(tup_sat)
                    #Add specified constraint to constraints list
                    constr.append(c)

        #N-ary all-different constraints for row
        c = Constraint("Constraints(R{})".format(i), vars_row)
        tup_sat = []
        for l in itertools.product(*vars_row_dom):
            if check_nary(vars_row, l):
                tup_sat.append(l)
        # Add all satisfying tuples to specified constraint
        c.add_satisfying_tuples(tup_sat)
        # Add specified constraint to constraints list
        constr.append(c)

        #N-ary all-different constraints for column
        c = Constraint("Constraints(R{})".format(i), vars_col)
        tup_sat = []
        for l in itertools.product(*vars_col_dom):
            # Will execute if all values are not the same
            if check_nary(vars_col, l):
                tup_sat.append(l)
        # Add all satisfying tuples to specified constraint
        c.add_satisfying_tuples(tup_sat)
        # Add specified constraint to constraints list
        constr.append(c)

    #Create CSP object
    csp = CSP("Futoshiki_Solver for {} by {} Board".format(len(var_array), len(var_array)), vars)
    #Add in all constraints
    for c in constr:
        csp.add_constraint(c)

    return csp, var_array


#Checker Function for binary not-equal constraints
def check(ineq, var_1, var_2, val_1, val_2):
    #Check if value of variable 1 does not equal to value of variable 2
    result = val_1 != val_2

    #Check if variable 1 and variable 2 are adjacent slots
    if var_1[1] + 1 == var_2[1]:
        #If they are, check if the inequality between them is satisfied
        result = result and check_ineq(ineq, val_1, val_2)

    return result


#Checker for if inequalities are satisfied
def check_ineq(ineq, val_1, val_2):
    result = True
    #If inequality is not '.', check if the values satisfy the inequalities
    if ineq == '>': #For greater
        result = (val_1 > val_2)
    elif ineq == '<': #For smaller
        result = (val_1 < val_2)

    return result


#Check if all the values are different on the same row or column
def check_nary(vars, vals):
    result = True

    for i in range(len(vars)):
        for j in range(i+1, len(vars)):
            #As long as one is False at one point, the result which the function returns will be False
            result = result and (vals[i] != vals[j])

    return result
