from mwparserfromhell.nodes import Template
from scripts.utils.parser_helper import get_value, sanitize_template

class MapVeto(object):
    def __init__(self, veto: Template = None) -> None:
        self.veto = veto

    def process(self):
        if self.veto is None:
            return
        sanitize_template(self.veto)

        
    def __str__(self) -> str:
        out = '{{MapVeto'

        firstpick = get_value(self.veto, 'firstban')
        if firstpick:
            out += f'\n\t\t|firstpick={firstpick}'
        vetoTypes = ""
        for x in range(1, 5):
            key = 'r'+str(x)
            if self.veto.has(key):
                vetoTypes += get_value(self.veto, key) + ","
        if vetoTypes[-1] == ",":
            vetoTypes = vetoTypes[0: -1]
        out += f'\n\t\t|types={vetoTypes}'
        for mapIdx in range(1, 4):
            outMapBan = ""
            for teamIdx in range(1, 3):
                key = 't' + str(teamIdx) + 'map' + str(mapIdx)
                if self.veto.has(key):
                    outMapBan += f'|{key}={get_value(self.veto, key)}'
            out += '\n\t\t' + outMapBan

        decider = get_value(self.veto, 'map4')
        if decider:
            out += '\n\t\t|decider=' + decider

        out+="\n\t"
        return out + '}}'
