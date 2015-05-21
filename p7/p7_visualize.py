import sys
import json
import collections


def parse_json_result(input):
    result = input

    assert len(result['Call']) > 0
    assert len(result['Call'][0]['Witnesses']) > 0

    witness = result['Call'][0]['Witnesses'][0]['Value']

    class IdentityDefaultDict(collections.defaultdict):
        def __missing__(self, key):
            return key

    preds = collections.defaultdict(set)
    env = IdentityDefaultDict()

    for atom in witness:
        if '(' in atom:
            left = atom.index('(')
            functor = atom[:left]
            arg_string = atom[left:]
            try:
                preds[functor].add(eval(arg_string, env))
            except TypeError:
                pass  # at least we tried...

        else:
            preds[atom] = True

    return dict(preds)


def render_ascii_dungeon(design):
    """Given a dict of predicates, return an ASCII-art depiction of the a dungeon."""

    sprite = dict(design['sprite'])
    param = dict(design['param'])
    width = param['width']
    glyph = dict(space='.', wall='W', altar='a', gem='g', trap='_')
    block = ''.join([''.join([glyph[sprite.get((r, c), 'space')]+' ' for c in range(width)])+'\n' for r in range(width)])
    return block


def main(args):
    try:
        input_file = open(args[1])
        input = json.load(input_file)
        input_file.close()

        map = parse_json_result(input)
        print render_ascii_dungeon(map)
    except IndexError:
        return False

    return True

if __name__ == "__main__":
    sys.exit(not main(sys.argv))