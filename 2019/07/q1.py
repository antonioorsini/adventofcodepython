from itertools import permutations

class ProgramDecoder( object ):

    def __init__(self, program):
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
        idxs = 0
        self.inputs_i = 0
        self.outputs = []
        while idxs <= len( self.p ):
            idxe = idxs + 4 if len(self.p) - idxs >= 4 else idxs + (len(self.p) - idxs)
            command = self.p[ idxs : idxe ] 
        
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
                    self.p[command[1]] = inputs[ self.inputs_i ]
                    self.inputs_i += 1
            elif opcode == 4:
                output = self.readMode(command[1], modes[2])
                self.outputs.append(output)
            elif opcode == 5:
                if self.readMode(command[1], modes[2]) != 0: idxs = self.readMode(command[2], modes[1])                
                else: idxs += 3
            elif opcode == 6:
                if self.readMode(command[1], modes[2]) == 0: idxs = self.readMode(command[2], modes[1])
                else: idxs += 3
            elif opcode == 7:
                self.p[command[3]] = 1 if self.readMode(command[1], modes[2]) < self.readMode(command[2], modes[1]) else 0
            elif opcode == 8:                  
                self.p[command[3]] = 1 if self.readMode(command[1], modes[2]) == self.readMode(command[2], modes[1]) else 0

            idxs += self.idx_update[opcode] #update pointes
            command = []
        return self.p

    def resetProgram( self ):
        self.p = self.op.copy() 

    def amplify( self, amp_settings ):
        amp_output = 0 # first amp output is gonna be 0, then update with the result
        program = [3,8,1001,8,10,8,105,1,0,0,21,42,55,76,89,114,195,276,357,438,99999,3,9,1001,9,3,9,1002,9,3,9,1001,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,101,5,9,9,4,9,99,3,9,102,3,9,9,101,5,9,9,1002,9,2,9,101,4,9,9,4,9,99,3,9,102,5,9,9,1001,9,3,9,4,9,99,3,9,1001,9,4,9,102,5,9,9,1001,9,5,9,1002,9,2,9,101,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99]
        for aset in amp_settings:
            self.runProgram( inputs = [aset, amp_output])
            amp_output = self.outputs[-1]
            self.resetProgram()
        return amp_output # returns the last thruster

    def findMaxThruster( self, range_signal = 4, len_signal = 5):
        signals  = [ x for x in range(range_signal+1) ]
        thrusters = []
        for p in permutations(signals):            
            thrusters.append( self.amplify( list( p ) ) )
        print(max(thrusters))        

def main():
    program = [3,8,1001,8,10,8,105,1,0,0,21,42,55,76,89,114,195,276,357,438,99999,3,9,1001,9,3,9,1002,9,3,9,1001,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,101,5,9,9,4,9,99,3,9,102,3,9,9,101,5,9,9,1002,9,2,9,101,4,9,9,4,9,99,3,9,102,5,9,9,1001,9,3,9,4,9,99,3,9,1001,9,4,9,102,5,9,9,1001,9,5,9,1002,9,2,9,101,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99]
    program_1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    program_2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    program_3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    pg = ProgramDecoder( program )
    #pg.amplify([1,0,4,3,2])
    #pg.runProgram([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0])
    #pg.runProgram([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0])
    pg.findMaxThruster()

if __name__ == '__main__':
    main()



