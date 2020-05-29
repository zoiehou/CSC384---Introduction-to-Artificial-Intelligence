#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
		 
		 
var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    # IMPLEMENT
    # Variables Initialization
    constr = []
    prune_list = []

    # Get Constraint list
    if newVar == None:
        constr = csp.get_all_cons()
    elif newVar != None:
        constr = csp.get_cons_with_var(newVar)

        # Prune all values that were not the one assigned to the newVar
        new_dom = newVar.cur_domain()
        for val in new_dom:
            if val != newVar.get_assigned_value():
                newVar.prune_value(val)
                prune_list.append((newVar, val))

    for c in constr:
        # Check constraints that have exactly one uninstantiated variable in their scope
        if c.get_n_unasgn() == 1:
            # Get all variables associated with constraint
            varis = c.get_scope()
            # Get the variable that is unassigned
            unassigned_var = c.get_unasgn_vars()[0]
            # Get its domain
            dom = unassigned_var.cur_domain()

            for val in dom:
                val_list = []
                # Assign the value to unassigned variable
                unassigned_var.assign(val)
                # Compute the list of values assigned to all variables
                for var in varis:
                    val_list.append(var.get_assigned_value())
                # Check if value assignments satisfy the constraint, if not execute following operations
                if not c.check(val_list):
                    # If value is in current domain of the unassigned variable, prune it and add to prune list
                    if unassigned_var.in_cur_domain(val):
                        unassigned_var.prune_value(val)
                        prune_list.append((unassigned_var, val))
                    # Check if there are values left in domain, if not, then reached a deadend
                    if unassigned_var.cur_domain_size == 0:
                        unassigned_var.unassign()
                        return False, prune_list
                # Unassign the value, and loop again to try new value assignment
                unassigned_var.unassign()

    return True, prune_list


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    # IMPLEMENT
    # Variables Initialization
    prune_list = []

    # Get Constraint list/GAC queue
    if not newVar:
        GAC_q = csp.get_all_cons()
    else:
        GAC_q = csp.get_cons_with_var(newVar)
        # Prune all values that were not the one assigned to the newVar
        dom = newVar.cur_domain()
        for val in dom:
            if val != newVar.get_assigned_value():
                newVar.prune_value(val)
                prune_list.append([newVar, val])
    # While GAC queue is not empty
    while len(GAC_q) != 0:
        # Get the constraint with index 0 in the GAC queue
        c = GAC_q.pop(0)
        # Get all variables associated with constraint
        varis = c.get_scope()
        for var in varis:
            # Get variable's domain
            cur_dom = var.cur_domain()
            # Check if there is a support for each value in the variable's domain, if not, prune it if it has not
            # been pruned
            for val in cur_dom:
                if not c.has_support(var, val):
                    if var.in_cur_domain(val):
                        var.prune_value(val)
                        prune_list.append([var, val])
                    # Check if there are values left in domain, if not, then reached a deadend
                    if var.cur_domain_size() == 0:
                        return False, prune_list
                    # If not deadend, then
                    else:
                        # Put all constraints associated with the variables into the GAC queue if not already in
                        for c_2 in csp.get_cons_with_var(var):
                            if c_2 not in GAC_q:
                                GAC_q.append(c_2)
    return True, prune_list


def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    # IMPLEMENT
    # Variables Initialization
    var_list = []
    var_domsize_list = []

    # Get a list of unassigned variables
    var_list = csp.get_all_unasgn_vars()

    # Get a list of variables and their current domain sizes
    for var in var_list:
        dom_size = var.cur_domain_size()
        var_domsize_list.append((var, dom_size))

    # Sort the list from smallest current domain to largest
    var_domsize_list = sorted(var_domsize_list, key=lambda x: x[1])

    # Variable with smallest current domain
    var = var_domsize_list[0][0]

    return var
	
