import sys
import psutil, os
from collections import deque
import timeit

pid = os.getpid()
ps = psutil.Process(pid)    
# =============================== INITIAL =====================================
# four component of sokoban game
wall   = []
player = []
goal   = []
box    = []
width  = 0
# Visited is stored as dict
visited = {}

# queue store as dequeue
queue = deque()

# direction
directions = {
    'U' : [-1, 0],
    'R' : [0, 1],
    'L' : [0, -1],
    'D' : [1, 0]
}
# Check if a side of game have a goal
valid_side = {
    'U' : False,
    'D' : False,
    'R' : False,
    'L' : False
}
# start_time to store time start
start_time = 0

# =============================== READ FILE ===================================
# Require 2 argument: <file solution>.py + <file test>.txt
# if len(sys.argv) < 2:
#     print("\nMiss argument! Please provide: \n python(3) <filename>.py <filetest.txt>\n")
#     exit(0)
    
# Read the test case
def print_char(filename):
    f = open(filename, 'r')
    i = 0
    j = 0
    new = []
    width = 0
    while True:
        char=f.read(1)		
        temp = []                
        if char: 
            temp.append(i)
            temp.append(j)
            if char == "#":
                new.append(1)
            elif char == "@":
                new.append(0)
                player.append(temp)
            elif char == ".":
                new.append(0)
                goal.append(temp)
            elif char == "$":
                new.append(0)
                box.append(temp)
            elif char == "*":
                new.append(0)
                box.append(temp)
                goal.append(temp)
            elif char == "+":
                new.append(0)
                player.append(temp)
                goal.append(temp)
            if char == "\n":
                j=0
                wall.append(new)
                if(len(new) > width):
                    width = len(new)
                new = []
                i=i+1
            else:               
                j=j+1
                if len(new) < j:
                    new.append(0)
        else:
            break

# Read file here
print_char(sys.argv[1])

# Return if file test have wrong format
if len(player) == 0 or len(box) == 0 or len(goal) == 0 or len(wall) == 0:
    print('''\nMiss infomation: Your <test file> must follow this notation:
 *Wall: O \n *Goal: S \n *Box: B \n *Player: R \n Box on goal: . \n Player on goal: $\n''')
    exit(0)

# =========================== MOVEMENT DEFINITION =============================
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
    for g in goal:
        if g[0] == 1:
            valid_side['U'] = True
        if g[0] == len(wall)-2:
            valid_side['D'] = True
        if g[1] == 1:
            valid_side['L'] = True
        if g[1] == width-2:
            valid_side['R'] = True
