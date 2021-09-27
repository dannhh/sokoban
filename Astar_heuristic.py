import sys
import numpy as np
from collections import deque
import timeit
import heapq

# array to store robot, walls, storages and boxes
robot=[]
walls=[]
storage=[]
box=[]

# Direction for robot to move, U: up; D: down; L: left; R: right
directions={
    'U': [-1, 0],
    'R': [0, 1],
    'D': [1, 0],
    'L': [0, -1]
}

# Starting time of game
start_time=0

#function with own heuristic

def heuristic(box_ls,storage_ls,path,point_ls):
     distance=[]
     p=point_ls[:]
     for h in box_ls:
         dis_h_p=sum(abs(np.subtract(h,p)))
         dis_temp=[]
         for s in storage_ls:
             a=sum(abs(np.subtract(h,s)))+dis_h_p
             dis_temp.append(a)
         distance.append(min(dis_temp))
     dis_value=sum(distance)+len(path)
     return dis_value

# function for reading test-case file
def print_Map(filename):
    f = open(filename, 'r')					
    i = 0										
    j = 0
    new = []
    while True:	
        character = f.read(1)
        temp = []
        if character:
            temp.append(i)
            temp.append(j)						
            if character == "#":
                walls.append(temp)
            if character == "@":
                robot.append(temp)
            if character == ".":
                storage.append(temp)
            if character == "$":
                box.append(temp)
            if character == "*":
                box.append(temp)
                storage.append(temp)
            if character == "+":
                robot.append(temp)
                storage.append(temp)
            if character == "\n":
                i += 1
                j = 0
            else:
                j += 1
        else:
            break

# User run file but don't provide textfile as system argument
if len(sys.argv) < 2:
    print("Please provide textfile name as system argument \n python3 Astar_heuristic.py <filename>")
    exit(0)

print_Map(sys.argv[1])

# array store the moves that have been met
visited_Moves = {}

# queue to put each state to check
queue = []

# textfile doesn't follow the format
if len(robot) == 0 or len(box) == 0 or len(storage) == 0 or len(walls) == 0:
    print("please provide the textfile in write format Walls : # \n storage : . \n box : $ \n robot : @ \n box on storage : * \n robot on storage : + \n should include walls,storage,box,robot")
    exit(0)

# function to move robot and boxes
def move(point_robot_move, direction_move, path, temp_box_list):
    # list store position of boxes
    box_list = temp_box_list[:]
    
    # list will store the position of robot and boxes
    temp_pos = []
    
    # path from start to now
    cur_path = path[:]
    cur_path.append(direction_move) # add next move to path
    if point_robot_move not in walls:
        if point_robot_move in box_list:
            # get index of the box that robot hit
            idx = box_list.index(point_robot_move)
            
            # get the new position if the robot move box 
            temp_pos_of_box = [x + y for x, y in zip(point_robot_move, directions[direction_move])]
            
            if temp_pos_of_box not in walls and temp_pos_of_box not in box_list:
                # update the position of the box in the list
                box_list[idx] = temp_pos_of_box
                
                # sort to avoid duplicate
                box_list.sort()

                # add the new position of robot and boxes to temp_pos
                temp_pos.append(point_robot_move)
                for i in box_list:
                    temp_pos.append(i)
                
                # check if the new state has been passed
                idx = point_robot_move[0]*10 + point_robot_move[1]
                counter = 0
                
                if idx in visited_Moves:
                    for k in visited_Moves[idx]:
                        if k == temp_pos:
                            counter = counter + 1
                
                # if this state hasn't been passed, add to queue
                if counter == 0:
                    temp_pos.append(cur_path)
                    dis_estimate = heuristic(box_list, storage, cur_path, point_robot_move)
                    temp_pos.append(str(dis_estimate))

                    # put to queue follow the min heap with the min heuristic distance
                    heapq.heappush(queue, (temp_pos[-1][:], temp_pos[:-1]))

                # check if goal is met
                if set(map(tuple, box_list)) == set(map(tuple, storage)):
                    stop = timeit.default_timer()
                    total_time = stop - start_time
                    
                    print("Solution found")
                    print(cur_path)
                    print("Total time taken: ")
                    print(total_time)
                    print("Total steps take: ")
                    print(len(cur_path))

                    with open('C:/Users/Acer/Desktop/HK211/NMAI/Ass1/thamkhao/result.txt', 'a') as f:
                        for i in cur_path:
                            f.write(i)
                
                    exit()
        else:
            temp_pos.append(point_robot_move)
            box_list.sort()
            for i in box_list:
                temp_pos.append(i)

            # check if the new state has been passed
            idx = point_robot_move[0]*10 + point_robot_move[1]
            counter = 0
            
            if idx in visited_Moves:
                for k in visited_Moves[idx]:
                    if k == temp_pos:
                        counter = counter + 1
            # if this state hasn't been passed, add to queue
            if counter == 0:
                temp_pos.append(cur_path)
                dis_estimate = heuristic(box_list, storage, cur_path, point_robot_move)
                temp_pos.append(str(dis_estimate))

                # put to queue follow the min heap with the min heuristic distance
                heapq.heappush(queue, (temp_pos[-1][:], temp_pos[:-1]))

            # check if goal is met
            if set(map(tuple, box_list)) == set(map(tuple, storage)):
                stop = timeit.default_timer()
                total_time = stop - start_time
                
                print("Solution found")
                print(cur_path)
                print("Total time taken: ")
                print(total_time)
                print("Total steps take: ")
                print(len(cur_path))

                with open('C:/Users/Acer/Desktop/HK211/NMAI/Ass1/thamkhao/result.txt', 'a') as f:
                    for i in cur_path:
                        f.write(i)

                exit()

