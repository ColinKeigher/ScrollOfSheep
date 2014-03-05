# -*- coding: utf-8 -*-

import os

class send_print():
    def __init__(s, printer='/dev/lp0', spacing=None):
        s.printer = printer
        s.spaces = spacing

    # Filter for printing multiple lines at once or just one. Kind of hacky but works.
    def _check_lines(s, lines):
        output = [ lines ]
        if type(lines) != str:
            try:
                output = [ x for x in lines ]
            except:
                pass
        return output

    # Creates new lines on paper
    def _check_spacing(s):
        if s.spaces != None:
            for x in xrange(0, s.spaces):
                s._write_blank()

    # Stupid simple to write to a receipt printer
    def _write(s, line):
        with open(s.printer, 'w') as printer:
            printer.write('%s\n' % line)

    def _write_blank(s):
        s._write('')

    def write_out(s, data):
        for item in s._check_lines(data):
            s._write(item)
        s._check_spacing()
