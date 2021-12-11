from SokobanQLearning import TrainResult
from sokoban import Game
from random import Random
from iqtable import QTable
from iqtable import CTable
import os
import sys
from copy import deepcopy
import time

quiet = 0
print_Q_exit = False
print_Q_success = False
print_Q_failure = False
print_Q_exit = False

board_map = {'.': ' ','*': '@', '$': '.', '&': '$'}
path_map = {'Left': 'L', 'Right': 'R', 'Up': 'U', 'Down': 'D'}

def RunAlgorithm(maze):
    interrupted = False
    _random = Random()
    game = Game(float("inf"), deepcopy(maze))
    PrintableQTable = QTable()
    PrintableCTable = CTable()
    trainResult = TrainResult(game.GetState(), PrintableQTable.Get(game.GetState()))
    while not interrupted and (quiet-1 > 1):
        print("in while")
        trainResult.Train(_random, game, PrintableQTable, PrintableCTable, 0.05, 0.5, 1.0, 1.0, 0.5, 50.0, 1000.0, 1000.0)

    if interrupted:
        print("\n")
        if (print_Q_exit):
            PrintableQTable.Print(4,12)
        return True

    trainResult.Train(_random, game, PrintableQTable, PrintableCTable, 0.05, 0.5, 1.0, 1.0, 0.5, 50.0, 1000.0, 1000.0) if quiet>=0 else TrainResult(game.GetState(), PrintableQTable.Get(game.GetState()))

    num_of_successes = 0
    while (True):
        os.system('cls' if os.name == 'nt' else 'clear')
        maze = game.GetMazeString()
        # ifdef
        print()
        for key, value in board_map.items():
            maze = maze.replace(key, value)
        print(maze)
        print()
        print("Time: ", game.GetTimeElapsed())
        print()
        print("State: 0x", hex(game.GetState()))
        print("Printing QTable")
        PrintableQTable.PrintHeader()
        PrintableQTable.PrintStateRow(game.GetState())
        print()
        if game.GetSucceeded():
            print("Succeeded!")
            if print_Q_success:
                print("\n")
                PrintableQTable.Print()
            num_of_successes += 1
            if num_of_successes >= 1:
                new_path = []
                for i in game.getPathToGoal():
                    new_path.append(i.replace(i, path_map[i]))
                print("Path to goal: ", new_path)
                break
        elif game.GetFailed():
            print("Failed!")
            if print_Q_failure:
                print("\n")
                PrintableQTable.Print()

        trainResult.Train(_random, game, PrintableQTable, PrintableCTable, 0.05, 0.5, 1.0, 1.0, 0.5, 50.0, 1000.0, 1000.0)
    
    if print_Q_exit:
        print("\n")
        PrintableQTable.Print()
    return True

    
def main():
    start_time = time.time()
    file = open(sys.argv[1])
    rowsCol = file.readline().split(" ")
    rows, cols = (int(rowsCol[0]), int(rowsCol[1]))
    arr = [["." for x in range(cols)] for y in range(rows)]

    # Walls
    walls = file.readline().split(" ")
    j=1
    for i in range(int(walls[0])):
        arr[int(walls[j])-1][int(walls[j+1])-1] = "#"
        j +=2

    # Boxes
    boxes = file.readline().split(" ")
    j=1
    for i in range(int(boxes[0])):
        arr[int(boxes[j])-1][int(boxes[j+1])-1] = "&"
        j +=2

    # Storage Locations
    strorageLocations = file.readline().split(" ")
    j=1
    for i in range(int(strorageLocations[0])):
        if arr[int(strorageLocations[j])-1][int(strorageLocations[j+1])-1] == "&":
            arr[int(strorageLocations[j])-1][int(strorageLocations[j+1])-1] = "G"
        else:
            arr[int(strorageLocations[j])-1][int(strorageLocations[j+1])-1] = "$"
        j +=2

    # Player Location
    playerLocation = file.readline().split(" ")
    if arr[int(playerLocation[0])-1][int(playerLocation[1])-1] == "$":
        arr[int(playerLocation[0])-1][int(playerLocation[1])-1] = "+"
    else:
        arr[int(playerLocation[0])-1][int(playerLocation[1])-1] = "*"

    # Concatenating
    maze = ""
    for i in range(rows):
        for j in range(cols):
            maze += arr[i][j]
        if(i != rows-1):
            maze += "\n"

    file.close()
    RunAlgorithm(maze)

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
