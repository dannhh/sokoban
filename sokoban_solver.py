import sys
import time
import heapq
import psutil
import os
from collections import deque
import pygame

#--------------------------------INITIAL--------------------------------#

# use to take memory used
pid = os.getpid()
ps = psutil.Process(pid)

# array to store robot, walls, storages and boxes
robot = []
walls = []
storage = []
box = []
width = 0

# Direction for robot to move, U: up; D: down; L: left; R: right
directions = {
    'U': [-1, 0],
    'R': [0, 1],
    'D': [1, 0],
    'L': [0, -1]
}

# Check if a side of game have a goal
valid_side = {
    'U' : False,
    'D' : False,
    'R' : False,
    'L' : False
}

# Starting time of game
start_time = 0

# time to check time run
out_time = 1800

# array store the moves that have been met
visited_Moves = {}

# queue to put each state to check
queue = []
dequeue = deque()

# variable to check when all boxes are in storages
check = False

#--------------------------------READ TESTCASE FILE, WRITE RESULT AND FUNCTION TO RUN--------------------------------#

# function to read testcase file
def read_file(filename):
    fulltest = []
    each_test = []
    level = []
    f = open(filename, 'r')
    for line in f:
        if line == "end":
            break
        if len(line) == 1:
            fulltest.append(each_test)
            each_test = []
        elif (line[0] == "L"):
            level.append(line)
        else:
            temp = []
            for c in line:
                if (c != '\n'):
                    temp.append(c)
            each_test.append(temp)
    f.close()
    return fulltest, level

# function to write result
def write_file(filename, cur_path, total_time, total_step, space_taken, total_state, level, algorithm):
    string_to_write = level
    string_to_write += "Algorithm " + algorithm + "\n"
    string_to_write += "Path: " + str(cur_path) + "\n"
    string_to_write += "Total time taken: " + str(total_time) + "\n"
    string_to_write += "Total steps: " + str(total_step) + "\n"
    string_to_write += "Total space taken: " + str(space_taken) + "\n"
    string_to_write += "Total state created: " + str(total_state) + "\n"
    string_to_write += "******************************************\n"
    f = open(filename, 'a')
    f.write(string_to_write)
    f.close()
#-----------------------------------------------------------------------------------------#

# function to print solution
def print_solution(cur_path, total_time, total_step, space_taken, total_state, level, algorithm):
    string_to_print = level
    string_to_print += "Algorithm " + algorithm + "\n"
    string_to_print += "Path: " + str(cur_path) + "\n"
    string_to_print += "Total time taken: " + str(total_time) + "\n"
    string_to_print += "Total steps: " + str(total_step) + "\n"
    string_to_print += "Total space taken: " + str(space_taken) + "\n"
    string_to_print += "Total state created: " + str(total_state) + "\n"

    return string_to_print
#-----------------------------------------------------------------------------------------#