# CHECK DEADLOCK: 
def checkDeadLock (box_list, curr_box, dir):
    temp_box_wtht_cur = []
    for box in box_list:
        if curr_box[0] != box[0] or curr_box[1] != box[1]:
            # Not a deadlock if both boxes are on goal
            if curr_box in goal and box in goal:
                continue

            # CHECK FOR CASE 1
            if box[1] == curr_box[1]:
                if wall[curr_box[0]][curr_box[1]-1]==1 or wall[curr_box[0]][curr_box[1]+1]==1:
                    if (curr_box[0]+1) == box[0] or (curr_box[0]-1) == box[0]:
                        if wall[box[0]][box[1]-1]==1 or wall[box[0]][box[1]+1]==1:
                            return True
            
            # CHECK FOR CASE 2:
            if box[0] == curr_box[0]: 
                if wall[curr_box[0]-1][curr_box[1]]==1 or wall[curr_box[0]+1][curr_box[1]]==1:
                    if (curr_box[1]+1) == box[1] or (curr_box[1]-1) == box[1]:
                        if wall[box[0]-1][box[1]]==1 or wall[box[0]+1][box[1]]==1:
                            return True
            temp_box_wtht_cur.append(box)

    # CHECK FOR CASE 3, 4, 5 (duplicated with case 1,2 in some(2) step)        
    if (dir == 'U'):     
        if curr_box[0] == 1 and valid_side['U'] == False: 
            return True
  
        if [curr_box[0]-1, curr_box[1]] in temp_box_wtht_cur or wall[curr_box[0]-1][curr_box[1]] == 1: # TOP

            if [curr_box[0], curr_box[1]-1] in temp_box_wtht_cur or wall[curr_box[0]][curr_box[1]-1]: # LEFT
                if [curr_box[0]-1, curr_box[1]-1] in temp_box_wtht_cur or wall[curr_box[0]-1][curr_box[1]-1] == 1: # TOP-LEFT
                    # If boxes are in deadlock state but also in destination, they are not considered deadlock
                    if ([curr_box[0]-1, curr_box[1]] not in goal and not wall[curr_box[0]-1][curr_box[1]] 
                     or [curr_box[0], curr_box[1]-1] not in goal and not wall[curr_box[0]][curr_box[1]-1]
                     or [curr_box[0]-1, curr_box[1]-1] not in goal and not wall[curr_box[0]-1][curr_box[1]-1]):     
                        return True

            if [curr_box[0], curr_box[1]+1] in temp_box_wtht_cur or wall[curr_box[0]][curr_box[1]+1]: # RIGHT
                if [curr_box[0]-1, curr_box[1]+1] in temp_box_wtht_cur or wall[curr_box[0]-1][curr_box[1]+1] == 1: # TOP-RIGHT
                    # If boxes are in deadlock state but also in destination, they are not considered deadlock
                    if ([curr_box[0]-1, curr_box[1]] not in goal and not wall[curr_box[0]-1][curr_box[1]] 
                     or [curr_box[0], curr_box[1]+1] not in goal and not wall[curr_box[0]][curr_box[1]+1]
                     or [curr_box[0]-1, curr_box[1]+1] not in goal and not wall[curr_box[0]-1][curr_box[1]+1]):     
                        return True

    elif (dir == 'D'):
        if curr_box[0] == (len(wall)-2) and valid_side['D'] == False:
            return True      
        if [curr_box[0]+1, curr_box[1]] in temp_box_wtht_cur or wall[curr_box[0]+1][curr_box[1]] == 1: # BOT

            if [curr_box[0], curr_box[1]-1] in temp_box_wtht_cur or wall[curr_box[0]][curr_box[1]-1]: # LEFT
                if [curr_box[0]+1, curr_box[1]-1] in temp_box_wtht_cur or wall[curr_box[0]+1][curr_box[1]-1] == 1: # BOT-LEFT
                    # If boxes are in deadlock state but also in destination, they are not considered deadlock
                    if ([curr_box[0]+1, curr_box[1]] not in goal and not wall[curr_box[0]+1][curr_box[1]] 
                     or [curr_box[0], curr_box[1]-1] not in goal and not wall[curr_box[0]][curr_box[1]-1]
                     or [curr_box[0]+1, curr_box[1]-1] not in goal and not wall[curr_box[0]+1][curr_box[1]-1]):     
                        return True

            if [curr_box[0], curr_box[1]+1] in temp_box_wtht_cur or wall[curr_box[0]][curr_box[1]+1]: # RIGHT
                if [curr_box[0]+1, curr_box[1]+1] in temp_box_wtht_cur or wall[curr_box[0]+1][curr_box[1]+1] == 1: # BOT-RIGHT
                    # If boxes are in deadlock state but also in destination, they are not considered deadlock
                    if ([curr_box[0]+1, curr_box[1]] not in goal and not wall[curr_box[0]+1][curr_box[1]] 
                     or [curr_box[0], curr_box[1]+1] not in goal and not wall[curr_box[0]][curr_box[1]+1]
                     or [curr_box[0]+1, curr_box[1]+1] not in goal and not wall[curr_box[0]+1][curr_box[1]+1]):     
                        return True

    elif (dir == 'R'): 
        if curr_box[1] == (width-2) and valid_side['R'] == False:
            return True       
        if [curr_box[0], curr_box[1]+1] in temp_box_wtht_cur or wall[curr_box[0]][curr_box[1]+1] == 1: # RIGHT

            if [curr_box[0]-1, curr_box[1]] in temp_box_wtht_cur or wall[curr_box[0]-1][curr_box[1]]: # TOP
                if [curr_box[0]-1, curr_box[1]+1] in temp_box_wtht_cur or wall[curr_box[0]-1][curr_box[1]+1] == 1: # RIGHT-TOP
                    # If boxes are in deadlock state but also in destination, they are not considered deadlock
                    if ([curr_box[0], curr_box[1]+1] not in goal and not wall[curr_box[0]][curr_box[1]+1] 
                     or [curr_box[0]-1, curr_box[1]] not in goal and not wall[curr_box[0]-1][curr_box[1]]
                     or [curr_box[0]-1, curr_box[1]+1] not in goal and not wall[curr_box[0]-1][curr_box[1]+1]):     
                        return True

            if [curr_box[0]+1, curr_box[1]] in temp_box_wtht_cur or wall[curr_box[0]+1][curr_box[1]]: # BOT
                if [curr_box[0]+1, curr_box[1]+1] in temp_box_wtht_cur or wall[curr_box[0]+1][curr_box[1]+1] == 1: # RIGHT-BOT
                    # If boxes are in deadlock state but also in destination, they are not considered deadlock
                    if ([curr_box[0], curr_box[1]+1] not in goal and not wall[curr_box[0]][curr_box[1]+1] 
                     or [curr_box[0]+1, curr_box[1]] not in goal and not wall[curr_box[0]+1][curr_box[1]]
                     or [curr_box[0]+1, curr_box[1]+1] not in goal and not wall[curr_box[0]+1][curr_box[1]+1]):     
                        return True

    elif (dir == 'L'):  
        if curr_box[1] == 1 and valid_side['L'] == False:
            return True      
        if [curr_box[0], curr_box[1]-1] in temp_box_wtht_cur or wall[curr_box[0]][curr_box[1]-1] == 1: # LEFT

            if [curr_box[0]-1, curr_box[1]] in temp_box_wtht_cur or wall[curr_box[0]-1][curr_box[1]]: # TOP
                if [curr_box[0]-1, curr_box[1]-1] in temp_box_wtht_cur or wall[curr_box[0]-1][curr_box[1]-1] == 1: # LEFT-TOP
                    # If boxes are in deadlock state but also in destination, they are not considered deadlock
                    if ([curr_box[0], curr_box[1]-1] not in goal and not wall[curr_box[0]][curr_box[1]-1] 
                     or [curr_box[0]-1, curr_box[1]] not in goal and not wall[curr_box[0]-1][curr_box[1]]
                     or [curr_box[0]-1, curr_box[1]-1] not in goal and not wall[curr_box[0]-1][curr_box[1]-1]):     
                        return True

            if [curr_box[0]+1, curr_box[1]] in temp_box_wtht_cur or wall[curr_box[0]+1][curr_box[1]]: # BOT
                if [curr_box[0]+1, curr_box[1]-1] in temp_box_wtht_cur or wall[curr_box[0]+1][curr_box[1]-1] == 1: # LEFT-BOT
                    # If boxes are in deadlock state but also in destination, they are not considered deadlock
                    if ([curr_box[0], curr_box[1]-1] not in goal and not wall[curr_box[0]][curr_box[1]-1] 
                     or [curr_box[0]+1, curr_box[1]] not in goal and not wall[curr_box[0]+1][curr_box[1]]
                     or [curr_box[0]+1, curr_box[1]-1] not in goal and not wall[curr_box[0]+1][curr_box[1]-1]):     
                        return True    
    return False


