import items
def level(Board, Loc):
    row1 = [
         Board(rooms = [(Loc(30,7),10,5),
                        ],
               corridors = [(Loc(40,10), None, 'r'),
                           ],
               items = [items.lent_doll]
               ),

         Board(rooms = [(Loc(30,7),10,5),
                        ],
               corridors = [
                            (Loc(35,10), None, 'l'),
                            (Loc(36,10), None, 'd'),
                            ]
               ),


    ]

    row2 = \
         [
         Board(rooms = [(Loc(30,7),10,5),
                        ],
               corridors = [
                            (Loc(35,10), None, 'r'),
                            ]
               ),

         Board(rooms = [(Loc(30,7),10,5),
                        ],
               corridors = [
                            (Loc(35,10), None, 'l'),
                            (Loc(35,10), None, 'u'),
                            ]
               ),
         ]

    return [row1, row2]
