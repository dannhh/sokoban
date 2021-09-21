from os import PRIO_USER
import sys
import numpy as np
from collections import deque
import timeit
wall = []
robot=[]
storage=[]
box=[]
directions={}
directions['N']=[0,-1]
directions['E']=[1,0]
directions['W']=[-1,0]
directions['S']=[0,1] 
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

def print_char(filename):
    f = open(filename, 'r')
# def print_char():
#     f = open("/home/daneiii/Documents/AI-sokoban/sokoban/test-case-one.txt", 'r')
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
            if char == "R":
                new.append(0)
                robot.append(temp)
            if char == "S":
                new.append(0)
                storage.append(temp)
            if char == "B":
                new.append(0)
                box.append(temp)
            if char == ".":
                new.append(0)
                box.append(temp)
                storage.append(temp)
            if char == "$":
                new.append(0)
                robot.append(temp)
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


if len(sys.argv)<2:
	print("please provide textfile name as system argument \n python bfs.py <filename>")
	exit(0)
print_char(sys.argv[1])
# print_char()
visited={}
queue=[]

if len(robot) == 0 or len(box) == 0 or len(storage) == 0 or len(wall) == 0:
	print("please provide the textfile in write format Walls :O \n storage : S \n box : B \n robot : R \n box on storage : . \n robot on storage : $ \n should include walls,storage,box,robot")
	exit(0)

storage.sort()
# function for movement of a box

def move(point,dir,path,temp_box_list):
    box_list=[]
    box_list=temp_box_list[:] 
    temp_append=[]
    cur_path=[]
    cur_path=path[:]
    cur_path.append(dir) #[..., 'N']

    # next-pos not be wall

    if wall[point[0]][point[1]] == 0:
        if point in box_list:
            ind=box_list.index(point)
            temp_box=[x + y for x, y in zip(point, directions[dir])]
            if temp_box not in box_list and wall[temp_box[0]][temp_box[1]] == 0:
                box_list[ind]=[x + y for x, y in zip(point, directions[dir])]
                box_list.sort()

                temp_append.append(point)
                for i in box_list:
                    temp_append.append(i)
                
                idx = point[0]*10 + point[1]
                counter = 0
                if idx in visited:
                    for k in visited[idx]:
                        if(k == temp_append):
                            counter = counter + 1

                if counter==0:
                    temp_append.append(cur_path)
                    dis_append=heuristic(box_list,storage,cur_path,point)
                    temp_append.append(dis_append)
                    queue.append(temp_append)

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
            temp_append.append(point)
            box_list.sort()
            for i in box_list:
                temp_append.append(i)
            
            idx = point[0]*10 + point[1]
            counter = 0
            if idx in visited:
                for k in visited[idx]:
                    if(k == temp_append):
                        counter = counter + 1

            if counter==0:
                temp_append.append(cur_path)
                dis_append=heuristic(box_list,storage,cur_path,point)
                temp_append.append(dis_append)
                queue.append(temp_append)

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

# function for A* algorithm

start_time = timeit.default_timer()
def Astar_heuristic():    
    # temp_queue contains current queue, form: [[]]
    temp_queue = []
    # store current robot's position, form: []
    initial = robot[0]
    temp_queue.append(initial) # form: [robot[0]]: [[]]
    # box form: [[]]
    box.sort()
    for i in box:
        temp_queue.append(i) # append each box into temp_queue
    path=[]
    temp_queue
    temp_queue.append(path)
    temp_queue.append(0)
    queue.append(temp_queue) # queue form: [[[]]] = [0:temp_queue]
    count = 0
    # After this step, temp_queue: [robot[0], box[0],..., [], 0]
    
    while queue:
        temp_box_list = []
        visited_adding = []
        queue.sort(key = lambda x: x[-1])
        # robot_position_ls queue[0] (temp_queue)
        robot_position_list = queue.pop(0)
        # robot_position: robot[0]
        robot_position = robot_position_list[0]
        # visited_adding: queue \ {path, 0}
        visited_adding = robot_position_list[:-2]

        idx = robot_position[0]*10 + robot_position[1] 
        if idx in visited:     
            counter = 0   
            for pos in visited[idx]:
                if(visited_adding == pos):
                    counter = 1
                    break
                    
            if(counter == 0):
                visited[idx].append(visited_adding)            
        else:
            visited[idx] = []
            visited[idx].append(visited_adding)            

        # path only
        temp_path = robot_position_list[-2][:]
        # box only [[]]
        temp_box_list=robot_position_list[1:-2]

        # 4 possible directions [col, row] 
        N=[x + y for x, y in zip(robot_position, directions['N'])]
        S=[x + y for x, y in zip(robot_position, directions['S'])]
        E=[x + y for x, y in zip(robot_position, directions['E'])]
        W=[x + y for x, y in zip(robot_position, directions['W'])]
        
        move(N,dir_N,temp_path,temp_box_list)
        move(S,dir_S,temp_path,temp_box_list)
        move(E,dir_E,temp_path,temp_box_list)
        move(W,dir_W,temp_path,temp_box_list)
        
        count = count + 1
        if(count == 44):
            count = count
        if not queue:
            print("solution not found")
            exit()
            
Astar_heuristic()
