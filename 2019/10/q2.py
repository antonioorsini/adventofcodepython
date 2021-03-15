from itertools import combinations, product
import sys
import math
import numpy as np
import operator

class AsteroidMap( object ):
    def __init__(self, asteroid_map):
        self.m = asteroid_map
        self.getAsteroids()
        self.getAsteroidsList()

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

    def getAsteroidsList( self ):
        self.asteroids_list = []
        for ast in self.asteroids:
            self.asteroids_list.append((ast.x,ast.y))

            


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
    return max(visibilities, key=visibilities.get)

def getPairs( self ):
    self.combs = combine(am.asteroids, 2)

def get_vaporization_order(coordinates, mx, my):
    vaporized = [(mx, my)]
    while len(vaporized) != len(coordinates):
        closest_points = {}
        for x, y in coordinates:
            if (x, y) not in vaporized:
                dx, dy = x - mx, y - my
                dx, dy = dx // math.gcd(dx, dy), dy // math.gcd(dx, dy)
                closestx, closesty = closest_points.get((dx, dy), (float('inf'), float('inf')))
                if abs(x - mx) + abs(y - my) < abs(closestx - mx) + abs(closesty - my):
                    closest_points[(dx, dy)] = (x, y)
        vaporized += sorted(closest_points.values(), key=lambda p:-math.atan2(p[0] - mx, p[1] - my))
    return vaporized

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
    #stat = getMaxVisibilities(am) # get station asteroid
    #stat = (11,13)
    stat = (22,19)
    vaporization_order = get_vaporization_order( am.asteroids_list ,stat[0], stat[1] )
    print(vaporization_order[200][0] * 100 + vaporization_order[200][1])

if __name__ == '__main__':
    main()