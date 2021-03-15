import six 

class Navigator():
    def __init__( self ):
        self.orbits_chains = None
        self.orbits_map = None

    def readMap( self ):
        self.orbits_map = []
        while True:
            line = input()
            if line:
                self.orbits_map.append(line)
            else:
                break
        self.orbits_map = '\n'.join(self.orbits_map).split('\n')
        self.orb_map = []
        for orbit in self.orbits_map:
            orb = orbit.split(')') 
            self.orb_map.append( [orb[0], orb[1]] )                    
        return self.orb_map

    def orderMap( self ):
        self.ord_map = []
        for orbx in self.orb_map:
            if orbx[0] == 'COM':
                self.ord_map.append(orbx)
        contx = True
        while contx:
            contx = False
            ord_map_temp = self.ord_map.copy()
            for orbx in ord_map_temp:
                conty = True
                while conty:
                    conty = False
                    for orby in self.orb_map:
                        if orbx != orby and orbx[1] == orby[0] and orby not in self.ord_map:
                            self.ord_map.append(orby)
                            orbx = orby
                            contx = True
                            conty = True
        return self.ord_map

    def createOrbitsChains( self ):
        self.orbits_chains = {}
        for orb in self.ord_map:
            cnt = orb[0]
            sat = orb[1]
            if cnt not in self.orbits_chains:
                self.orbits_chains[sat] = [cnt,sat]
            else:
                self.orbits_chains[sat] = self.orbits_chains[cnt] + [sat]
        for key, value in list(six.iteritems(self.orbits_chains)): # clean last value after having used it
            self.orbits_chains[key] = value[:-1]
        return self.orbits_chains
        
    def unravelOrbitsChains( self ):
        self.dconn = []
        self.indirect_connections = []
        for key, value in list(six.iteritems(self.orbits_chains)):
            for i, orb in enumerate(value):
                if i == len(value) - 1:
                    self.dconn.append([key, orb])
                else:
                    self.indirect_connections.append([key,orb])
        
        return self.dconn, self.indirect_connections

    def countConnections( self ):
        print(len(self.dconn) + len(self.indirect_connections))

    def connectToSanta( self ):
        orbcy = self.orbits_chains['YOU']
        orbcs = self.orbits_chains['SAN']
        for o in orbcy[::-1]:
            if o in orbcs[::-1]:
                movesy = orbcy[ orbcy.index(o): ]
                movess = orbcs[ orbcs.index(o): ]
                break
        movesy.reverse()
        path = movesy[:-1] + movess
        print( len(path) -1 )

nv = Navigator()
nv.readMap()
nv.orderMap()
nv.createOrbitsChains()
nv.connectToSanta()