# main function to run
def run(fileread, filewrite):
    wall = pygame.image.load('images/wall.png')
    floor = pygame.image.load('images/floor.png')
    boxes = pygame.image.load('images/box.png')
    box_docked = pygame.image.load('images/box_docked.png')
    worker = pygame.image.load('images/worker.png')
    worker_docked = pygame.image.load('images/worker_dock.png')
    docker = pygame.image.load('images/dock.png')
    background = 255, 226, 191
    pygame.init()      
    fulltest, list_level = read_file(fileread)
    count = 0
    
    while True:
        global robot, walls, box, storage, visited_Moves, queue, dequeue, check, width
        print("Choose testcase to run (1 -> 40), enter -1 to quit: ")
        level_choose = int(input())

        if level_choose == -1:
            break

        if level_choose < 1 or level_choose > 40:
            continue

        print("Solving testcase " + str(level_choose) + "..........")
        level = list_level[level_choose - 1]
        matrix = fulltest[level_choose - 1]
        print_Map(matrix)   # Read level and add to state array
        global start_time

        while True:
            print("Choose algorithm to run, enter 1 to run BFS, enter 2 to run A_star: ")
            algorithm_choose = int(input())
            if algorithm_choose == 1 or algorithm_choose == 2:
                break
        
        if algorithm_choose == 1:
            start_time = time.time()
            cur_path, total_time, total_step, space_taken, total_state = bfs()
            if cur_path == []:
                file = open(filewrite, 'a')
                file.write("Testcase is fail\n")
                file.close()
                write_file(filewrite, cur_path, total_time, total_step, space_taken, total_state, level, "BFS")
            else:
                write_file(filewrite, cur_path, total_time, total_step, space_taken, total_state, level, "BFS")
                print(print_solution(cur_path, total_time, total_step, space_taken, total_state, level, "BFS"))
        elif algorithm_choose == 2:
            start_time = time.time()
            cur_path, total_time, total_step, space_taken, total_state = A_star_heuristic()
            if cur_path == []:
                file = open(filewrite, 'a')
                file.write("Testcase is fail\n")
                file.close()
                write_file(filewrite, cur_path, total_time, total_step, space_taken, total_state, level, "A_star")
            else:
                write_file(filewrite, cur_path, total_time, total_step, space_taken, total_state, level, "A_star")
                print(print_solution(cur_path, total_time, total_step, space_taken, total_state, level, "A_star"))
        
        print("Done algorithm")

        count += 1

        # reassign the state of the game
        robot = []
        walls = []
        storage = []
        box = []
        width = 0
        visited_Moves = {}
        queue = []
        check = False
        dequeue = deque()

        sokoban = game(matrix)
        size = sokoban.load_size()
        screen = pygame.display.set_mode(size)
        pygame.display.init()

        print_game(sokoban.get_matrix(),screen, background, floor, wall, worker, docker, box_docked, boxes, worker_docked)
        pygame.display.update()
        time.sleep(0.5)

        cur_path = move_string(cur_path)

        for i in cur_path:
            pygame.event.pump()
            sokoban.move(i[0],i[1])
            print_game(sokoban.get_matrix(),screen, background, floor, wall, worker, docker, box_docked, boxes, worker_docked)
            pygame.display.update()
            if (sokoban.is_completed()): 
                time.sleep(0.5)
            else: 
                time.sleep(0.3)
        
        pygame.display.flip ()
        pygame.quit()
        print("Game runs successfully")

        break
    
    return count
#-----------------------------------------------------------------------------------------#

#function with own heuristic
def heuristic(box_ls,storage_ls,path):
    temp_storage = storage_ls[:]
    distance = 0
    for h in box_ls:
        dis_temp = 9999999
        temp_goal = []
        for s in temp_storage:
            a = abs(h[1] - s[1]) + abs(h[0] - s[0])
            if a < dis_temp:
                dis_temp = a
                temp_goal.append(s)
        distance += dis_temp
        temp_storage.pop(temp_storage.index(temp_goal[-1][:]))
    distance += len(path)
    return distance
#-----------------------------------------------------------------------------------------#

# function to store the map to state variables
def print_Map(matrix):	
    global width			
    i = 0										
    j = 0
    new = []
    while i < len(matrix):	
        character = matrix[i][j]
        temp = []
        if character:
            temp.append(i)
            temp.append(j)						
            if character == "#":
                new.append(1)
            if character == "@":
                robot.append(temp)
                new.append(0)
            if character == ".":
                storage.append(temp)
                new.append(0)
            if character == "$":
                box.append(temp)
                new.append(0)
            if character == "*":
                box.append(temp)
                storage.append(temp)
                new.append(0)
            if character == "+":
                robot.append(temp)
                storage.append(temp)
                new.append(0)
            if j == len(matrix[i]) - 1:
                walls.append(new)
                if len(new) > width:
                    width = len(new)
                new = []
                i += 1
                j = 0
            else:
                j += 1
                if len(new) < j:
                    new.append(0)
        else:
            break
#-----------------------------------------------------------------------------------------#

