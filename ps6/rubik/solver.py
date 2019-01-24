import rubik


class LoopException:
    pass


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves.

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    if start == end:
        return []

    front = {0: [start]}
    back = {0: [end]}

    front_discovered = {start: (None, None)}  # position: parent, twist
    back_discovered = {end: (None, None)}

    common = None

    try:
        for i in range(0, 8):
            front[i + 1] = []
            for position in front.get(i):
                for twist in rubik.quarter_twists:
                    new = rubik.perm_apply(twist, position)

                    if position in back_discovered:
                        common = position
                        raise LoopException #TODO this is ugly as hell

                    if new not in front_discovered:
                        front[i + 1].append(new)
                        front_discovered[new] = (position, twist)

            back[i+1] = []
            for position in back.get(i):
                for twist in rubik.quarter_twists:
                    new = rubik.perm_apply(rubik.perm_inverse(twist), position)

                    if position in front_discovered:
                        common = position
                        raise LoopException  # TODO this is ugly as hell

                    if new not in back_discovered:
                        back[i + 1].append(new)
                        back_discovered[new] = (position, twist)
    finally:
        result = []
        current = common
        front_parent, twist = front_discovered[current]

        while front_parent is not None:
            result.append(twist)
            current = front_parent
            front_parent, twist = front_discovered[current]

        result.reverse()

        current = common
        back_parent, twist = back_discovered[current]

        while back_parent is not None:
            result.append(twist)
            current = back_parent
            back_parent, twist = back_discovered[current]

        return result
