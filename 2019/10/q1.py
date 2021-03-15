from itertools import combinations, product
import sys
import numpy as np
import operator

class AsteroidMap( object ):
    def __init__(self, asteroid_map):
        self.m = asteroid_map
        self.getAsteroids()

    def getAsteroids( self ):
        self.ys, self.xs = 0, 0
        self.asteroids = []
        for element in self.m:            
            if element == '\n':
                self.ys += 1
                self.xs = 0
            elif element in ['.', '#']:
                if element == '#':
                    asteroid = Asteroid( self.xs, self.ys )
                    self.asteroids.append( asteroid )
                self.xs += 1            


class Asteroid( object ):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = (x,y)
        self.visibility = 0

def isBetween(a, b, c):
    crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)

    # compare versus epsilon for floating point values, or != 0 if using integers
    if abs(crossproduct) != 0:
        return False

    dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
    if dotproduct < 0:
        return False

    squaredlengthba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
    if dotproduct > squaredlengthba:
        return False

    return True

def combine(arr, s): 
    return list(product(arr, repeat = s)) 

def getMaxVisibilities( am ):
    visibilities = {}
    for ast in am.asteroids:
        visibilities[ast] = 0

    combins = combine(am.asteroids, 2)
    
    for comb in combins:
        is_visible = True
        for ast in am.asteroids:
            if ast not in comb:
                if isBetween(comb[0], comb[1], ast):
                    is_visible = False
                    break
                    #print(comb[0].x, comb[0].y, comb[1].x, comb[1].y, ast.x, ast.y)
        if is_visible == True:
            visibilities[comb[0]] += 1

    print(visibilities[max(visibilities, key=visibilities.get)])

def main():
    asteroid_map = '''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##'''

    ast_map = '''###..#.##.####.##..###.#.#..
                 #..#..###..#.......####.....
                 #.###.#.##..###.##..#.###.#.
                 ..#.##..##...#.#.###.##.####
                 .#.##..####...####.###.##...
                 ##...###.#.##.##..###..#..#.
                 .##..###...#....###.....##.#
                 #..##...#..#.##..####.....#.
                 .#..#.######.#..#..####....#
                 #.##.##......#..#..####.##..
                 ##...#....#.#.##.#..#...##.#
                 ##.####.###...#.##........##
                 ......##.....#.###.##.#.#..#
                 .###..#####.#..#...#...#.###
                 ..##.###..##.#.##.#.##......
                 ......##.#.#....#..##.#.####
                 ...##..#.#.#.....##.###...##
                 .#.#..#.#....##..##.#..#.#..
                 ...#..###..##.####.#...#..##
                 #.#......#.#..##..#...#.#..#
                 ..#.##.#......#.##...#..#.##
                 #.##..#....#...#.##..#..#..#
                 #..#.#.#.##..#..#.#.#...##..
                 .#...#.........#..#....#.#.#
                 ..####.#..#..##.####.#.##.##
                 .#.######......##..#.#.##.#.
                 .#....####....###.#.#.#.####
                 ....####...##.#.#...#..#.##.'''
 
    am = AsteroidMap( ast_map )
    
    getMaxVisibilities(am)

    
if __name__ == '__main__':
    main()