# User run file but don't provide textfile as system argument
if len(sys.argv) < 3:
    print("Please provide textfile name as system argument \n python3 sokoban_solver.py <filename> <filename>")
    exit(0)

#--------------------------------DEADLOCK DETECTION--------------------------------#
""" CHECK FOR DEADLOCK
    # DEADLOCK CASE:
    #  1. Box in corner 
    #  2. Cluster of four (at least one box)
    #  4. The box at the 1 wall-side can be moved but never reach a goal <Not test in this code>
    #  5. Two boxes are between 2 walls and they block the ends <Not test in this code>
    #  6. ...

    #  In this dfs, we just check for:
            CASE 1:
                #$   $#   #$     $#
                #$   $#    $#   #$ 
            CASE 2:
                ##   $$   #   # 
                $$   ##  $$   $$
                         #     #
            CASE 3: 
                $$
                $$
            CASE 4: 
                #$ 		$#   	 $$		$$  
                $$		$$		 #$		$#
            CASE 5: 
                $#   ##
                #S   #S    and it's rotations
"""
def check_if_goal_in_side():
    for s in storage:
        if s[0] == 1:
            valid_side['U'] = True
        if s[0] == len(walls)-2:
            valid_side['D'] = True
        if s[1] == 1:
            valid_side['L'] = True
        if s[1] == width-2:
            valid_side['R'] = True