# function for movement of a box
def move(point,dir,path,temp_box_list):
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
        if temp_box not in box_list and wall[temp_box[0]][temp_box[1]] == 0:
            box_list[ind]=[x + y for x, y in zip(point, directions[dir])]

            if checkDeadLock(box_list, box_list[ind], dir) != True:
                box_list.sort()                
                # Sort to avoid duplicate. Ex: [1,3,2] -> [1,2,3] same as [1,2,3]
                temp_append.append(point)
                temp_append.append(box_list)
                
                # check if any status has passed
                idx = point[0]*10 + point[1]
                counter = 0
                if idx in visited:
                    for k in visited[idx]:
                        if(k == temp_append):
                            counter = counter + 1

                # If this state havent passed, add (state + predicted distance) to queue
                if counter == 0:
                    temp_append.append(cur_path)
                    queue.append(temp_append)

            # check if goal
            if set(map(tuple,box_list))==set(map(tuple,goal)):
                stop = timeit.default_timer()
                total_time=stop-start_time
                print("solution found")
                print(cur_path)
                print("total time taken: ")
                print(total_time)
                print("total steps taken: ")
                print(len(cur_path))
                print("total space taken: ")
                print(ps.memory_info()[0]/(1024*1024)) 
                exit()
    else:
        # Sort to avoid duplicate. Ex: [1,3,2] -> [1,2,3] same as [1,2,3]
        box_list.sort()
        temp_append.append(point)
        temp_append.append(box_list)
        
        # check if any status has passed
        idx = point[0]*10 + point[1]
        counter = 0
        if idx in visited:
            for k in visited[idx]:
                if(k == temp_append):
                    counter = counter + 1
        # If this state havent passed, add (state+predicted distance)to queue
        if counter == 0:
            temp_append.append(cur_path)
            queue.append(temp_append)

        # check if goal is reach
        if set(map(tuple,box_list))==set(map(tuple,goal)):
            stop = timeit.default_timer()
            total_time=stop-start_time
            print("solution found")
            print(cur_path)
            print("total time taken: ")
            print(total_time)
            print("total steps take :")
            print(len(cur_path))
            print("total space taken: ")
            print(ps.memory_info()[0]/(1024*1024))
            exit()

