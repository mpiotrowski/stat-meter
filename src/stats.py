#!/usr/bin/python
import os, sys

def _is_break(line):
    return not line.strip()

def _get_field(line, field):
    try:
        _line = line.split(':')
        _field_name = _line[0].strip()
        _field_value = _line[1].strip()

        return _field_value if _field_name == field else None
    except:
        return None

def cpu_values():
    results = {}
    with open('/proc/stat', 'r') as cpu_usage:
        for line in cpu_usage:
            entry = line.strip().split()
            if entry and entry[0].startswith('cpu'):
                _cpu = {}
                entry[1:] = [int(x) for x in entry[1:]]
                _sum = sum(entry[1:])
                _cpu['sum'] = _sum
                _cpu['user'] = entry[1]
                _cpu['nice'] = entry[2]
                _cpu['system'] = entry[3]
                _cpu['idle'] = entry[4]
                results[entry[0][-1]] = _cpu
    return results

def mem_values():
    results = {
            'total': None,
            'free': None
            }
    with open('/proc/meminfo', 'r') as mem_usage:
        for line in mem_usage:
            results['total'] = _get_field(line, 'MemTotal') or results['total']
            results['free'] = _get_field(line, 'MemFree') or results['free']
    return results

def cores_from_cpu_info():
    results = {}
    _part_result = {
            'proc_num' : None,
            'proc_name': None
            }
    with open('/proc/cpuinfo', 'r') as cpu_info:
        for line in cpu_info:
            if _is_break(line):
                results[_part_result['proc_num']] = _part_result['proc_name']
                _part_result = {
                        'proc_num' : None,
                        'proc_name': None
                        }
                continue

            _part_result['proc_name'] = _get_field(line, 'model name') or _part_result['proc_name']
            _part_result['proc_num'] = _get_field(line, 'processor') or _part_result['proc_num']

    return results