# CHECK DEADLOCK: 
def checkDeadLock (box_list, curr_box, dir):
    temp_box_wtht_cur = []
    for box in box_list:
        if curr_box[0] != box[0] or curr_box[1] != box[1]:
            # Not a deadlock if both boxes are on goal
            if curr_box in storage and box in storage:
                continue

            # CHECK FOR CASE 1
            if box[1] == curr_box[1]:
                if walls[curr_box[0]][curr_box[1]-1]==1 or walls[curr_box[0]][curr_box[1]+1]==1:
                    if (curr_box[0]+1) == box[0] or (curr_box[0]-1) == box[0]:
                        if walls[box[0]][box[1]-1]==1 or walls[box[0]][box[1]+1]==1:
                            return True
            
            # CHECK FOR CASE 2:
            if box[0] == curr_box[0]: 
                if walls[curr_box[0]-1][curr_box[1]]==1 or walls[curr_box[0]+1][curr_box[1]]==1:
                    if (curr_box[1]+1) == box[1] or (curr_box[1]-1) == box[1]:
                        if walls[box[0]-1][box[1]]==1 or walls[box[0]+1][box[1]]==1:
                            return True
            temp_box_wtht_cur.append(box)

    # CHECK FOR CASE 3, 4, 5 (duplicated with case 1,2 in some(2) step)        
    if (dir == 'U'):  
        if curr_box[0] == 1 and valid_side['U'] == False:
            return True
      
        if [curr_box[0]-1, curr_box[1]] in temp_box_wtht_cur or walls[curr_box[0]-1][curr_box[1]] == 1: # TOP

            if [curr_box[0], curr_box[1]-1] in temp_box_wtht_cur or walls[curr_box[0]][curr_box[1]-1]: # LEFT
                if [curr_box[0]-1, curr_box[1]-1] in temp_box_wtht_cur or walls[curr_box[0]-1][curr_box[1]-1] == 1: # TOP-LEFT
                    # If boxes are in deadlock state but also in destination, they are not considered deadlock
                    if ([curr_box[0]-1, curr_box[1]] not in storage and not walls[curr_box[0]-1][curr_box[1]] 
                     or [curr_box[0], curr_box[1]-1] not in storage and not walls[curr_box[0]][curr_box[1]-1]
                     or [curr_box[0]-1, curr_box[1]-1] not in storage and not walls[curr_box[0]-1][curr_box[1]-1]):     
                        return True

            if [curr_box[0], curr_box[1]+1] in temp_box_wtht_cur or walls[curr_box[0]][curr_box[1]+1]: # RIGHT
                if [curr_box[0]-1, curr_box[1]+1] in temp_box_wtht_cur or walls[curr_box[0]-1][curr_box[1]+1] == 1: # TOP-RIGHT
                    # If boxes are in deadlock state but also in destination, they are not considered deadlock
                    if ([curr_box[0]-1, curr_box[1]] not in storage and not walls[curr_box[0]-1][curr_box[1]] 
                     or [curr_box[0], curr_box[1]+1] not in storage and not walls[curr_box[0]][curr_box[1]+1]
                     or [curr_box[0]-1, curr_box[1]+1] not in storage and not walls[curr_box[0]-1][curr_box[1]+1]):     
                        return True

    elif (dir == 'D'):
        if curr_box[0] == (len(walls) - 2) and valid_side['D'] == False:
            return True       
        if [curr_box[0]+1, curr_box[1]] in box_list or walls[curr_box[0]+1][curr_box[1]] == 1: # BOT

            if [curr_box[0], curr_box[1]-1] in box_list or walls[curr_box[0]][curr_box[1]-1]: # LEFT
                if [curr_box[0]+1, curr_box[1]-1] in box_list or walls[curr_box[0]+1][curr_box[1]-1] == 1: # BOT-LEFT
                    # If boxes are in deadlock state but also in destination, they are not considered deadlock
                    if ([curr_box[0]+1, curr_box[1]] not in storage and not walls[curr_box[0]+1][curr_box[1]] 
                     or [curr_box[0], curr_box[1]-1] not in storage and not walls[curr_box[0]][curr_box[1]-1]
                     or [curr_box[0]+1, curr_box[1]-1] not in storage and not walls[curr_box[0]+1][curr_box[1]-1]):     
                        return True

            if [curr_box[0], curr_box[1]+1] in box_list or walls[curr_box[0]][curr_box[1]+1]: # RIGHT
                if [curr_box[0]+1, curr_box[1]+1] in box_list or walls[curr_box[0]+1][curr_box[1]+1] == 1: # BOT-RIGHT
                    # If boxes are in deadlock state but also in destination, they are not considered deadlock
                    if ([curr_box[0]+1, curr_box[1]] not in storage and not walls[curr_box[0]+1][curr_box[1]] 
                     or [curr_box[0], curr_box[1]+1] not in storage and not walls[curr_box[0]][curr_box[1]+1]
                     or [curr_box[0]+1, curr_box[1]+1] not in storage and not walls[curr_box[0]+1][curr_box[1]+1]):     
                        return True

    elif (dir == 'R'):        
        if curr_box[1] == (width - 2) and valid_side['R'] == False:
            return True
        if [curr_box[0], curr_box[1]+1] in temp_box_wtht_cur or walls[curr_box[0]][curr_box[1]+1] == 1: # RIGHT

            if [curr_box[0]-1, curr_box[1]] in temp_box_wtht_cur or walls[curr_box[0]-1][curr_box[1]]: # TOP
                if [curr_box[0]-1, curr_box[1]+1] in temp_box_wtht_cur or walls[curr_box[0]-1][curr_box[1]+1] == 1: # RIGHT-TOP
                    if ([curr_box[0], curr_box[1]+1] not in storage and not walls[curr_box[0]][curr_box[1]+1] 
                     or [curr_box[0]-1, curr_box[1]] not in storage and not walls[curr_box[0]-1][curr_box[1]]
                     or [curr_box[0]-1, curr_box[1]+1] not in storage and not walls[curr_box[0]-1][curr_box[1]+1]):     
                        return True

            if [curr_box[0]+1, curr_box[1]] in temp_box_wtht_cur or walls[curr_box[0]+1][curr_box[1]]: # BOT
                if [curr_box[0]+1, curr_box[1]+1] in temp_box_wtht_cur or walls[curr_box[0]+1][curr_box[1]+1] == 1: # RIGHT-BOT
                    if ([curr_box[0], curr_box[1]+1] not in storage and not walls[curr_box[0]][curr_box[1]+1] 
                     or [curr_box[0]+1, curr_box[1]] not in storage and not walls[curr_box[0]+1][curr_box[1]]
                     or [curr_box[0]+1, curr_box[1]+1] not in storage and not walls[curr_box[0]+1][curr_box[1]+1]):     
                        return True

    elif (dir == 'L'):       
        if curr_box[1] == 1 and valid_side['L'] == False:
            return True 
        if [curr_box[0], curr_box[1]-1] in temp_box_wtht_cur or walls[curr_box[0]][curr_box[1]-1] == 1: # LEFT

            if [curr_box[0]-1, curr_box[1]] in temp_box_wtht_cur or walls[curr_box[0]-1][curr_box[1]]: # TOP
                if [curr_box[0]-1, curr_box[1]-1] in temp_box_wtht_cur or walls[curr_box[0]-1][curr_box[1]-1] == 1: # LEFT-TOP
                    if ([curr_box[0], curr_box[1]-1] not in storage and not walls[curr_box[0]][curr_box[1]-1] 
                     or [curr_box[0]-1, curr_box[1]] not in storage and not walls[curr_box[0]-1][curr_box[1]]
                     or [curr_box[0]-1, curr_box[1]-1] not in storage and not walls[curr_box[0]-1][curr_box[1]-1]):     
                        return True

            if [curr_box[0]+1, curr_box[1]] in temp_box_wtht_cur or walls[curr_box[0]+1][curr_box[1]]: # BOT
                if [curr_box[0]+1, curr_box[1]-1] in temp_box_wtht_cur or walls[curr_box[0]+1][curr_box[1]-1] == 1: # LEFT-BOT
                    if ([curr_box[0], curr_box[1]-1] not in storage and not walls[curr_box[0]][curr_box[1]-1] 
                     or [curr_box[0]+1, curr_box[1]] not in storage and not walls[curr_box[0]+1][curr_box[1]]
                     or [curr_box[0]+1, curr_box[1]-1] not in storage and not walls[curr_box[0]+1][curr_box[1]-1]):     
                        return True    
    return False

