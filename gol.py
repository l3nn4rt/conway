#!/usr/bin/env python3

import os
import time


class State:

    def __init__(self):
        self.alive = set()

    def __str__(self):
        if not self.alive:
            return ''
        xs, ys = list(zip(*self.alive))
        rows = []
        for i in range(min(xs) - 1, max(xs) + 2):
            row = []
            for j in range(min(ys) - 1, max(ys) + 2):
                row.append('@' if (i, j) in self.alive else '.')
            rows.append(' '.join(row))
        return '\n'.join(rows)

    def toggle(self, x, y):
        self.alive.symmetric_difference_update({(x, y)})


class Game:

    def __init__(self):
        self.finished = False
        self.time = 0
        self.state = State()

    def neighs(self, x, y):
        return {
            (x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
            (x, y - 1),                 (x, y + 1),
            (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)
        }

    def step(self):
        '''update global state'''
        prev_state = self.state
        self.time += 1
        self.state = State()

        # cells to be updated
        hot_cells = set()
        for (x, y) in prev_state.alive:
            hot_cells.add((x, y))
            hot_cells.update(self.neighs(x, y))

        for (x, y) in hot_cells:
            cell_state = (x, y) in prev_state.alive
            neighs = self.neighs(x, y)
            live_neighs = len(neighs & prev_state.alive)

            if cell_state and live_neighs in (2, 3):
                # keep alive
                self.state.alive.add((x, y))
            elif not cell_state and live_neighs == 3:
                # come to life
                self.state.alive.add((x, y))

        self.finished = self.state.alive == prev_state.alive

    def toggle(self, x, y):
        '''toggle cell state'''
        self.state.toggle(x, y)

    def __str__(self):
        return '\n'.join([
            f'current time: {self.time}',
            f'cells alive: {len(self.state.alive)}',
            '',
            str(self.state),
        ])

    def block(self, x, y):
        '''
        . . y . .
        . . . . .
        x . @ @ .
        . . @ @ .
        . . . . .
        '''
        for (i, j) in [(x, y), (x, y+1), (x+1, y), (x+1, y+1)]:
            self.state.toggle(i, j)

    def blink(self, x, y):
        '''
        . . . y . .
        . . . . . .
        x . @ @ @ .
        . . . . . .
        '''
        for (i, j) in [(x, y-1), (x, y), (x, y+1)]:
            self.state.toggle(i, j)

    def glider(self, x, y):
        '''
        . . . y . .
        . . . . . .
        . . . @ . .
        x . . . @ .
        . . @ @ @ .
        . . . . . .
        '''
        for (i, j) in [(x-1, y), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]:
            self.state.toggle(i, j)

    def r_pentomino(self, x, y):
        '''
        . . . y . .
        . . . . . .
        . . . @ @ .
        x . @ @ . .
        . . . @ . .
        . . . . . .
        '''
        for (i, j) in [(x-1, y), (x-1, y+1), (x, y-1), (x, y), (x+1, y)]:
            self.state.toggle(i, j)


def main():
    g = Game()

    g.block(0, 0)
    g.blink(5, 1)
    g.glider(1, 5)
    g.r_pentomino(12, 12)

    while True:
        try:
            os.system('clear')
            print(g)

            g.step()
            if g.finished:
                break

            time.sleep(.1)
        except KeyboardInterrupt:
            print()
            break


if __name__ == '__main__':
    main()
