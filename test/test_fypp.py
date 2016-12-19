'''Unit tests for testing Fypp.'''

import unittest
import fypp

def _linenum(linenr, fname=None, flag=None):
    if fname is None:
        fname = fypp.STRING
    return fypp.linenumdir(linenr, fname, flag)

def _defvar(var, val):
    return '-D{0}={1}'.format(var, val)

def _incdir(path):
    return '-I{0}'.format(path)

def _linelen(linelen):
    return '-l{0}'.format(linelen)

def _indentation(ind):
    return '--indentation={0}'.format(ind)

def _folding(fold):
    return '-f{0}'.format(fold)

def _inifile(fname):
    return '-i{0}'.format(fname)

def _linenumbering(nummode):
    return '-N{0}'.format(nummode)

_LINENUM_FLAG = '-n'

_FIXED_FORMAT_FLAG = '--fixed-format'

_NO_FOLDING_FLAG = '-F'

_NEW_FILE = 1

_RETURN_TO_FILE = 2

# Various basic tests
#
# Each test consists of a tuple containing the test name and a tuple with the
# arguments of the get_test_output_method() routine.
#
SIMPLE_TESTS = [
    ('if_true',
     ([_defvar('TESTVAR', 1)],
      '#:if TESTVAR > 0\nTrue\n#:endif\n',
      'True\n'
     )
    ),
    ('if_false',
     ([_defvar('TESTVAR', 0)],
      '#:if TESTVAR > 0\nTrue\n#:endif\n',
      ''
     )
    ),
    ('if_else_true',
     ([_defvar('TESTVAR', 1)],
      '#:if TESTVAR > 0\nTrue\n#:else\nFalse\n#:endif\n',
      'True\n'
     )
    ),
    ('if_else_false',
     ([_defvar('TESTVAR', 0)],
      '#:if TESTVAR > 0\nTrue\n#:else\nFalse\n#:endif\n',
      'False\n'
     )
    ),
    ('if_elif_true1',
     ([_defvar('TESTVAR', 1)],
      '#:if TESTVAR == 1\nTrue1\n#:elif TESTVAR == 2\nTrue2\n#:endif\n',
      'True1\n'
     )
    ),
    ('if_elif_true2',
     ([_defvar('TESTVAR', 2)],
      '#:if TESTVAR == 1\nTrue1\n#:elif TESTVAR == 2\nTrue2\n#:endif\n',
      'True2\n'
     )
    ),
    ('if_elif_false',
     ([_defvar('TESTVAR', 0)],
      '#:if TESTVAR == 1\nTrue1\n#:elif TESTVAR == 2\nTrue2\n#:endif\n',
      ''
     )
    ),
    ('if_elif_else_true1',
     ([_defvar('TESTVAR', 1)],
      '#:if TESTVAR == 1\nTrue1\n#:elif TESTVAR == 2\nTrue2\n'
      '#:else\nFalse\n#:endif\n',
      'True1\n'
     )
    ),
    ('if_elif_else_true2',
     ([_defvar('TESTVAR', 2)],
      '#:if TESTVAR == 1\nTrue1\n#:elif TESTVAR == 2\nTrue2\n'
      '#:else\nFalse\n#:endif\n',
     'True2\n'
     )
    ),
    ('if_elif_else_false',
     ([_defvar('TESTVAR', 0)],
      '#:if TESTVAR == 1\nTrue1\n#:elif TESTVAR == 2\nTrue2\n'
      '#:else\nFalse\n#:endif\n',
     'False\n'
     )
    ),
    ('inline_if_true',
     ([_defvar('TESTVAR', 1)],
      '#{if TESTVAR > 0}#True#{endif}#Done',
      'TrueDone'
     )
    ),
    ('inline_if_false',
     ([_defvar('TESTVAR', 0)],
      '#{if TESTVAR > 0}#True#{endif}#Done',
      'Done'
     )
    ),
    ('inline_if_else_true',
     ([_defvar('TESTVAR', 1)],
      '#{if TESTVAR > 0}#True#{else}#False#{endif}#Done',
      'TrueDone'
     )
    ),
    ('inline_if_else_false',
     ([_defvar('TESTVAR', 0)],
      '#{if TESTVAR > 0}#True#{else}#False#{endif}#Done',
      'FalseDone'
     )
    ),
    ('inline_if_elif_true1',
     ([_defvar('TESTVAR', 1)],
      '#{if TESTVAR == 1}#True1#{elif TESTVAR == 2}#True2#{endif}#Done',
      'True1Done'
     )
    ),
    ('inline_if_elif_true2',
     ([_defvar('TESTVAR', 2)],
      '#{if TESTVAR == 1}#True1#{elif TESTVAR == 2}#True2#{endif}#Done',
      'True2Done'
     )
    ),
    ('inline_if_elif_false',
     ([_defvar('TESTVAR', 0)],
      '#{if TESTVAR == 1}#True1#{elif TESTVAR == 2}#True2#{endif}#Done',
      'Done'
     )
    ),
    ('inline_if_elif_else_true1',
     ([_defvar('TESTVAR', 1)],
      '#{if TESTVAR == 1}#True1#{elif TESTVAR == 2}#True2#{else}#False#{endif}#'
      'Done',
      'True1Done'
     )
    ),
    ('inline_if_elif_else_true2',
     ([_defvar('TESTVAR', 2)],
      '#{if TESTVAR == 1}#True1#{elif TESTVAR == 2}#True2#{else}#False#{endif}#'
      'Done',
      'True2Done'
     )
    ),
    ('inline_if_elif_else_false',
     ([_defvar('TESTVAR', 0)],
      '#{if TESTVAR == 1}#True1#{elif TESTVAR == 2}#True2#{else}#False#{endif}#'
      'Done',
      'FalseDone'
     )
    ),
    ('exprsub',
     ([_defvar('TESTVAR', 0)],
      '<${TESTVAR}$ x ${ 2 - 3 }$>',
      '<0 x -1>'
     )
    ),
    ('linesub_eol',
     ([_defvar('TESTVAR', 1)],
      'A\n$: TESTVAR + 1\nB\n',
      'A\n2\nB\n'
     )
    ),
    ('linesub_contlines',
     ([_defvar('TESTVAR', 1)],
      '$: TESTVAR & \n  & + 1\n',
      '2\n'
     )
    ),
    ('linesub_contlines2',
     ([_defvar('TESTVAR', 1)],
      '$: TEST& \n  &VAR & \n  & + 1\n',
      '2\n'
     )
    ),
    ('linesub_contlines_contchar1',
     ([],
      '$: \'hello&\n  world\'\n',
      'hello  world\n'
     )
    ),
    ('linesub_contlines2_contchar1',
     ([],
      '$: \'hello&\n  world&\n  !\'\n',
      'hello  world  !\n'
     )
    ),
    ('exprsub',
     ([_defvar('TESTVAR', 1)],
      'A${TESTVAR}$B${TESTVAR + 1}$C',
      'A1B2C'
     )
    ),
    ('exprsub_ignored_contlines',
     ([_defvar('TESTVAR', 1)],
      'A${TEST&\n  &VAR}$B${TESTVAR + 1}$C',
      'A${TEST&\n  &VAR}$B2C'
     )
    ),
    ('macrosubs',
     ([],
      '#:def macro(var)\nMACRO|${var}$|\n#:enddef\n${macro(1)}$',
      'MACRO|1|'
     )
    ),
    ('macrosubs_named_enddef',
     ([],
      '#:def macro(var)\nMACRO|${var}$|\n#:enddef macro\n${macro(1)}$',
      'MACRO|1|'
     )
    ),
    ('macro_noargs',
     ([],
      '#:def macro()\nMACRO\n#:enddef\n${macro()}$',
      'MACRO'
     )
    ),
    ('recursive_macrosubs',
     ([],
      '#:def macro(var)\nMACRO|${var}$|\n#:enddef\n${macro(macro(1))}$',
      'MACRO|MACRO|1||'
     )
    ),
    ('macrosubs_extvarsubs',
     ([_defvar('TESTVAR', 1)],
      '#:def macro(var)\nMACRO|${var}$-${TESTVAR}$|\n#:enddef\n${macro(2)}$',
      'MACRO|2-1|'
     )
    ),
    ('macrosubs_extvar_override',
     ([_defvar('TESTVAR', 1)],
      '#:def macro(var)\nMACRO|${var}$-${TESTVAR}$|\n#:enddef\n'
      '${macro(2, TESTVAR=4)}$',
      'MACRO|2-4|'
     )
    ),
    ('inline_macrodef',
     ([],
      '#{def f(x)}#${x}$^2#{enddef}#\n$: f(20)\nDone\n',
      '\n20^2\nDone\n'
     )
    ),
    ('inline_macrodef_named_enddef',
     ([],
      '#{def f(x)}#${x}$^2#{enddef f}#\n$: f(20)\nDone\n',
      '\n20^2\nDone\n'
     )
    ),
    ('macro_trailing_newlines',
     ([],
      '#:def macro()\nL1\n\n#:enddef\n$: macro()\n',
      'L1\n\n',
     )
    ),
    ('macro_trailing_newlines_inline',
     ([],
      '#:def macro()\nL1\n\n#:enddef\n|${macro()}$|',
      '|L1\n|',
     )
    ),
    ('for',
     ([],
      '#:for i in (1, 2, 3)\n${i}$\n#:endfor\n',
      '1\n2\n3\n'
     )
    ),
    ('for_macro',
     ([],
      '#:def mymacro(val)\nVAL:${val}$\n#:enddef\n'
      '#:for i in (1, 2, 3)\n$: mymacro(i)\n#:endfor\n',
      'VAL:1\nVAL:2\nVAL:3\n'
     )
    ),
    ('inline_for',
     ([],
      '#{for i in (1, 2, 3)}#${i}$#{endfor}#Done\n',
      '123Done\n'
     )
    ),
    ('inline_for_macro',
     ([],
      '#:def mymacro(val)\nVAL:${val}$\n#:enddef\n'
      '#{for i in (1, 2, 3)}#${mymacro(i)}$#{endfor}#Done\n',
      'VAL:1VAL:2VAL:3Done\n'
     )
    ),
    ('call_directive',
     ([],
      '#:def mymacro(val)\n|${val}$|\n#:enddef\n'\
      '#:call mymacro\nL1\nL2\nL3\n#:endcall\n',
      '|L1\nL2\nL3|\n',
     )
    ),
    ('call_directive_named_endcall',
     ([],
      '#:def mymacro(val)\n|${val}$|\n#:enddef\n'\
      '#:call mymacro\nL1\nL2\nL3\n#:endcall mymacro\n',
      '|L1\nL2\nL3|\n',
     )
    ),
    ('inine_call_directive_named_endcall',
     ([],
      '#:def mymacro(val)\n|${val}$|\n#:enddef\n'\
      '#{call mymacro}#L1 L2 L3#{endcall mymacro}#',
      '|L1 L2 L3|',
     )
    ),
    ('call_directive_quotation',
     ([],
      '#:def mymacro(val)\n|${val}$|\n#:enddef\n'\
      '#:call mymacro\n"""L1"""\nL2\nL3\n#:endcall\n',
      '|"""L1"""\nL2\nL3|\n',
     )
    ),
    ('call_directive_backslash_escape1',
     ([],
      '#:def mymacro(val)\n|${val}$|\n#:enddef\n'\
      '#:call mymacro\nL1\\n\nL2\nL3\n#:endcall\n',
      '|L1\\n\nL2\nL3|\n',
     )
    ),
    ('call_directive_backslash_escape2',
     ([],
      '#:def mymacro(val)\n|${val}$|\n#:enddef\n'\
      '#:call mymacro\nL1\\"a\\"\\n\nL2\nL3\n#:endcall\n',
      '|L1\\"a\\"\\n\nL2\nL3|\n',
     )
    ),
    ('call_directive_2_args',
     ([],
      '#:def mymacro(val1, val2)\n|${val1}$|${val2}$|\n#:enddef\n'\
      '#:call mymacro\n"""L1"""\nL2\n#:nextarg\nL3\n#:endcall\n',
      '|"""L1"""\nL2|L3|\n',
     )
    ),
    ('call_directive_2_args_inline',
     ([],
      '#:def mymacro(val1, val2)\n|${val1}$|${val2}$|\n#:enddef\n'\
      '#{call mymacro}#A1#{nextarg}#A2#{endcall}#',
      '|A1|A2|',
     )
    ),
    ('call_lambda_func',
     ([],
      '#:set convert = lambda s: s.lower()\n'\
      '#:call convert\nHELLO\n#:endcall\n',
      'hello\n',
     )
    ),
    ('call_generator',
     ([_inifile('include/caseconv.py')],
      '#:call caseconv("l")\nHELLO\n#:endcall\n',
      'hello\n',
     )
    ),
    ('call_generator_named_endcall',
     ([_inifile('include/caseconv.py')],
      '#:call caseconv("l")\nHELLO\n#:endcall caseconv\n',
      'hello\n',
     )
    ),
    ('call_generator_inline',
     ([_inifile('include/caseconv.py')],
      '#{call caseconv("l")}#HELLO#{endcall}#',
      'hello',
     )
    ),
    ('call_generator_inline_named_endcall',
     ([_inifile('include/caseconv.py')],
      '#{call caseconv("l")}#HELLO#{endcall caseconv}#',
      'hello',
     )
    ),
    ('direct_call',
     ([],
      '#:def mymacro(val)\n|${val}$|\n#:enddef\n'\
      '@:mymacro a < b\n',
      '|a < b|\n',
     )
    ),
    ('direct_call2',
     ([],
      '#:def mymacro(val)\n|${val}$|\n#:enddef\n'\
      '@:mymacro a < b\n',
      '|a < b|\n',
     )
    ),
    ('direct_call_contline',
     ([],
      '#:def mymacro(val)\n|${val}$|\n#:enddef\n'\
      '@:mymacro a &\n    &< b&\n    &\n',
      '|a < b|\n',
     )
    ),
    ('direct_call_quotation',
     ([],
      '#:def mymacro(val)\n|${val}$|\n#:enddef\n'\
      '@:mymacro """L1"""\n',
      '|"""L1"""|\n',
     )
    ),
    ('direct_call_escape1',
     ([],
      '#:def mymacro(val)\n|${val}$|\n#:enddef\n'\
      '@:mymacro L1\\n\n',
      '|L1\\n|\n',
     )
    ),
    ('direct_call_backslash_escape2',
     ([],
      '#:def mymacro(val)\n|${val}$|\n#:enddef\n'\
      '@:mymacro L1\\"a\\"\\n\n',
      '|L1\\"a\\"\\n|\n',
     )
    ),
    ('direct_call_2_args',
     ([],
      '#:def mymacro(val1, val2)\n|${val1}$|${val2}$|\n#:enddef\n'\
      '@:mymacro """L1""" @@ L2\n',
      '|"""L1"""|L2|\n',
     )
    ),
    ('direct_call_2_args_escape',
     ([],
      '#:def mymacro(val1, val2)\n|${val1}$|${val2}$|\n#:enddef\n'\
      '@:mymacro """L1""" @\\@ L2 @@ L3\n',
      '|"""L1""" @@ L2|L3|\n',
     )
    ),
    ('direct_call_varsubs',
     ([],
      '#:def mymacro(val1)\n|${val1}$|\n#:enddef\n'\
      '@:mymacro 2x2=${2*2}$\n',
      '|2x2=4|\n',
     )
    ),
    ('direct_call_if',
     ([],
      '#:def mymacro(val1)\n|${val1}$|\n#:enddef\n'\
      '@:mymacro 2x2=#{if False}#${2*1}$#{else}#${2*2}$#{endif}#\n',
      '|2x2=4|\n',
     )
    ),
    ('direct_call_varsubs_2_args',
     ([],
      '#:def mymacro(val1, val2)\n|${val1}$|${val2}$|\n#:enddef\n'\
      '@:mymacro ${2*1}$ @@ ${2*2}$\n',
      '|2|4|\n',
     )
    ),
    ('direct_call_varsubs_2_args_escape',
     ([],
      '#:def mymacro(val1, val2)\n|${val1}$|${val2}$|\n#:enddef\n'\
      '@:mymacro ${2*1}$ @\\@ ${2*2}$ @@ ${2*3}$\n',
      '|2 @@ 4|6|\n',
     )
    ),
    ('comment_single',
     ([],
      ' #! Comment here\nDone\n',
      'Done\n',
     )
    ),
    ('comment_multiple',
     ([],
      ' #! Comment1\n#! Comment2\nDone\n',
      'Done\n',
     )
    ),
    ('set',
     ([],
      '#:set x = 2\n$: x\n',
      '2\n',
     )
    ),
    ('set_equal_sign_nospace',
     ([],
      '#:set x=2\n$: x\n',
      '2\n',
     )
    ),
    ('set_equal_sign_withspace',
     ([],
      '#:set x = 2\n$: x\n',
      '2\n',
     )
    ),
    ('set_setvar',
     ([],
      '#:setvar x 2\n$: x\n',
      '2\n',
     )
    ),
    ('inline_set_equal_withspace',
     ([],
      '#{set x = 2}#${x}$Done\n',
      '2Done\n',
     )
    ),
    ('inline_set_equal_nospace',
     ([],
      '#{set x=2}#${x}$Done\n',
      '2Done\n',
     )
    ),
    ('inline_setvar',
     ([],
      '#{setvar x 2}#${x}$Done\n',
      '2Done\n',
     )
    ),
    ('set_function',
     ([],
      '$:setvar("x", 2)\n${x}$\nDone\n',
      "\n2\nDone\n",
     )
    ),
    ('set_function_tuple',
     ([],
      '$:setvar("x, y", (2, 3))\n${x}$${y}$\nDone\n',
      "\n23\nDone\n",
     )
    ),
    ('set_function_tuple2',
     ([],
      '$:setvar("(x, y)", (2, 3))\n${x}$${y}$\nDone\n',
      "\n23\nDone\n",
     )
    ),
    ('getvar_existing_value',
     ([_defvar('VAR', '\"VAL\"')],
      '$:getvar("VAR", "DEFAULT")\n',
      'VAL\n',
     )
    ),
    ('getvar_default_value',
     ([],
      '$:getvar("VAR", "DEFAULT")\n',
      'DEFAULT\n',
     )
    ),
    ('mute',
     ([],
      'A\n#:mute\nB\n#:set VAR = 2\n#:endmute\nVAR=${VAR}$\n',
      'A\nVAR=2\n'
     )
    ),
    ('builtin_var_line',
     ([],
      '${_LINE_}$',
      '1'
     )
    ),
    ('builtin_var_file',
     ([],
      '${_FILE_}$',
      fypp.STRING
     )
    ),
    ('builtin_var_line_in_lineeval',
     ([],
      '$:_LINE_\n',
      '1\n'
     )
    ),
    ('escaped_control_inline',
     ([],
      r'A#\{if False}\#B#\{endif}\#',
      'A#{if False}#B#{endif}#'
     )
    ),
    ('escaped_control_line',
     ([],
      '#\\:if False\n',
      '#:if False\n'
     )
    ),
    ('escaped_eval_inline',
     ([],
      r'A$\{1 + 1}\$',
      'A${1 + 1}$'
     )
    ),
    ('escaped_eval_line',
     ([],
      '$\\: 1 + 1\n',
      '$: 1 + 1\n'
     )
    ),
    ('multi_escape',
     ([],
      r'$\\\{1 + 1}\\$',
      r'$\\{1 + 1}\$'
     )
    ),
    ('escape_direct_call',
     ([],
      '@\\:assertTrue x > y\n',
      '@:assertTrue x > y\n'
     )
    ),
    ('fold_lines',
     ([_linelen(10), _indentation(2), _folding('simple')],
      'This line is not folded\nThis line ${1 + 1}$ is folded\n',
      'This line is not folded\nThis line&\n  & 2 is &\n  &folded\n'
     )
    ),
    ('prevent_comment_folding',
     ([_linelen(10), _indentation(2), _folding('simple')],
      '#:def macro()\n ! Should be not folded\nShould be folded\n#:enddef\n'
      '$:macro()\n',
      ' ! Should be not folded\nShould be&\n  & folded\n'
     )
    ),
    ('no_folding',
     ([_linelen(15), _indentation(4), _NO_FOLDING_FLAG],
      '  ${3}$456 89 123456 8',
      '  3456 89 123456 8',
     )
    ),
    ('brute_folding',
     ([_linelen(15), _indentation(4), _folding('brute')],
      '  ${3}$456 89 123456 8',
      '  3456 89 1234&\n    &56 8',
     )
    ),
    ('simple_folding',
     ([_linelen(15), _indentation(4), _folding('simple')],
      '  ${3}$456 89 123456 8',
      '  3456 89 1234&\n      &56 8',
     )
    ),
    ('smart_folding',
     ([_linelen(15), _indentation(4), _folding('smart')],
      '  ${3}$456 89 123456 8',
      '  3456 89&\n      & 123456&\n      & 8',
     )
    ),
    ('fixed_format_folding',
     ([_FIXED_FORMAT_FLAG],
      '      print *, ${\'aa\'}$, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, '
      'mm, nn, oo, pp, qq, rr, ss, tt\n',
      '      print *, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, '
      'o\n     &o, pp, qq, rr, ss, tt\n',
     )
    ),
    ('tuple_assignment',
     ([],
      '#:set mytuple = (1, 2, 3)\n#:set a, b, c = mytuple\n${a}$${b}$${c}$\n',
      '123\n'
     )
    ),
   ('tuple_assignment2',
     ([],
      '#:set a, b, c = (1, 2, 3)\n${a}$${b}$${c}$\n',
      '123\n'
     )
    ),
   ('tuple_assignment3',
     ([],
      '#:set a, b, c = 1, 2, 3\n${a}$${b}$${c}$\n',
      '123\n'
     )
    ),
   ('tuple_assignment_nospace',
     ([],
      '#:set a,b,c = (1, 2, 3)\n${a}$${b}$${c}$\n',
      '123\n'
     )
    ),
   ('tuple_assignment_vartuple',
     ([],
      '#:set (a, b, c) = (1, 2, 3)\n${a}$${b}$${c}$\n',
      '123\n'
     )
    ),
   ('tuple_assignment_vartuple2',
     ([],
      '#:set ( a, b, c ) = (1, 2, 3)\n${a}$${b}$${c}$\n',
      '123\n'
     )
    ),
   ('inline_tuple_assignment',
     ([],
      '#{set a, b, c = 1, 2, 3}#${a}$${b}$${c}$\n',
      '123\n'
     )
    ),
   ('inline_tuple_assignment_vartuple',
     ([],
      '#{set (a, b, c) = 1, 2, 3}#${a}$${b}$${c}$\n',
      '123\n'
     )
    ),
   ('whitespace_but_no_param',
     ([],
      '#:if True\nOK\n#:endif \n',
      'OK\n'
     )
    ),
   ('whitespace_but_no_param2',
     ([],
      '#:if True\nOK\n#:endif \n \n',
      'OK\n \n'
     )
    ),
   ('whitespace_but_no_param_inline',
     ([],
      '#{if True}#OK#{endif }#',
      'OK'
     )
    ),
   ('for_loop_scope',
     ([],
      '#{for i in range(4)}##{set X = i}##{endfor}#${X}$${i}$\n',
      '33\n'
     )
    ),

]