#--------------------------------MOVE FUNCTION--------------------------------#

# function to move robot and boxes
def move_a_star(point_robot_move, direction_move, path, temp_box_list):
    global check
    # list store position of boxes
    box_list = temp_box_list[:]
    
    # list will store the position of robot and boxes
    temp_pos = []
    
    # path from start to now
    cur_path = path[:]
    cur_path.append(direction_move) # add next move to path
    
    if point_robot_move in box_list:
        # get index of the box that robot hit
        idx = box_list.index(point_robot_move)
        
        # get the new position if the robot move box 
        temp_pos_of_box = [x + y for x, y in zip(point_robot_move, directions[direction_move])]
        
        if walls[temp_pos_of_box[0]][temp_pos_of_box[1]] == 0 and temp_pos_of_box not in box_list:
            # update the position of the box in the list
            box_list[idx] = temp_pos_of_box
            
            # sort to avoid duplicate
            box_list.sort()

            if checkDeadLock(box_list, box_list[idx], direction_move) != True:
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
                    dis_estimate = heuristic(box_list, storage, cur_path)
                    temp_pos.append(str(dis_estimate))

                    # put to queue follow the min heap with the min heuristic distance
                    heapq.heappush(queue, (temp_pos[-1][:], temp_pos[:-1]))

            # check if goal is met
            if set(map(tuple, box_list)) == set(map(tuple, storage)):
                stop = time.time()
                total_time = stop - start_time
                check = True
            
                return cur_path, total_time, len(cur_path), ps.memory_info()[0]/(1024*1024)
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
            dis_estimate = heuristic(box_list, storage, cur_path)
            temp_pos.append(str(dis_estimate))

            # put to queue follow the min heap with the min heuristic distance
            heapq.heappush(queue, (temp_pos[-1][:], temp_pos[:-1]))

        # check if goal is met
        if set(map(tuple, box_list)) == set(map(tuple, storage)):
            stop = time.time()
            total_time = stop - start_time
            
            check = True

            return cur_path, total_time, len(cur_path), ps.memory_info()[0]/(1024*1024)
    return 0,0,0,0
