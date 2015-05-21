import subprocess
import json
import collections
import random
import sys

def solve():
    """Run clingo with the provided argument list and return the parsed JSON result."""
    
    CLINGO = "./clingo"

    GRINGO = "./gringo"

    REIFY = "./reify"
    
    gringo = subprocess.Popen(
        [GRINGO, "level-core.lp", "level-style.lp", "level-sim.lp", "level-shortcuts.lp"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    reify = subprocess.Popen(
        [REIFY],
        stdin=gringo.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    clingo = subprocess.Popen(
        [CLINGO, "-", "meta.lp", "metaD.lp", "metaO.lp", "metaS.lp", "--parallel-mode=4", "--outf=2"],
        stdin=reify.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    clingo_out, clingo_err = clingo.communicate()
    if clingo_err:
        print clingo_err
    return parse_json_result(clingo_out)


def parse_json_result(out):
    """Parse the provided JSON text and extract a dict
    representing the predicates described in the first solver result."""

    result = json.loads(out)
    
    assert len(result['Call']) > 0
    assert len(result['Call'][0]['Witnesses']) > 0
    
    witness = result['Call'][0]['Witnesses'][0]['Value']
    
    class identitydefaultdict(collections.defaultdict):
        def __missing__(self, key):
            return key
    
    preds = collections.defaultdict(set)
    env = identitydefaultdict()
    
    for atom in witness:
        if '(' in atom:
            left = atom.index('(')
            functor = atom[:left]
            arg_string = atom[left:]
            try:
                preds[functor].add( eval(arg_string, env) )
            except TypeError:
                pass # at least we tried...
            
        else:
            preds[atom] = True
    
    return dict(preds)

def render_ascii_dungeon(design):
    """Given a dict of predicates, return an ASCII-art depiction of the a dungeon."""
    
    sprite = dict(design['sprite'])
    param = dict(design['param'])
    width = param['width']
    glyph = dict(space='.', wall='W', altar='a', gem='g', trap='_')
    block = ''.join([''.join([glyph[sprite.get((r,c),'space')]+' ' for c in range(width)])+'\n' for r in range(width)])
    return block

def main(args):
    design_dict = solve()
    f = open('boardwalk.txt', 'w')
    print >> f,  render_ascii_dungeon(design_dict)
    print render_ascii_dungeon(design_dict)

if __name__ == "__main__":
    sys.exit(not main(sys.argv))