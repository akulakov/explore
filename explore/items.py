
from shared import Object

class Item(Object):
    pass


celtic_knife = Item("Knife", '🔪', 1000)
celtic_knife.description = """
A knife with a celtic knot engraved on the hilt. The knife is sunk into a heavy stone
and cannot be removed.
"""

clover = Item("Clover", '🍀', 1)
clover.description = """
A clover leaf.
"""

lent_doll = Item("Doll", '࿄', 1000)
lent_doll.description = """
A doll, crudely sown out of burlap with a simple linen clothes with
a repeating geometric pattern, wearing a small lump of vaguely shaped
wrought iron as a medallion; its face is left blank without features.  It
is suspended from a coarse pole on a hemp rope attached to its upper back.

The pole is firmly implanted into the ground.
"""

items = [i for i in locals().values() if isinstance(i, Item)]
