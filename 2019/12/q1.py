from itertools import combinations

def applyGravity( moons ):
    names = moons.keys()
    pairs = list(combinations( names, 2 ))

    vels = {}
    for n in names:
        vels.update({n:[0,0,0]})

    for pair in pairs:
        ma = moons[pair[0]]
        mb = moons[pair[1]]
        for i in range(3):
            if ma.pos[i] < mb.pos[i]:
                vels[pair[0]][i] += +1
                vels[pair[1]][i] += -1
            elif ma.pos[i] > mb.pos[i]:
                vels[pair[0]][i] += -1
                vels[pair[1]][i] += +1

    for name in names:
        for i in range(3):
            moons[name].vel[i] += vels[name][i]

    return moons

def applyVelocity( moons ):
    for moon in moons.keys():
        for i in range(3):
            moons[moon].pos[i] += moons[moon].vel[i]
    return moons

def calculateEnergy( moons ):
    for name in moons.keys():
        tot, pot, kin = 0, 0, 0
        for i in range(3):
            pot += abs(moons[name].pos[i])
            kin += abs(moons[name].vel[i])
        tot = pot*kin

        moons[name].pote = pot
        moons[name].kine = kin
        moons[name].tote = tot

    return moons

class Moon( object ):
    def __init__( self, pos ):
        self.pos = pos
        self.vel = [0,0,0]
        self.pote = 0
        self.kine = 0
        self.tote = 0

moons = {
    0:Moon([-4,3,15]),
    1:Moon([-11,-10,13]),
    2:Moon([2,2,18]),
    3:Moon([7,-1,0]),
}

# moons = {
#     0:Moon([-8,-10,0]),
#     1:Moon([5,5,10]),
#     2:Moon([2,-7,3]),
#     3:Moon([9,-8,-3]),
# }


xh = []
yh = []
zh = []

foundx = foundy = foundz = False

xstep = 0
ystep = 0
zstep = 0

for step in range(100_000_000):
    xcs = []
    ycs = []
    zcs = []
    import six
    for name, moon in list(six.iteritems(moons)):        
        xcs.append( (name, moon.pos[0], moon.vel[0] ) )
        ycs.append( (name, moon.pos[1], moon.vel[1] ) )
        zcs.append( (name, moon.pos[2], moon.vel[2] ) )

    xcs = tuple(xcs)
    ycs = tuple(ycs)
    zcs = tuple(zcs)


    if xcs in xh and foundx == False:
        print('FOUND X %s', step)
        print(xcs)
        xstep = step
        foundx = True
    if ycs in yh and foundy == False:
        print('FOUND Y %s', step)
        ystep = step
        foundy = True
    if zcs in zh and foundz == False:
        print('FOUND Z %s', step)
        zstep = step
        foundz = True
        
    if step == 0:
        xh.append(xcs)
        yh.append(ycs)
        zh.append(zcs)

    if foundx == foundy == foundz == True:
        break

    moons = applyGravity(moons)
    moons = applyVelocity(moons)


from math import gcd
a = [xstep,ystep,zstep]   #will work for an int array of any length
lcm = a[0]
for i in a[1:]:
  lcm = int(lcm)*int(i)/gcd(int(lcm), int(i))
print(lcm)

moons = calculateEnergy(moons)
print(sum([m.tote for m in moons.values()]))


