import sys
import numpy as np
from collections import deque
import timeit

wall = []
player=[]
storage=[]
box=[]

directions={}
directions['N'] = [-1,0]
directions['E'] = [0,1]
directions['W'] = [0,-1]
directions['S'] = [1,0] 
start_time=0

# reading the file
# def print_char(filename):
def print_char():
    f = open("/home/daneiii/Documents/AI-sokoban/sokoban/test-case-four.txt", 'r')
    i = 0
    j = 0
    new = []
    while True:
        char=f.read(1)		
        temp = []                
        if char: 
            temp.append(i)
            temp.append(j)
            if char == "O":
                new.append(1)
            elif char == "R":
                new.append(0)
                player.append(temp)
            elif char == "S":
                new.append(0)
                storage.append(temp)
            elif char == "B":
                new.append(0)
                box.append(temp)
            elif char == ".":
                new.append(0)
                box.append(temp)
                storage.append(temp)
            elif char == "$":
                new.append(0)
                player.append(temp)
                storage.append(temp)
            if char == "\n":
                j=0
                wall.append(new)
                new = []
                i=i+1
            else:               
                j=j+1
                if len(new) < j:
                    new.append(0)
        else:
            break

# if len(sys.argv)<2:
#     print("please provide textfile name as system argument \n python bfs.py <filename>")
#     exit(0)

print_char()
visited={}
queue=deque()

if len(player) == 0 or len(box) == 0 or len(storage) == 0 or len(wall) == 0:
        print("please provide the textfile in write format wall :O \n storage : S \n box : B \n player : R \n box on storage : . \n player on storage : $ \n should include wall,storage,box,player")
        exit(0)

# check whether a goal state

# function for movement of a box
def move(point,dir,path,temp_box_list):
    box_list = temp_box_list[:] 
    temp_append = []
    path.append(dir)
    cur_path = path

    if point in box_list:
        ind = box_list.index(point)
        temp_box = [x + y for x, y in zip(point, directions[dir])]
        if temp_box not in box_list and wall[temp_box[0]][temp_box[1]] == 0:
            box_list[ind]=[x + y for x, y in zip(point, directions[dir])]
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
            if counter==0:
                temp_append.append(cur_path)
                queue.appendleft(temp_append)

            # check if goal
            if set(map(tuple,box_list))==set(map(tuple,storage)):
                stop = timeit.default_timer()
                total_time=stop-start_time
                print("solution found")
                print(cur_path)
                print("total time taken: ")
                print(total_time)
                print("total steps take :")
                print(len(cur_path))
                exit()
    else:
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
        if counter==0:
            temp_append.append(cur_path)
            queue.appendleft(temp_append)

        # check if goal
        if set(map(tuple,box_list))==set(map(tuple,storage)):
            stop = timeit.default_timer()
            total_time=stop-start_time
            print("solution found")
            print(cur_path)
            print("total time taken: ")
            print(total_time)
            print("total steps take :")
            print(len(cur_path))
            exit()


#directions
dir_N='N'
dir_S='S'
dir_E='E'
dir_W='W'

start_time = timeit.default_timer()
#dfs function
def dfs():
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

        current_path = node[-1][:]
        temp_box_list = node[1]

        Up    = [x + y for x, y in zip(current_player, directions['N'])]
        Down  = [x + y for x, y in zip(current_player, directions['S'])]
        Right = [x + y for x, y in zip(current_player, directions['E'])]
        Left  = [x + y for x, y in zip(current_player, directions['W'])]
        
        if wall[Up[0]][Up[1]] == 0:
            move(Up, dir_N, current_path, temp_box_list)
        if wall[Down[0]][Down[1]] == 0:
            move(Down, dir_S, current_path, temp_box_list)
        if wall[Right[0]][Right[1]] == 0:
            move(Right, dir_E, current_path, temp_box_list)
        if wall[Left[0]][Left[1]] == 0:
            move(Left, dir_W,current_path,temp_box_list)
dfs()