#-----------------------------------------------------------------------------------------#

# initialize start time
start_time = time.time()

#--------------------------------A* ALGORITHM--------------------------------#

# function for A* algorithm
def A_star_heuristic():

    check_if_goal_in_side()
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
    count_to_check = 0
    while queue:    # if queue is empty, algorithm done
        count_to_check += 1
        if count_to_check % 100 == 0:
            current_time = time.time()
            time_run = current_time - start_time
            if time_run > out_time:
                return [], time_run, 0, 0, count
        
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


        if walls[U[0]][U[1]] == 0:
            cur_path, total_time, total_step, space_taken = move_a_star(U, 'U', temp_path, temp_box_list)
            count=count+1
            if check == True:
                break
        if walls[D[0]][D[1]] == 0:
            cur_path, total_time, total_step, space_taken = move_a_star(D, 'D', temp_path, temp_box_list)
            count=count+1
            if check == True:
                break
        if walls[R[0]][R[1]] == 0:   
            cur_path, total_time, total_step, space_taken = move_a_star(R, 'R', temp_path, temp_box_list)
            count=count+1
            if check == True:
                break
        if walls[L[0]][L[1]] == 0:
            cur_path, total_time, total_step, space_taken = move_a_star(L, 'L', temp_path, temp_box_list)
            count=count+1
            if check == True:
                break

        
        
    return cur_path, total_time, total_step, space_taken, count
#-----------------------------------------------------------------------------------------#

# function for movement of a box
def move_bfs(point,dir,path,temp_box_list):
    global check
    # Store temp box list
    box_list = temp_box_list[:] 
    temp_append = []
    cur_path = path[:]
    # Store current path
    cur_path.append(dir)

    # Current robot position is a box, so push the box if possible
    if point in box_list:
        # Find index and move this box to new position
        ind = box_list.index(point)
        temp_box = [x + y for x, y in zip(point, directions[dir])]
        # Check new possition of this box is valid
        if temp_box not in box_list and walls[temp_box[0]][temp_box[1]] == 0:
            box_list[ind]=[x + y for x, y in zip(point, directions[dir])]

            if checkDeadLock(box_list, box_list[ind], dir) != True:
                box_list.sort()                
                # Sort to avoid duplicate. Ex: [1,3,2] -> [1,2,3] same as [1,2,3]
                temp_append.append(point)
                temp_append.append(box_list)
                
                # check if any status has passed
                idx = point[0]*10 + point[1]
                counter = 0
                if idx in visited_Moves:
                    for k in visited_Moves[idx]:
                        if(k == temp_append):
                            counter = counter + 1

                # If this state havent passed, add (state + predicted distance) to queue
                if counter == 0:
                    temp_append.append(cur_path)
                    dequeue.append(temp_append)

            # check if goal
            if set(map(tuple,box_list))==set(map(tuple,storage)):
                check = True
                stop = time.time()
                total_time=stop-start_time

                return cur_path, total_time, len(cur_path), ps.memory_info()[0]/(1024*1024)

    else:
        # Sort to avoid duplicate. Ex: [1,3,2] -> [1,2,3] same as [1,2,3]
        box_list.sort()
        temp_append.append(point)
        temp_append.append(box_list)
        
        # check if any status has passed
        idx = point[0]*10 + point[1]
        counter = 0
        if idx in visited_Moves:
            for k in visited_Moves[idx]:
                if(k == temp_append):
                    counter = counter + 1
        # If this state havent passed, add (state+predicted distance)to queue
        if counter == 0:
            temp_append.append(cur_path)
            dequeue.append(temp_append)
    return 0,0,0,0
#-----------------------------------------------------------------------------------------#

#--------------------------------BFS ALGORITHM--------------------------------#