# Tests with line enumerations
#
# Each test consists of a tuple containing the test name and a tuple with the
# arguments of the get_test_output_method() routine.
#
LINENUM_TESTS = [
    # This test (but only this) must be changed, if linenum directive changes.
    ('explicit_str_linenum_test',
     ([_LINENUM_FLAG],
      '',
      '# 1 "<string>" 1\n',
     )
    ),
    ('trivial',
     ([_LINENUM_FLAG],
      'Test\n',
      _linenum(0, flag=_NEW_FILE) + 'Test\n'
     )
    ),
    ('if_true',
     ([_LINENUM_FLAG],
      '#:if 1 < 2\nTrue\n#:endif\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(1) + 'True\n' + _linenum(3)
      + 'Done\n'
     )
    ),
    ('if_false',
     ([_LINENUM_FLAG],
      '#:if 1 > 2\nTrue\n#:endif\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(3) + 'Done\n'
     )
    ),
    ('if_else_true',
     ([_LINENUM_FLAG],
      '#:if 1 < 2\nTrue\n#:else\nFalse\n#:endif\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(1) + 'True\n' + _linenum(5)
      + 'Done\n'
     )
    ),
    ('if_else_false',
     ([_LINENUM_FLAG],
      '#:if 1 > 2\nTrue\n#:else\nFalse\n#:endif\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(3) + 'False\n' + _linenum(5)
      + 'Done\n'
     )
    ),
    ('if_elif_true1',
     ([_LINENUM_FLAG],
      '#:if 1 == 1\nTrue1\n#:elif 1 == 2\nTrue2\n#:endif\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(1) + 'True1\n' + _linenum(5)
      + 'Done\n'
     )
    ),
    ('if_elif_true2',
     ([_LINENUM_FLAG],
      '#:if 2 == 1\nTrue1\n#:elif 2 == 2\nTrue2\n#:endif\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(3) + 'True2\n' + _linenum(5)
      + 'Done\n'
     )
    ),
    ('if_elif_false',
     ([_LINENUM_FLAG],
      '#:if 0 == 1\nTrue1\n#:elif 0 == 2\nTrue2\n#:endif\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(5) + 'Done\n'
     )
    ),
    ('if_elif_else_true1',
     ([_LINENUM_FLAG],
      '#:if 1 == 1\nTrue1\n#:elif 1 == 2\nTrue2\n'
      '#:else\nFalse\n#:endif\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(1) + 'True1\n' + _linenum(7)
      + 'Done\n'
     )
    ),
    ('if_elif_else_true2',
     ([_LINENUM_FLAG],
      '#:if 2 == 1\nTrue1\n#:elif 2 == 2\nTrue2\n'
      '#:else\nFalse\n#:endif\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(3) + 'True2\n' + _linenum(7)
      + 'Done\n'
     )
    ),
    ('if_elif_else_false',
     ([_LINENUM_FLAG],
      '#:if 0 == 1\nTrue1\n#:elif 0 == 2\nTrue2\n'
      '#:else\nFalse\n#:endif\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(5) + 'False\n' + _linenum(7)
      + 'Done\n'
     )
    ),
    ('inline_if_true',
     ([_LINENUM_FLAG],
      '#{if 1 < 2}#True#{endif}#Done\n',
      _linenum(0, flag=_NEW_FILE) + 'TrueDone\n'
     )
    ),
    ('inline_if_false',
     ([_LINENUM_FLAG],
      '#{if 1 > 2}#True#{endif}#Done\n',
      _linenum(0, flag=_NEW_FILE) + 'Done\n'
     )
    ),
    ('inline_if_else_true',
     ([_LINENUM_FLAG],
      '#{if 1 < 2}#True#{else}#False#{endif}#Done\n',
      _linenum(0, flag=_NEW_FILE) + 'TrueDone\n'
     )
    ),
    ('inline_if_else_false',
     ([_LINENUM_FLAG],
      '#{if 1 > 2}#True#{else}#False#{endif}#Done\n',
      _linenum(0, flag=_NEW_FILE) + 'FalseDone\n'
     )
    ),
    ('inline_if_elif_true1',
     ([_LINENUM_FLAG],
      '#{if 1 == 1}#True1#{elif 1 == 2}#True2#{endif}#Done\n',
      _linenum(0, flag=_NEW_FILE) + 'True1Done\n'
     )
    ),
    ('inline_if_elif_true2',
     ([_LINENUM_FLAG],
      '#{if 2 == 1}#True1#{elif 2 == 2}#True2#{endif}#Done\n',
      _linenum(0, flag=_NEW_FILE) + 'True2Done\n'
     )
    ),
    ('inline_if_elif_false',
     ([_LINENUM_FLAG],
      '#{if 0 == 1}#True1#{elif 0 == 2}#True2#{endif}#Done\n',
      _linenum(0, flag=_NEW_FILE) + 'Done\n'
     )
    ),
    ('inline_if_elif_else_true1',
     ([_LINENUM_FLAG],
      '#{if 1 == 1}#True1#{elif 1 == 2}#True2#{else}#False#{endif}#Done\n',
      _linenum(0, flag=_NEW_FILE) + 'True1Done\n'
     )
    ),
    ('inline_if_elif_else_true2',
     ([_LINENUM_FLAG],
      '#{if 2 == 1}#True1#{elif 2 == 2}#True2#{else}#False#{endif}#Done\n',
      _linenum(0, flag=_NEW_FILE) + 'True2Done\n'
     )
    ),
    ('inline_if_elif_else_false',
     ([_LINENUM_FLAG],
      '#{if 0 == 1}#True1#{elif 0 == 2}#True2#{else}#False#{endif}#Done\n',
      _linenum(0, flag=_NEW_FILE) + 'FalseDone\n'
     )
    ),
    ('linesub_oneline',
     ([_LINENUM_FLAG],
      'A\n$: 1 + 1\nB\n',
      _linenum(0, flag=_NEW_FILE) + 'A\n2\nB\n'
     )
    ),
    ('linesub_contlines',
     ([_LINENUM_FLAG, _defvar('TESTVAR', 1)],
      '$: TESTVAR & \n  & + 1\nDone\n',
      _linenum(0, flag=_NEW_FILE) + '2\n' + _linenum(2) + 'Done\n'
     )
    ),
    ('linesub_contlines2',
     ([_LINENUM_FLAG, _defvar('TESTVAR', 1)],
      '$: TEST& \n  &VAR & \n  & + 1\nDone\n',
      _linenum(0, flag=_NEW_FILE) + '2\n' + _linenum(3) + 'Done\n'
     )
    ),
    ('exprsub_single_line',
     ([_LINENUM_FLAG, _defvar('TESTVAR', 1)],
      'A${TESTVAR}$B${TESTVAR + 1}$C',
      _linenum(0, flag=_NEW_FILE) + 'A1B2C'
     )
    ),
    ('exprsub_multi_line',
     ([_LINENUM_FLAG],
      '${"line1\\nline2"}$\nDone\n',
      _linenum(0, flag=_NEW_FILE) + 'line1\n' + _linenum(0) + 'line2\nDone\n'
     )
    ),
    ('macrosubs',
     ([_LINENUM_FLAG],
      '#:def macro(var)\nMACRO|${var}$|\n#:enddef\n${macro(1)}$',
      _linenum(0, flag=_NEW_FILE) + _linenum(3) + 'MACRO|1|'
     )
    ),
    ('recursive_macrosubs',
     ([_LINENUM_FLAG],
      '#:def macro(var)\nMACRO|${var}$|\n#:enddef\n${macro(macro(1))}$',
      _linenum(0, flag=_NEW_FILE) + _linenum(3) + 'MACRO|MACRO|1||'
     )
    ),
    ('macrosubs_multiline',
     ([_LINENUM_FLAG],
      '#:def macro(c)\nMACRO1|${c}$|\nMACRO2|${c}$|\n#:enddef\n${macro(\'A\')}$'
      '\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(4) + 'MACRO1|A|\n' + _linenum(4)
      + 'MACRO2|A|\n'
     )
    ),
    ('recursive_macrosubs_multiline',
     ([_LINENUM_FLAG],
      '#:def f(c)\nLINE1|${c}$|\nLINE2|${c}$|\n#:enddef\n$: f(f("A"))\n',
      (_linenum(0, flag=_NEW_FILE) + _linenum(4) + 'LINE1|LINE1|A|\n' +
       _linenum(4) + 'LINE2|A||\n' + _linenum(4) + 'LINE2|LINE1|A|\n' +
       _linenum(4) + 'LINE2|A||\n')
     )
    ),
    ('multiline_macrocall',
     ([_LINENUM_FLAG],
      '#:def macro(c)\nMACRO|${c}$|\n#:enddef\n$: mac& \n  &ro(\'A\')\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(3) + 'MACRO|A|\n' + _linenum(5)
      + 'Done\n'
     )
    ),
    ('call_directive_2_args',
     ([_LINENUM_FLAG],
      '#:def mymacro(val1, val2)\n|${val1}$|${val2}$|\n#:enddef\n'\
      '#:call mymacro\nL1\nL2\n#:nextarg\nL3\n#:endcall\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(3) + '|L1\n' + _linenum(3)
      + 'L2|L3|\n' + _linenum(9),
     )
    ),
    ('for',
     ([_LINENUM_FLAG],
      '#:for i in (1, 2)\n${i}$\n#:endfor\nDone\n',
      (_linenum(0, flag=_NEW_FILE) + _linenum(1) + '1\n' + _linenum(1) + '2\n'
       + _linenum(3) + 'Done\n')
     )
    ),
    ('inline_for',
     ([_LINENUM_FLAG],
      '#{for i in (1, 2)}#${i}$#{endfor}#Done\n',
      _linenum(0, flag=_NEW_FILE) + '12Done\n'
     )
    ),
    ('set',
     ([_LINENUM_FLAG],
      '#:set x = 2\n$: x\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(1) + '2\n',
     )
    ),
    ('inline_set',
     ([_LINENUM_FLAG],
      '#{set x = 2}#${x}$Done\n',
      _linenum(0, flag=_NEW_FILE) + '2Done\n',
     )
    ),
    ('comment_single',
     ([_LINENUM_FLAG],
      ' #! Comment here\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(1) + 'Done\n'
     )
    ),
    ('comment_multiple',
     ([_LINENUM_FLAG],
      ' #! Comment1\n#! Comment2\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(2) + 'Done\n',
     )
    ),
    ('mute',
     ([_LINENUM_FLAG],
      'A\n#:mute\nB\n#:set VAR = 2\n#:endmute\nVAR=${VAR}$\n',
      _linenum(0, flag=_NEW_FILE) + 'A\n' + _linenum(5) + 'VAR=2\n'
     )
    ),
    ('direct_call',
     ([_LINENUM_FLAG],
      '#:def mymacro(val)\n|${val}$|\n#:enddef\n'\
      '@:mymacro a < b\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(3) + '|a < b|\n',
     )
    ),
    ('direct_call_contline',
     ([_LINENUM_FLAG],
      '#:def mymacro(val)\n|${val}$|\n#:enddef\n'\
      '@:mymacro a &\n    &< b&\n    &\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(3) + '|a < b|\n' + _linenum(6)
      + 'Done\n',
     )
    ),
    ('assert_directive',
     ([_LINENUM_FLAG],
      '#:assert 1 < 2\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(1) + 'Done\n',
     )
    ),
    ('assert_directive_contline',
     ([_LINENUM_FLAG],
      '#:assert 1&\n& < 2\nDone\n',
      _linenum(0, flag=_NEW_FILE) + _linenum(2) + 'Done\n',
     )
    ),
    ('smart_folding',
     ([_LINENUM_FLAG, _linelen(15), _indentation(4), _folding('smart')],
      '  ${3}$456 89 123456 8\nDone\n',
      _linenum(0, flag=_NEW_FILE) + '  3456 89&\n' + _linenum(0)
      + '      & 123456&\n' + _linenum(0) + '      & 8\n' + 'Done\n'
     )
    ),
    ('smart_folding_nocontlines',
     ([_LINENUM_FLAG, _linenumbering('nocontlines'), _linelen(15),
       _indentation(4), _folding('smart')],
      '  ${3}$456 89 123456 8\nDone\n',
      _linenum(0, flag=_NEW_FILE) + '  3456 89&\n' + '      & 123456&\n' \
      + '      & 8\n' + _linenum(1) + 'Done\n'
     )
    ),
]


