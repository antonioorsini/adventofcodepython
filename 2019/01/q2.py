import pandas as pd
import math

def findModuleFuel( mass ):
    return math.floor( mass / 3 ) - 2

def findModuleFuelComplete( mass ):
    fuel = findModuleFuel( mass )
    extra_mass = fuel
    while extra_mass > 0:
        extra_fuel = findModuleFuel( extra_mass )
        if extra_fuel > 0:
            fuel += extra_fuel
        extra_mass = extra_fuel
    return fuel

def main():
    mass = pd.read_csv(r'C:\Users\anton\OneDrive\Code\AdventOfCode\20191201\mass.csv')['mass'].tolist()    
    fuel = sum( list(map( findModuleFuelComplete, mass ) ) )
    print( fuel )

if __name__ == '__main__':
    main()
