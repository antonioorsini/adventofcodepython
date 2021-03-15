class ProgramDecoder( object ):

    def __init__(self):
        self.completed = False
        self.outputs = []
        self.relative_base = 0

    def setProgram( self, program ):
        memory_boost = 1_000
        self.op = program + [ 0 ] * memory_boost
        self.p  = self.op.copy()

    def readMode( self, param, param_mode ):
        if   param_mode == 0:
            return self.p[param]
        elif param_mode == 1:
            return param        
        elif param_mode == 2:
            return self.p[ param + self.relative_base]

    def writeMode( self, param, param_mode ):
        if param_mode in [0,1]:
            return param
        elif param_mode in [2]:
            return param + self.relative_base

    def runProgram( self, inputs = None ):
        self.idx_update = {0:4,1:4,2:4,3:2,4:2,5:0,6:0,7:4,8:4,9:2}
        command = []
        if not hasattr(self, 'idxs'):
            self.idxs = 0

        self.inputs_i = 0
        
        while self.idxs <= len( self.p ):
            idxe = self.idxs + 4 if len(self.p) - self.idxs >= 4 else self.idxs + (len(self.p) - self.idxs)
            command = self.p[ self.idxs : idxe ] 
            modes = [int(d) for d in str(command[0])] # command[0] contains the modes and the opcode
            while len(modes) <= 4:
                modes.insert(0, 0)
            opcode = int(str(modes[3]) + str(modes[4]))
            
            if opcode == 99:
                break
            elif opcode == 1:
                self.p[self.writeMode(command[3], modes[0])] = self.readMode(command[1], modes[2]) + self.readMode(command[2], modes[1])
            elif opcode == 2:                    
                self.p[self.writeMode(command[3], modes[0])] = self.readMode(command[1], modes[2]) * self.readMode(command[2], modes[1])
            elif opcode == 3:
                if inputs == None:
                    self.p[self.writeMode(command[1], modes[2])] = int(input('Opcode = 3, insert input: '))
                else:
                    if self.inputs_i < len(inputs):
                        self.p[self.writeMode(command[1], modes[2])] = inputs[ self.inputs_i ]
                        self.inputs_i += 1
                    else:
                        #self.idxs += self.idx_update[opcode]                   
                        return self.p
            elif opcode == 4:
                output = self.readMode(command[1], modes[2])
                self.outputs.append(output)
            elif opcode == 5:
                if self.readMode(command[1], modes[2]) != 0: 
                    self.idxs = self.readMode(command[2], modes[1])                
                else: 
                    self.idxs += 3
            elif opcode == 6:
                if self.readMode(command[1], modes[2]) == 0: 
                    self.idxs = self.readMode(command[2], modes[1])
                else: 
                    self.idxs += 3
            elif opcode == 7:
                self.p[self.writeMode(command[3], modes[0])] = 1 if self.readMode(command[1], modes[2]) < self.readMode(command[2], modes[1]) else 0
            elif opcode == 8:                  
                self.p[self.writeMode(command[3], modes[0])] = 1 if self.readMode(command[1], modes[2]) == self.readMode(command[2], modes[1]) else 0
            elif opcode == 9:
                self.relative_base += self.readMode(command[1], modes[2])

            self.idxs += self.idx_update[opcode] #update pointes
            command = []
        self.completed = True
        return self.p

    def resetProgram( self ):
        self.p = self.op.copy() 


class PaintingRobot( object ):

    def __init__( self, program ):
        self.direction = 1
        self.position = [0,0]
        self.paint_scheme = {}
        self.camera = ProgramDecoder()
        self.camera.setProgram( program )
        
    def updateDirection( self, value ):
        if value == 0:
            self.direction += -1
        elif value == 1:
            self.direction += +1

        if self.direction == 5:
            self.direction = 1
        elif self.direction == 0:
            self.direction = 4

    def move( self ):
        if self.direction == 1:
            self.position[1] += 1
        elif self.direction == 2:
            self.position[0] += 1
        elif self.direction == 3:
            self.position[1] += -1
        elif self.direction == 4:
            self.position[0] += -1

    def paint( self, colour ):
        self.paint_scheme.update( {tuple(self.position):colour} )

    def checkPanelColour( self ):
        if tuple(self.position) in self.paint_scheme:
            return self.paint_scheme[tuple(self.position)]
        else:
            return 0

    def showRegistration( self ):
        import six
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1,1)
        ax.set_facecolor('black')

        for panel, colour in six.iteritems(self.paint_scheme):
            if colour == 0:
                cl = 'black'
            if colour == 1:
                cl = 'white'
            plt.scatter(panel[0],panel[1], c = cl, s = 1)
        plt.show()

    def zugZug( self ):
        current_panel_colour = 1 # first amp output is gonna be 0, then update with the result
        stop_ = False
        first_ = True
        start_ = True
        while stop_ == False:              
            if start_ == False:
                current_panel_colour = self.checkPanelColour()
            else:
                start_ = False

            self.camera.runProgram( inputs = [current_panel_colour] )

            new_panel_colour = self.camera.outputs[-2]
            new_direction = self.camera.outputs[-1]

            self.paint( new_panel_colour )

            self.updateDirection( new_direction )
            self.move()

            if self.camera.completed == True:
                stop_ = True

        return self.paint_scheme
        
def main():
    p = [3,8,1005,8,318,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1002,8,1,28,1,107,14,10,1,107,18,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,58,1006,0,90,2,1006,20,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,88,2,103,2,10,2,4,7,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,118,1,1009,14,10,1,1103,9,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1002,8,1,147,1006,0,59,1,104,4,10,2,106,18,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,181,2,4,17,10,1006,0,36,1,107,7,10,2,1008,0,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,217,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,240,1006,0,64,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,1002,8,1,264,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1001,8,0,287,1,1104,15,10,1,102,8,10,1006,0,2,101,1,9,9,1007,9,940,10,1005,10,15,99,109,640,104,0,104,1,21102,932700857236,1,1,21101,335,0,0,1106,0,439,21101,0,387511792424,1,21101,346,0,0,1106,0,439,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,46372252675,0,1,21102,393,1,0,1106,0,439,21101,97806162983,0,1,21102,404,1,0,1105,1,439,3,10,104,0,104,0,3,10,104,0,104,0,21102,1,825452438376,1,21101,0,427,0,1106,0,439,21102,709475586836,1,1,21101,0,438,0,1106,0,439,99,109,2,22101,0,-1,1,21101,40,0,2,21102,1,470,3,21102,1,460,0,1106,0,503,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,465,466,481,4,0,1001,465,1,465,108,4,465,10,1006,10,497,1101,0,0,465,109,-2,2105,1,0,0,109,4,2102,1,-1,502,1207,-3,0,10,1006,10,520,21102,1,0,-3,21202,-3,1,1,21202,-2,1,2,21101,0,1,3,21101,0,539,0,1106,0,544,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,567,2207,-4,-2,10,1006,10,567,22101,0,-4,-4,1106,0,635,21202,-4,1,1,21201,-3,-1,2,21202,-2,2,3,21102,586,1,0,1105,1,544,22101,0,1,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,605,21102,0,1,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,627,22101,0,-1,1,21102,1,627,0,106,0,502,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0] 
    robot = PaintingRobot( p )
    robot.zugZug()
    robot.showRegistration()
    
    #pd = ProgramDecoder( )
    #pd.setProgram( p )
    #pd.runProgram()

if __name__ == '__main__':
    main()