# Tests with include files
#
# Each test consists of a tuple containing the test name and a tuple with the
# arguments of the get_test_output_method() routine.
#
INCLUDE_TESTS = [
    ('explicit_include',
     ([],
      '#:include "include/fypp1.inc"\n',
      'INCL1\nINCL5\n'
     )
    ),
    ('search_include',
     ([_incdir('include')],
      '#:include "fypp1.inc"\n',
      'INCL1\nINCL5\n'
     )
    ),
    ('nested_include_in_incpath',
     ([_incdir('include')],
      '#:include "subfolder/include_fypp1.inc"\n',
      'INCL1\nINCL5\n'
     )
    ),
    ('nested_include_in_folder_of_incfile',
     ([_incdir('include')],
      '#:include "subfolder/include_fypp2.inc"\n',
      'FYPP2\n'
     )
    ),
    ('search_include_linenum',
     ([_LINENUM_FLAG, _incdir('include')],
      '#:include "fypp1.inc"\n$: incmacro(1)\n',
      (_linenum(0, flag=_NEW_FILE)
       + _linenum(0, 'include/fypp1.inc', flag=_NEW_FILE)
       + 'INCL1\n' + _linenum(4, 'include/fypp1.inc')
       + 'INCL5\n' + _linenum(1, flag=_RETURN_TO_FILE) + 'INCMACRO(1)\n')
     )
    ),
    ('nested_include_in_incpath_linenum',
     ([_LINENUM_FLAG, _incdir('include')],
      '#:include "subfolder/include_fypp1.inc"\n',
      (_linenum(0, flag=_NEW_FILE)
       + _linenum(0, 'include/subfolder/include_fypp1.inc', flag=_NEW_FILE)
       + _linenum(0, 'include/fypp1.inc', flag=_NEW_FILE) + 'INCL1\n'
       + _linenum(4, 'include/fypp1.inc') + 'INCL5\n'
       + _linenum(1, 'include/subfolder/include_fypp1.inc',
                  flag=_RETURN_TO_FILE)
       + _linenum(1, flag=_RETURN_TO_FILE))
     )
    ),
    ('nested_include_in_folder_of_incfile',
     ([_LINENUM_FLAG, _incdir('include')],
      '#:include "subfolder/include_fypp2.inc"\n',
      (_linenum(0, flag=_NEW_FILE)
       + _linenum(0, 'include/subfolder/include_fypp2.inc', flag=_NEW_FILE)
       + _linenum(0, 'include/subfolder/fypp2.inc', flag=_NEW_FILE)
       + 'FYPP2\n'
       + _linenum(1, 'include/subfolder/include_fypp2.inc',
                  flag=_RETURN_TO_FILE)
       + _linenum(1, flag=_RETURN_TO_FILE))
     )
    ),
    ('muted_include',
     ([_incdir('include')],
      'START\n#:mute\n#:include \'fypp1.inc\'\n#:endmute\nDONE\n',
      'START\nDONE\n'
     )
    ),
    ('muted_include_linenum',
     ([_LINENUM_FLAG, _incdir('include')],
      'START\n#:mute\n#:include \'fypp1.inc\'\n#:endmute\nDONE\n',
      _linenum(0, flag=_NEW_FILE) + 'START\n' + _linenum(4) + 'DONE\n'
     )
    ),
]


