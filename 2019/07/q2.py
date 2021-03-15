from itertools import permutations

class ProgramDecoder( object ):

    def __init__(self):
        self.completed = False
        self.outputs = []

    def setProgram( self, program ):
        self.op = program 
        self.p  = self.op.copy()

    def readMode( self, param, param_mode ):
        if   param_mode == 0:
            return self.p[param]
        elif param_mode == 1:
            return param        

    def runProgram( self, inputs = None ):
        self.idx_update = {0:4,1:4,2:4,3:2,4:2,5:0,6:0,7:4,8:4}
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
            #print(command,modes)
            if opcode == 99:
                break
            elif opcode == 1:
                self.p[command[3]] = self.readMode(command[1], modes[2]) + self.readMode(command[2], modes[1])
            elif opcode == 2:                    
                self.p[command[3]] = self.readMode(command[1], modes[2]) * self.readMode(command[2], modes[1])
            elif opcode == 3:
                if inputs == None:
                    self.p[command[1]] = int(input('Opcode = 3, insert input: '))
                else:
                    if self.inputs_i < len(inputs):
                        self.p[command[1]] = inputs[ self.inputs_i ]
                        self.inputs_i += 1
                    else:                        
                        return self.p
            elif opcode == 4:
                output = self.readMode(command[1], modes[2])
                self.outputs.append(output)
            elif opcode == 5:
                if self.readMode(command[1], modes[2]) != 0: self.idxs = self.readMode(command[2], modes[1])                
                else: self.idxs += 3
            elif opcode == 6:
                if self.readMode(command[1], modes[2]) == 0: self.idxs = self.readMode(command[2], modes[1])
                else: self.idxs += 3
            elif opcode == 7:
                self.p[command[3]] = 1 if self.readMode(command[1], modes[2]) < self.readMode(command[2], modes[1]) else 0
            elif opcode == 8:                  
                self.p[command[3]] = 1 if self.readMode(command[1], modes[2]) == self.readMode(command[2], modes[1]) else 0

            self.idxs += self.idx_update[opcode] #update pointes
            command = []
        self.completed = True
        return self.p

    def resetProgram( self ):
        self.p = self.op.copy() 

class AmplifierChain():
    def __init__( self, n ):
        self.n_amps = n
        self.createAmps()

    def createAmps( self ) :
        self.amps = []
        for n in range( self.n_amps ):
            self.amps.append( ProgramDecoder() )

    def insertControllerSofware( self, program ):
        for i in range(len(self.amps)):
            self.amps[i].setProgram( program )

    def insertAmpSettings( self, settings ):
        self.amp_settings = settings

    def amplify( self ):
        amp_output = 0 # first amp output is gonna be 0, then update with the result
        stop_ = False
        first_ = True
        while stop_ == False:                        
            for i, amp in enumerate(self.amps): 
                if first_ == True:               
                    amp.runProgram( inputs = [self.amp_settings[i], amp_output] )
                else:
                    amp.runProgram( inputs = [amp_output] )
                amp_output = amp.outputs[-1]
                if amp.completed == True and i == 4:
                    stop_ = True
                    break                                
            first_ = False
        return amp_output # returns the last thruster

    def findMaxThruster( self, amp_settings, program ):
        thrusters = []        
        for p in permutations( amp_settings ):
            self.createAmps()
            self.insertControllerSofware( program )
            self.insertAmpSettings( list( p ) )
            thr = self.amplify() 
            thrusters.append( thr )
        print(max(thrusters))        

def main():
    program   = [3,8,1001,8,10,8,105,1,0,0,21,42,55,76,89,114,195,276,357,438,99999,3,9,1001,9,3,9,1002,9,3,9,1001,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,101,5,9,9,4,9,99,3,9,102,3,9,9,101,5,9,9,1002,9,2,9,101,4,9,9,4,9,99,3,9,102,5,9,9,1001,9,3,9,4,9,99,3,9,1001,9,4,9,102,5,9,9,1001,9,5,9,1002,9,2,9,101,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99]
    program_1 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    program_2 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]    
    ac = AmplifierChain( 5 )
    ac.findMaxThruster([9,7,8,5,6], program)
    
    #pg.runProgram([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0])
    #pg.runProgram([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0])

if __name__ == '__main__':
    main()