# bfs function
def bfs():
    check_if_goal_in_side()
    # State store current position of current player and box
    node=[]
    node.append(robot[0])
    node.append(box)    
    path=[]
    node.append(path)
    # Add current node = state+path to dequeue
    dequeue.append(node)

    count = 0
    count_to_check = 0
    while True:
        if len(dequeue) == 0:
            print ("Can not find a solution")
            return

        count_to_check += 1
        if count_to_check % 100 == 0:
            current_time = time.time()
            time_run = current_time - start_time
            if time_run > out_time:
                return [], time_run, 0, 0, count

        # pop recent added node
        node = dequeue.popleft()
        state = node[:-1]
        current_player = node[0]
        
        # Dictionary visited contain key: player position
        # and value: corresponding [states] 
        # state: [player, box1, box2]
        idx = current_player[0]*10 + current_player[1] 

        # check if there is a duplicate state
        if idx in visited_Moves:   
            cnt = 0   
            for pos in visited_Moves[idx]:
                if(state == pos):
                    cnt = 1
                    break       
            if(cnt == 0):
                visited_Moves[idx].append(state)            
        else:
            visited_Moves[idx] = []
            visited_Moves[idx].append(state)            

        # temp_path and current box list
        temp_path = node[-1][:]
        temp_box_list = node[1]

        # determine position of player after each possible move
        U = [x + y for x, y in zip(current_player, directions['U'])]
        D = [x + y for x, y in zip(current_player, directions['D'])]
        R = [x + y for x, y in zip(current_player, directions['R'])]
        L = [x + y for x, y in zip(current_player, directions['L'])]
        
        # Check current player's position 
        # Add a state to dequeue if satifies 
        # 1. the player does not move into the wall 
        # 2. the player does not push a box that is already close to the wall towards the wall
        # 3. the player does not push 2 boxes at a time
        # 4. Check deadlock
        # 5. Visited list does not contain this state
        # Final, check if the goal status is reached or not
        if walls[U[0]][U[1]] == 0:
            cur_path, total_time, total_step, space_taken = move_bfs(U, 'U', temp_path, temp_box_list)
            count=count+1
            if check == True:
                break
        if walls[D[0]][D[1]] == 0:
            cur_path, total_time, total_step, space_taken = move_bfs(D, 'D', temp_path, temp_box_list)
            count=count+1
            if check == True:
                break
        if walls[R[0]][R[1]] == 0:   
            cur_path, total_time, total_step, space_taken = move_bfs(R, 'R', temp_path, temp_box_list)
            count=count+1
            if check == True:
                break
        if walls[L[0]][L[1]] == 0:
            cur_path, total_time, total_step, space_taken = move_bfs(L, 'L', temp_path, temp_box_list)
            count=count+1
            if check == True:
                break
    return cur_path, total_time, total_step, space_taken, count
#-----------------------------------------------------------------------------------------#