# Tests triggering exceptions
#
# Each test consists of a tuple containing the test name and a tuple with the
# arguments of the get_test_exception_method() routine.
#
EXCEPTION_TESTS = [
    #
    # Parser errors
    #
    ('invalid_directive',
     ([],
      '#:invalid\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('invalid_macrodef',
     ([],
      '#:def alma[x]\n#:enddef\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('invalid_for_decl',
     ([],
      '#:for i = 1, 2\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('invalid_include',
     ([],
      '#:include <test.h>\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('inline_include',
     ([],
      '#{include "test.h"}#\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 0))]
     )
    ),
    ('wrong_include_file',
     ([],
      '#:include "testfkjsdlfkjslf.h"\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('invalid_else',
     ([],
      '#:if 1 > 2\nA\n#:else True\nB\n#:endif\n',
      [(fypp.FyppFatalError, fypp.STRING, (2, 3))]
     )
    ),
    ('invalid_endif',
     ([],
      '#:if 1 > 2\nA\n#:else\nB\n#:endif INV\n',
      [(fypp.FyppFatalError, fypp.STRING, (4, 5))]
     )
    ),
    ('invalid_endfor',
     ([],
      '#:for i in range(5)\n${i}$\n#:endfor INV\n',
      [(fypp.FyppFatalError, fypp.STRING, (2, 3))]
     )
    ),
    ('invalid_variable_assign',
     ([],
      '#:set A=\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('invalid_mute',
     ([],
      '#:mute TEST\n#:endmute\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('invalid_endmute',
     ([],
      '#:mute\n#:endmute INVALID\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 2))]
     )
    ),
    ('inline_mute',
     ([],
      '#{mute}#test#{endmute}#\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 0))]
     )
    ),
    ('inline_endmute',
     ([],
      '#:mute\ntest#{endmute}#\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 1))]
     )
    ),
    ('setvar_with_equal',
     ([],
      '#:setvar x = 2\n$: x\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('inline_set_without_equal',
     ([],
      '#{set x 2}#${x}$Done\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 0))]
     )
    ),
    #
    # Builder errors
    #
    ('line_if_inline_endif',
     ([],
      '#:if 1 < 2\nTrue\n#{endif}#\n',
      [(fypp.FyppFatalError, fypp.STRING, (2, 2))]
     )
    ),
    ('inline_if_line_endif',
     ([],
      '#{if 1 < 2}#True\n#:endif\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 2))]
     )
    ),
    ('line_if_inline_elif',
     ([],
      '#:if 1 < 2\nTrue\n#{elif 2 > 3}#\n',
      [(fypp.FyppFatalError, fypp.STRING, (2, 2))]
     )
    ),
    ('inline_if_line_elif',
     ([],
      '#{if 1 < 2}#True\n#:elif 2 > 3\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 2))]
     )
    ),
    ('line_if_inline_else',
     ([],
      '#:if 1 < 2\nTrue\n#{else}#\n',
      [(fypp.FyppFatalError, fypp.STRING, (2, 2))]
     )
    ),
    ('inline_if_line_else',
     ([],
      '#{if 1 < 2}#True\n#:else\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 2))]
     )
    ),
    ('loose_else',
     ([],
      'A\n#:else\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 2))]
     )
    ),
    ('loose_inline_else',
     ([],
      'A\n#{else}#\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 1))]
     )
    ),
    ('loose_elif',
     ([],
      'A\n#:elif 1 > 2\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 2))]
     )
    ),
    ('loose_inline_elif',
     ([],
      'A\n#{elif 1 > 2}#\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 1))]
     )
    ),
    ('loose_endif',
     ([],
      'A\n#:endif\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 2))]
     )
    ),
    ('loose_inline_endif',
     ([],
      'A\n#{endif}#\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 1))]
     )
    ),
    ('mismatching_else',
     ([],
      '#:if 1 < 2\n#:for i in range(3)\n#:else\n',
      [(fypp.FyppFatalError, fypp.STRING, (2, 3))]
     )
    ),
    ('mismatching_elif',
     ([],
      '#:if 1 < 2\n#:for i in range(3)\n#:elif 1 > 2\n',
      [(fypp.FyppFatalError, fypp.STRING, (2, 3))]
     )
    ),
    ('mismatching_endif',
     ([],
      '#:if 1 < 2\n#:for i in range(3)\n#:endif\n',
      [(fypp.FyppFatalError, fypp.STRING, (2, 3))]
     )
    ),
    ('line_def_inline_enddef',
     ([],
      '#:def alma(x)\n#{enddef}#\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 1))]
     )
    ),
    ('inline_def_line_enddef',
     ([],
      '#{def alma(x)}#Empty\n#:enddef\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 2))]
     )
    ),
    ('loose_enddef',
     ([],
      '#:enddef\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('loose_inline_enddef',
     ([],
      '#{enddef}#\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 0))]
     )
    ),
    ('mismatching_enddef',
     ([],
      '#:def test(x)\n#{if 1 < 2}#\n#:enddef\n',
      [(fypp.FyppFatalError, fypp.STRING, (2, 3))]
     )
    ),
    ('enddef_name_mismatch',
     ([],
      '#:def macro(var)\nMACRO|${var}$|\n#:enddef nonsense\n${macro(1)}$',
      [(fypp.FyppFatalError, fypp.STRING, (2, 3))]
     )
    ),
    ('inline_enddef_name_mismatch',
     ([],
      '#{def macro(var)}#MACRO|${var}$|#{enddef nonsense}#${macro(1)}$',
      [(fypp.FyppFatalError, fypp.STRING, (0, 0))]
     )
    ),
    ('endcall_name_mismatch',
     ([],
      '#:def macro(var)\nMACRO|${var}$|\n#:enddef\n'\
      '#:call macro\n1\n#:endcall nonsense\n',
      [(fypp.FyppFatalError, fypp.STRING, (5, 6))]
     )
    ),
    ('inline_endcall_name_mismatch',
     ([],
      '#:def macro(var)\nMACRO|${var}$|\n#:enddef\n'\
      '#{call macro}#1#{endcall nonsense}#',
      [(fypp.FyppFatalError, fypp.STRING, (3, 3))]
     )
    ),
    ('generator_endcall_name_mismatch',
     ([_inifile('include/caseconv.py')],
      '#:call caseconv("l")\nHELLO\n#:endcall invalid\n',
      [(fypp.FyppFatalError, fypp.STRING, (2, 3))]
     )
    ),
    ('inline_generator_endcall_name_mismatch',
     ([_inifile('include/caseconv.py')],
      '#{call caseconv("l")}#HELLO#{endcall nonsense}#',
      [(fypp.FyppFatalError, fypp.STRING, (0, 0))]
     )
    ),
    ('line_for_inline_endfor',
     ([],
      '#:for i in range(3)\nA\n#{endfor}#\n',
      [(fypp.FyppFatalError, fypp.STRING, (2, 2))]
     )
    ),
    ('inline_for_line_endfor',
     ([],
      '#{for i in range(3)}#Empty\n#:endfor\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 2))]
     )
    ),
    ('loose_endfor',
     ([],
      '#:endfor\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('loose_inline_endfor',
     ([],
      '#{endfor}#',
      [(fypp.FyppFatalError, fypp.STRING, (0, 0))]
     )
    ),
    ('mismatching_endfor',
     ([],
      '#:for i in range(3)\n#{if 1 < 2}#\n#:endfor\n',
      [(fypp.FyppFatalError, fypp.STRING, (2, 3))]
     )
    ),
    ('loose_endmute',
     ([],
      '#:endmute\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('mismatching_endmute',
     ([],
      '#:mute\n#{if 1 < 2}#\n#:endmute\n',
      [(fypp.FyppFatalError, fypp.STRING, (2, 3))]
     )
    ),
    ('unclosed_directive',
     ([],
      '#:if 1 > 2\nA\n',
      [(fypp.FyppFatalError, fypp.STRING, None)]
     )
    ),
    ('missing_space_after_directive',
     ([],
      '#:if(1 > 2)\nA\n#:endif',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('missing_space_after_inline_directive',
     ([],
      '#{if(1 > 2)}#A#{endif}#',
      [(fypp.FyppFatalError, fypp.STRING, (0, 0))]
     )
    ),
    #
    # Renderer errors
    #
    ('invalid_expression',
     ([],
      '${i}$',
      [(fypp.FyppFatalError, fypp.STRING, (0, 0))]
     )
    ),
    ('invalid_variable',
     ([],
      '#:set i 1.2.3\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('invalid_condition',
     ([],
      '#{if i >>> 3}##{endif}#',
      [(fypp.FyppFatalError, fypp.STRING, (0, 0))]
     )
    ),
    ('invalid_iterator',
     ([],
      '#:for i in 1.2.3\nDummy\n#:endfor\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('invalid_macro_prefix',
     ([],
      '#:def __test(x)\n#:enddef\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1)),
       (fypp.FyppFatalError, None, None)]
     )
    ),
    ('reserved_macro_name',
     ([],
      '#:def defined(x)\n#:enddef\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1)),
       (fypp.FyppFatalError, None, None)]
     )
    ),
    ('invalid_variable_prefix',
     ([],
      '#:set __test = 2\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1)),
       (fypp.FyppFatalError, None, None)]
     )
    ),
    ('reserved_variable_name',
     ([],
      '#:set _LINE_ = 2\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1)),
       (fypp.FyppFatalError, None, None)]
     )
    ),
    ('macro_call_more_args',
     ([],
      '#:def test(x)\n${x}$\n#:enddef\n$: test(\'A\', 1)\n',
      [(fypp.FyppFatalError, fypp.STRING, (3, 4)),
       (fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('macro_call_less_args',
     ([],
      '#:def test(x)\n${x}$\n#:enddef\n$: test()\n',
      [(fypp.FyppFatalError, fypp.STRING, (3, 4)),
       (fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('short_line_length',
     ([_linelen(4)],
      '',
      [(fypp.FyppFatalError, None, None)]
     )
    ),
    ('failing_macro_in_include',
     ([],
      '#:include "include/failingmacro.inc"\n$:failingmacro()\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 2)),
       (fypp.FyppFatalError, 'include/failingmacro.inc', (2, 3))]
     )
    ),
    ('incompatible_tuple_assignment',
     ([],
      '#:set a,b,c = (1, 2)\n${a}$${b}$${c}$\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('invalid_lhs_tuple1',
     ([],
      '#:set (a, b = (1, 2)\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1)),
       (fypp.FyppFatalError, None, None)]
     )
    ),
    ('invalid_lhs_tuple2',
     ([],
      '#:set a, b) = (1, 2)\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1)),
       (fypp.FyppFatalError, None, None)]
     )
    ),
    #
    # Command line errors
    #
    ('def_error',
     (['-DVAR=1.2.2'],
      '',
      [(fypp.FyppFatalError, None, None)]
     )
    ),
    ('missing_module',
     (['-mWhateverDummyKJFDKf'],
      '',
      [(fypp.FyppFatalError, None, None)]
     )
    ),
    ('missing_ini',
     (['-iWhateverDummyKJFDKf'],
      '',
      [(fypp.FyppFatalError, None, None)]
     )
    ),
    ('broken_ini',
     (['-iinclude/brokenini.py'],
      '',
      [(fypp.FyppFatalError, None, None)]
     )
    ),
    #
    # User requested stop
    #
    ('userstop',
     ([],
      '#:set A = 12\n#:if A > 10\n#:stop "Wrong A: {0}".format(A)\n#:endif\n',
      [(fypp.FyppStopRequest, fypp.STRING, (2, 3))]
     )
    ),
    ('invalid_userstop_expr',
     ([],
      '#:set A = 12\n#:if A > 10\n#:stop "Wrong A: {0}".format(BA)\n#:endif\n',
      [(fypp.FyppFatalError, fypp.STRING, (2, 3))]
     )
    ),
    ('invalid_inline_stop',
     ([],
      '#:set A = 1\n#:if A > 10\n#{stop "Wrong A: {0}".format(BA)}#\n#:endif\n',
      [(fypp.FyppFatalError, fypp.STRING, (2, 2))]
     )
    ),
    ('assert',
     ([],
      '#:set A = 12\n#:assert A < 10\n',
      [(fypp.FyppStopRequest, fypp.STRING, (1, 2))]
     )
    ),
    ('invalid_assert_expr',
     ([],
      '#:assert A < 10\n',
      [(fypp.FyppFatalError, fypp.STRING, (0, 1))]
     )
    ),
    ('invalid_inline_assert',
     ([],
      '#:set A = 12\n#{assert A < 10}#\n',
      [(fypp.FyppFatalError, fypp.STRING, (1, 1))]
     )
    ),
]


def get_test_output_method(args, inp, out):
    '''Returns a test method for checking correctness of Fypp output.

    Args:
        args (list of str): Command-line arguments to pass to Fypp.
        inp (str): Input with Fypp directives.
        out (str): Expected output.

    Returns:
       method: Method to test equality of output with result delivered by Fypp.
    '''

    def test_output(self):
        '''Tests whether Fypp result matches expected output.'''
        optparser = fypp.get_option_parser()
        options, leftover = optparser.parse_args(args)
        self.assertEqual(len(leftover), 0)
        tool = fypp.Fypp(options)
        result = tool.process_text(inp)
        self.assertEqual(out, result)
    return test_output


def get_test_exception_method(args, inp, exceptions):
    '''Returns a test method for checking correctness of thrown exception.

    Args:
        args (list of str): Command-line arguments to pass to Fypp.
        inp (str): Input with Fypp directives.
        exceptions (list of tuples): Each tuple contains an exception, a file
            name and a span (tuple or int). The tuples should be in reverse
            order (latest raised exception first).

    Returns:
       method: Method to test, whether Fypp throws the correct exception.
    '''

    def test_exception(self):
        '''Tests whether Fypp throws the correct exception.'''
        optparser = fypp.get_option_parser()
        options, leftover = optparser.parse_args(args)
        self.assertEqual(len(leftover), 0)
        try:
            tool = fypp.Fypp(options)
            _ = tool.process_text(inp)
        except Exception as e:
            raised = e
        else:
            self.fail('No exception was raised')
        for exc, fname, span in exceptions:
            self.assertTrue(isinstance(raised, exc))
            if fname is None:
                self.assertTrue(raised.fname is None)
            else:
                self.assertEqual(fname, raised.fname)
            if span is None:
                self.assertTrue(raised.span is None)
            else:
                self.assertEqual(span, raised.span)
            raised = raised.cause
        self.assertTrue(not isinstance(raised, fypp.FyppError))

    return test_exception


class TestContainer(unittest.TestCase):
    '''General test container class.'''

    @classmethod
    def add_test_methods(cls, tests, methodfactory):
        '''Adds tests to a test case.

        Args:
            tests (list of tuples): Tests to attach.
            testcase (TestCase): Class which the tests should be attached to.
            methodfactory (function): Functions which turns the tuples in
                tests into methods, which can be then attached to the test case.
        '''
        for itest, test in enumerate(tests):
            name = test[0]
            testargs = test[1]
            methodname = 'test{0}_{1}'.format(itest + 1, name)
            setattr(cls, methodname, methodfactory(*testargs))


class SimpleTest(TestContainer): pass
SimpleTest.add_test_methods(SIMPLE_TESTS, get_test_output_method)

class LineNumberingTest(TestContainer): pass
LineNumberingTest.add_test_methods(LINENUM_TESTS, get_test_output_method)

class IncludeTest(TestContainer): pass
IncludeTest.add_test_methods(INCLUDE_TESTS, get_test_output_method)

class ExceptionTest(TestContainer): pass
ExceptionTest.add_test_methods(EXCEPTION_TESTS, get_test_exception_method)


if __name__ == '__main__':
    unittest.main()