# ============================== BFS FUNCTION =================================
# start counts time
start_time = timeit.default_timer()

# bfs function
def bfs():
    check_if_goal_in_side()
    # State store current position of current player and box
    node=[]
    node.append(player[0])
    node.append(box)    
    path=[]
    node.append(path)
    # Add current node = state+path to queue
    queue.append(node)

    count = 0
    while True:
        if len(queue) == 0:
            print(current_path)
            print ("Can not find a solution")
            return
        count = count+1
        # pop recent added node
        node = queue.popleft()
        state = node[:-1]
        current_player = node[0]
        
        # Dictionary visited contain key: player position
        # and value: corresponding [states] 
        # state: [player, box1, box2]
        idx = current_player[0]*10 + current_player[1] 

        # check if there is a duplicate state
        if idx in visited:   
            cnt = 0   
            for pos in visited[idx]:
                if(state == pos):
                    cnt = 1
                    break       
            if(cnt == 0):
                visited[idx].append(state)            
        else:
            visited[idx] = []
            visited[idx].append(state)            

        # current path and current box list
        current_path = node[-1][:]
        temp_box_list = node[1]

        # determine position of player after each possible move
        U = [x + y for x, y in zip(current_player, directions['U'])]
        D = [x + y for x, y in zip(current_player, directions['D'])]
        R = [x + y for x, y in zip(current_player, directions['R'])]
        L = [x + y for x, y in zip(current_player, directions['L'])]
        
        # Check current player's position 
        # Add a state to queue if satifies 
        # 1. the player does not move into the wall 
        # 2. the player does not push a box that is already close to the wall towards the wall
        # 3. the player does not push 2 boxes at a time
        # 4. Visited list does not contain this state
        # Final, check if the goal status is reached or not
        if wall[U[0]][U[1]] == 0:
            move(U, 'U', current_path, temp_box_list)
        if wall[D[0]][D[1]] == 0:
            move(D, 'D', current_path, temp_box_list)
        if wall[R[0]][R[1]] == 0:
            move(R, 'R', current_path, temp_box_list)
        if wall[L[0]][L[1]] == 0:
            move(L, 'L', current_path, temp_box_list)
bfs()
