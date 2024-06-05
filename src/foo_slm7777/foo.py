#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 19:55:58 2024

@author: slm7777

This is the generic "foo" class that may be subclassed for specific
numerical needs. 

The private attribute _prm_list allows subclasses to determine their own
number of and types of parameters. The user_data could be used to specify
user preferences for visualization, or other external tools. The private
_type_check dictionary sets users up to perform type checking on parameters.

This is heavily based on Python Scripting for Computational Science, 3rd Edition,
by H.P. Langtangen.
"""

import numpy as np
import operator

# Base class; think of foo as a generic physics model.
class foo(object):
    def __init__(self):
        self._prm_list = []  # model parameters, to be filled in by subclass
        self.user_data = None
        self._type_check = {} # defined in subclass

    def _update(self, key, val):
        setattr(self, key, val)
        
# subclass it
class sphere(foo):
    """
    This implements a class "sphere" using the foo base class to
    determine its basic parameter structure.

    One could imagine an intermediate base class, say "shape" that directly 
    subclasses "foo", and "sphere" is just one example of a "shape" subclass.
    I did not implement it that way. 

    One method you might want in a sphere object is to return its volume. Alternatively,
    one might be interested in surface area, or material properties. One could
    further extend this to actually include user data that ties into visualization
    tools.
    """
    def __init__(self, **kwargs):
        # sphere has one parameter, its radius
        foo.__init__(self)
        self.parms = {'radius': 1.0}
        self.units = {'radius': 'meters'}
        self._prm_list = [self.parms, self.units]
        self._type_check.update({'radius': (float,), 'units': True})
        self.user_data = None # modify to add user params for say, visualization
        self.set(**kwargs)
        
    
    def set(self, **kwargs):
        # Because we're trying to be generic, the set method needs to do some
        # extra work.
        for prm in kwargs:
            _set = False
            for d in self._prm_list: 
                try: 
                    if self.set_in_dict(prm, kwargs[prm], d):
                        _set = True
                        break
                except TypeError as exception:
                    print(exception)
                    break
                
            if not _set:
                if self.user_data is not None:
                    if isinstance(self.user_prm, dict):
                        self.user_prm[prm] = kwargs[prm]
                        break
                
                raise NameError('parameter "%s" not registered' % prm)
                        
            self._update(prm, kwargs[prm])
    
    def set_in_dict(self, prm, value, d):
        """ 
        Set d[prm]=valuem, but check if prm is registered in class 
        dictionaries, type is acceptable, etc.
        """
        can_set = False
        # is prm a registered key?
        if prm in d:
            if prm in self._type_check:
                
                # check for valid type
                if isinstance(self._type_check[prm], int): 
                    # check for Boolean
                    if self._type_check[prm]:
                        # type check against previous value or None
                        if isinstance(value, (type(d[prm]), None)):
                            can_set = True
                        elif operator.isNumberType(value) and\
                            operator.isNumberType(d[prm]):
                                can_set = True
                                
                elif isinstance(self._type_check[prm], (tuple,list,type)):
                    if isinstance(value, self._type_check[prm]):
                        can_set = True
                    else:
                        raise (TypeError, \
                                'parameter "%s" failed type check' % prm)
                            
                elif callable(self._type_check[prm]):
                    can_set = self.type_check[prm](value)
                    
        else:
            can_set = True
            
        if can_set:
            d[prm] = value
            return True
        
        return False
                
    def get_volume(self):
        # I would probably use pint or sympy to attach units to the values
        # so I don't have to keep track of units separately.
        return (4.0/3.0)*np.pi*self.radius**3.0, '%s**3'  % self.units   

    def short_form(self):
        # unpack the dictionary for easier usage.
        return self.parms['radius'], self.parms['units']
        
    def __str__(self):
        r, unitstr = self.short_form()
        return f'The sphere has radius {r} {unitstr}'

    def __repr__(self):
        return f'Sphere({self.parms})'
        
if __name__ == '__main__':
    s = sphere()
    s.set(radius=10., units='meters')
    print(str(s))
    Vol, unitstr = s.get_volume()
    print(f'Sphere s has volume {Vol} {unitstr}')
        
 