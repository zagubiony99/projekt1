#!/usr/bin/env python3
"""Safety check for the CMS: would saving a file in Pages CMS lose any content?

Pages CMS keeps only fields declared in .pages.yml (lib/schema.ts: initializeState/deepMap)
and drops empty values on save (sanitizeObject). This script replays that on every content
file and fails if anything would be lost.

  python3 scripts/cms/check.py          # check
  python3 scripts/cms/check.py --write  # also rewrite files in the exact shape the CMS saves
                                        # (field order, false booleans), so the first edit
                                        # in the CMS produces a clean diff
"""
import json
import os
import sys
import yaml

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
DEFAULTS = {'boolean': False}


def init_state(data, fields):
    """Mirror of Pages CMS initializeState/deepMap: keep declared fields only, fill defaults."""
    out = {}
    data = data or {}
    for f in fields:
        v = data.get(f['name'])
        if f.get('list'):
            if v is None:
                out[f['name']] = []
            elif isinstance(v, list):
                out[f['name']] = [init_state(x, f['fields']) if f['type'] == 'object' else x for x in v]
            else:
                out[f['name']] = []
        elif f['type'] == 'object':
            out[f['name']] = init_state(v, f['fields'])
        else:
            out[f['name']] = v if v is not None else f.get('default', DEFAULTS.get(f['type'], ''))
    return out


def sanitize(o):
    """Mirror of Pages CMS sanitizeObject: drop None, '' and empty lists/objects."""
    empty = lambda v: v is None or v == ''
    if isinstance(o, list):
        return [x for x in (sanitize(v) if isinstance(v, (dict, list)) else v for v in o) if not empty(x)]
    if isinstance(o, dict):
        res = {}
        for k, v in o.items():
            v = sanitize(v) if isinstance(v, (dict, list)) else v
            if (isinstance(v, list) and all(empty(x) for x in v)) or (isinstance(v, dict) and not v) or empty(v):
                continue
            res[k] = v
        return res
    return o


def lost(orig, saved, path=''):
    """Paths whose non-empty value would disappear or change on save."""
    out = []
    if isinstance(orig, dict):
        for k, v in orig.items():
            p = f'{path}.{k}' if path else k
            if v in ('', None, [], {}):
                continue
            if not isinstance(saved, dict) or k not in saved:
                out.append(p)
            else:
                out += lost(v, saved[k], p)
    elif isinstance(orig, list):
        if not isinstance(saved, list) or len(saved) != len([x for x in orig if x not in ('', None)]):
            out.append(path)
        else:
            for i, (a, b) in enumerate(zip(orig, saved)):
                out += lost(a, b, f'{path}[{i}]')
    elif orig != saved:
        out.append(path)
    return out


def entries(items):
    for e in items:
        if e.get('type') == 'group':
            yield from entries(e['items'])
        else:
            yield e


def main():
    config = yaml.safe_load(open(os.path.join(ROOT, '.pages.yml'), encoding='utf-8'))
    write = '--write' in sys.argv
    problems = 0
    seen = set()
    for e in entries(config['content']):
        path = os.path.join(ROOT, e['path'])
        seen.add(os.path.normpath(path))
        data = json.load(open(path, encoding='utf-8'))
        saved = sanitize(init_state(data, e['fields']))
        miss = lost(data, saved)
        status = 'OK' if not miss else f'WOULD LOSE {len(miss)}: ' + ', '.join(miss[:8])
        print(f"{e['path']}: {status}")
        problems += len(miss)
        if write and not miss:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(saved, f, ensure_ascii=False, indent=2)
                f.write('\n')
    # every content file must be reachable from the CMS
    for dp, _, fn in os.walk(os.path.join(ROOT, 'content')):
        for name in fn:
            p = os.path.normpath(os.path.join(dp, name))
            if name.endswith('.json') and p not in seen:
                print(f'NOT IN CMS: {os.path.relpath(p, ROOT)}')
                problems += 1
    print('PASS' if not problems else f'FAIL ({problems})')
    sys.exit(1 if problems else 0)


main()