# demo game
class game:

    def is_valid_value(self,char):
        if ( char == ' ' or #floor
            char == '#' or #wall
            char == '@' or #worker on floor
            char == '.' or #dock
            char == '*' or #box on dock
            char == '$' or #box
            char == '+' ): #worker on dock
            return True
        else:
            return False

    def __init__(self,matrix):
        self.matrix = matrix

    def load_size(self):
        x = 0
        y = len(self.matrix)
        for row in self.matrix:
            if len(row) > x:
                x = len(row)
        return (x * 32, y * 32)

    def get_matrix(self):
        return self.matrix

    def get_content(self,x,y):
        return self.matrix[y][x]

    def set_content(self,x,y,content):
        if self.is_valid_value(content):
            self.matrix[y][x] = content
        else:
            print ("ERROR: Value '"+content+"' to be added is not valid")

    def worker(self):
        x = 0
        y = 0
        for row in self.matrix:
            for pos in row:
                if pos == '@' or pos == '+': # worker on floor or worker on dock
                    return (x, y, pos)
                else:
                    x = x + 1
            y = y + 1
            x = 0

    def can_move(self,x,y):
        return self.get_content(self.worker()[0]+x,self.worker()[1]+y) not in ['#','*','$']

    def next(self,x,y):
        return self.get_content(self.worker()[0]+x,self.worker()[1]+y)

    def can_push(self,x,y):
        return (self.next(x,y) in ['*','$'] and self.next(x+x,y+y) in [' ','.'])

    def is_completed(self):
        for row in self.matrix:
            for cell in row:
                if cell == '$':
                    return False
        return True

    def move_box(self,x,y,a,b):
        #        (x,y) -> move to do
        #        (a,b) -> box to move
        current_box = self.get_content(x,y)
        future_box = self.get_content(x+a,y+b)
        if current_box == '$' and future_box == ' ':
            self.set_content(x+a,y+b,'$')
            self.set_content(x,y,' ')
        elif current_box == '$' and future_box == '.':
            self.set_content(x+a,y+b,'*')
            self.set_content(x,y,' ')
        elif current_box == '*' and future_box == ' ':
            self.set_content(x+a,y+b,'$')
            self.set_content(x,y,'.')
        elif current_box == '*' and future_box == '.':
            self.set_content(x+a,y+b,'*')
            self.set_content(x,y,'.')

    def move(self,x,y):
        if self.can_move(x,y):
            current = self.worker()
            future = self.next(x,y)
            if current[2] == '@' and future == ' ':
                self.set_content(current[0]+x,current[1]+y,'@')
                self.set_content(current[0],current[1],' ')
            elif current[2] == '@' and future == '.':
                self.set_content(current[0]+x,current[1]+y,'+')
                self.set_content(current[0],current[1],' ')
            elif current[2] == '+' and future == ' ':
                self.set_content(current[0]+x,current[1]+y,'@')
                self.set_content(current[0],current[1],'.')
            elif current[2] == '+' and future == '.':
                self.set_content(current[0]+x,current[1]+y,'+')
                self.set_content(current[0],current[1],'.')
        elif self.can_push(x,y):
            current = self.worker()
            future = self.next(x,y)
            future_box = self.next(x+x,y+y)
            if current[2] == '@' and future == '$' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'@')
            elif current[2] == '@' and future == '$' and future_box == '.':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'@')
            elif current[2] == '@' and future == '*' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'+')
            elif current[2] == '@' and future == '*' and future_box == '.':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'+')
            elif current[2] == '+' and future == '$' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'@')
            elif current[2] == '+' and future == '$' and future_box == '.':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'@') # + => @
            elif current[2] == '+' and future == '*' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'+')
            elif current[2] == '+' and future == '*' and future_box == '.':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'+')
#-----------------------------------------------------------------------------------------#

def print_game(matrix, screen, background, floor, wall, worker, docker, box_docked, box, worker_docked):
        screen.fill(background)
        x = 0
        y = 0
        for row in matrix:
           for char in row:
                if char == ' ': #floor
                    screen.blit(floor,(x,y))
                elif char == '#': #wall
                    screen.blit(wall,(x,y))
                elif char == '@': #worker on floor
                    screen.blit(worker,(x,y))
                elif char == '.': #dock
                    screen.blit(docker,(x,y))
                elif char == '*': #box on dock
                    screen.blit(box_docked,(x,y))
                elif char == '$': #box
                    screen.blit(box,(x,y))
                elif char == '+': #worker on dock
                    screen.blit(worker_docked,(x,y))
                x = x + 32
           x = 0
           y = y + 32
#-----------------------------------------------------------------------------------------#

def move_string(moves):
    movesssss = []
    for i in moves: 
        if i == "L":
            movesssss.append([-1, 0])
        elif i == "R":
            movesssss.append([1, 0])
        elif i == "U":
            movesssss.append([0, -1])
        else:
            movesssss.append([0, 1])
    return movesssss
#-----------------------------------------------------------------------------------------#

#--------------------------------RUN THE GAME WITH TWO INPUT FILES--------------------------------#
run(sys.argv[1], sys.argv[2])

#----------------------------------------- END ----------------------------------------------#