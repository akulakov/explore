
from shared import Object

class NPC(Object):
    pass

npc1 = NPC("Lachesis", 'ൠ')
npc1.description = """
A skinny fellow in a red jacket, with long flowing yellow hair. He is
wearing high red shoes.
"""

npcs = [i for i in locals().values() if getattr(i, "name", None)]
