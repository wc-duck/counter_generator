'''
   Generates a c-header that on each inclusion will increase a define with 1. 
   This can be used as an replacement for __COUNTER__ on platforms that do not
   support it or as a more deterministic counter. 

   version 1.0, march, 2014

   Copyright (C) 2014- Fredrik Kihlander

   This software is provided 'as-is', without any express or implied
   warranty.  In no event will the authors be held liable for any damages
   arising from the use of this software.

   Permission is granted to anyone to use this software for any purpose,
   including commercial applications, and to alter it and redistribute it
   freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
      claim that you wrote the original software. If you use this software
      in a product, an acknowledgment in the product documentation would be
      appreciated but is not required.
   2. Altered source versions must be plainly marked as such, and must not be
      misrepresented as being the original software.
   3. This notice may not be removed or altered from any source distribution.

   Fredrik Kihlander 
'''

import argparse

TEMPLATE = \
'''/**
 * Auto-generated header implementing a counter that increases by each include of the file.
 * 
 * This header will define the macro %%(counter_name)s to be increased for each inclusion of the file.
 * 
 * It has been generated with %%(digits)d amount of digits resulting in the counter wrapping around after
 * %%(wrap_count)d inclusions.
 * 
 * Usage:
 * 
 * #include "this_header.h"
 * int a = %%(counter_name)s; // 0
 * #include "this_header.h"
 * int b = %%(counter_name)s; // 1
 * #include "this_header.h"
 * int c = %%(counter_name)s; // 2
 * #include "this_header.h"
 * int d = %%(counter_name)s; // 3
 */
 
%(init)s

%(impl)s

%(join)s
'''

def gen_init( digits ):
    lines = []
    lines.append( 'ifndef %(counter_name)s' )
    lines.append( '  define %(counter_name)s_0 0' )
    for i in range( 1, digits + 1 ):
        lines.append( '  define %%(counter_name)s_%d' % i)
    for i in range( 1, digits + 1 ):
        lines.append( '  define %%(counter_name)s_D%d_0' % i)
    lines.append( 'endif // %(counter_name)s' )
    return lines

def gen_impl( digit, digits, counter_name ):
    lines = []
    
    for i in range( 10 ):
        if i == 0:
            lines.append( 'if !defined( %(counter_name)s_D%(digit)d_' + str(i) + ' )' )
        else:
            lines.append( 'elif !defined( %(counter_name)s_D%(digit)d_' + str(i) + ' )' )

        lines.append( '  define %(counter_name)s_D%(digit)d_' + str(i) )
        lines.append( '  undef  %(counter_name)s_%(digit)d' )
        lines.append( '  define %(counter_name)s_%(digit)d ' + str(i) )
    
    lines.append( 'else' )    
    for i in range( 1, 10 ):
        lines.append( '  undef %(counter_name)s_D%(digit)d_' + str(i) )

    lines.append( '  undef  %(counter_name)s_%(digit)d' )
    lines.append( '  define %(counter_name)s_%(digit)d 0' )    
    if digit < digits:
        lines += gen_impl( digit + 1, digits, counter_name )
    lines.append( 'endif' )
    ind_str = '' if digit == 0 else ' ' * 2
    lines = [ '%s%s' % ( ind_str, l % { 'digit' : digit, 'counter_name' : counter_name }) for l in lines ]
    return lines

def gen_join_macro( digits ):
    syms = [ 'digit%d' % i for i in range( digits + 1 ) ]
    return [ 'define %%(counter_name)s_JOIN_DIGITS_MACRO_(%s) %s' % ( ','.join( syms ), '##'.join( syms ) ),
             'define %%(counter_name)s_JOIN_DIGITS_MACRO(%s) %%(counter_name)s_JOIN_DIGITS_MACRO_(%s)' % ( ','.join( syms ), ','.join( syms ) ),
             'undef  %(counter_name)s',
             'define %%(counter_name)s %%(counter_name)s_JOIN_DIGITS_MACRO(%s)' % ( ','.join( [ '%%(counter_name)s_%d' % ( i - 1 ) for i in range( digits + 1, 0, -1 ) ] ) )]

def parse_args():
    parser = argparse.ArgumentParser( description='wc-engine material compiler' )
    parser.add_argument( '--digits',       type = int, default = 3,         help = 'number of digits in counter.' )
    parser.add_argument( '--counter_name', type = str, default = 'COUNTER', help = 'name of counter variable to have defined after inclusion of file.' )
    
    return parser.parse_args()

args = parse_args()
res = TEMPLATE % { 'init' : '\n'.join( '#%s' % l for l in gen_init( args.digits ) ),
                   'impl' : '\n'.join( '#%s' % l for l in gen_impl( 0, args.digits, args.counter_name ) ),
                   'join' : '\n'.join( '#%s' % l for l in gen_join_macro( args.digits ) ) }

print res % { 'counter_name' : args.counter_name,
              'digits'       : args.digits,
              'wrap_count'   : 10 ** ( args.digits + 1 ) }