# direction to move
move_up = 'U'
move_down = 'D'
move_left = 'L'
move_right = 'R'

# function for A* algorithm
def A_star_heuristic():
    
    # initialize start time
    start_time = timeit.default_timer()
    
    # temp queue to store
    temp_queue = []
    
    initial_pos = robot[0]
    temp_queue.append(initial_pos)
    
    for i in box:
        temp_queue.append(i)
    
    path = []
    
    temp_queue.append(path)
    
    # initial h(n)
    temp_queue.append(str(0))

    # put all items of temp queue to queue
    heapq.heappush(queue, (temp_queue[-1][:], temp_queue[:-1]))
    count = 0
    while queue:    # if queue is empty, algorithm done
        
        # create the temp box list
        temp_box_list = []
        
        # create list of visited move to add
        visited_moves_add = []
        
        # take the first item of the queue
        temp_list = heapq.heappop(queue)

        # take the list consists of robot position, boxes position and path
        position_list = temp_list[1]
        
        # take the position of robot
        robot_position = position_list[0]
        
        # take the visited move of robot and boxes
        visited_moves_add = position_list[:-1]
        
        # Dictionary visited contain key: robot position
        # and value: corresponding [states] 
        # state: [robot, box1, box2]
        idx = robot_position[0]*10 + robot_position[1]

        # check if there is a duplicate state
        if idx in visited_Moves:
            counter = 0
            for pos in visited_Moves[idx]:
                if visited_moves_add == pos:
                    counter = 1
                    break
            if counter == 0:
                visited_Moves[idx].append(visited_moves_add)
        else:
            visited_Moves[idx] = []
            visited_Moves[idx].append(visited_moves_add)

        # take the path
        temp_path = position_list[-1][:]

        # take position of boxes
        temp_box_list = position_list[1: -1]

        # 4 possible directions to move [row, col]
        U = [x + y for x, y in zip(robot_position, directions['U'])]
        D = [x + y for x, y in zip(robot_position, directions['D'])]
        R = [x + y for x, y in zip(robot_position, directions['R'])]
        L = [x + y for x, y in zip(robot_position, directions['L'])]

        move(U, move_up, temp_path, temp_box_list)
        move(D, move_down, temp_path, temp_box_list)
        move(R, move_right, temp_path, temp_box_list)
        move(L, move_left, temp_path, temp_box_list)
        
        count=count+1
        
        if not queue:
            print("Solution not found")
            exit()

A_star_heuristic()
