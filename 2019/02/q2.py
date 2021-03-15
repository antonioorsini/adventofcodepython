program = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,19,5,23,1,23,9,27,2,27,6,31,1,31,6,35,2,35,9,39,1,6,39,43,2,10,43,47,1,47,9,51,1,51,6,55,1,55,6,59,2,59,10,63,1,6,63,67,2,6,67,71,1,71,5,75,2,13,75,79,1,10,79,83,1,5,83,87,2,87,10,91,1,5,91,95,2,95,6,99,1,99,6,103,2,103,6,107,2,107,9,111,1,111,5,115,1,115,6,119,2,6,119,123,1,5,123,127,1,127,13,131,1,2,131,135,1,135,10,0,99,2,14,0,0]

def runProgram( program ):
    command = []
    for idx in range( len( program ) ):
        command.append(program[ idx ])
        if len(command) == 4 or idx == len(program) - 1:
            if command[0] == 99:
                break
            elif command[0] == 1:
                program[command[3]] = program[command[1]] + program[command[2]]
            elif command[0] == 2:
                program[command[3]] = program[command[1]] * program[command[2]]
            command = []
    return program

def findSolution( problem ):
    cods = []
    for n in range(0,99):
        for v in range(0,99):
            cods.append([n,v])
    for cod in cods:
        n, v = cod[0], cod[1]
        program = problem.copy()
        program[1] = n
        program[2] = v
        solution = runProgram( program )[0]
        if solution == 19690720:
            print(n,v)
            break
    return 100 * n + v

def main():
    print( findSolution(program) )

if __name__ == '__main__':
    main()
