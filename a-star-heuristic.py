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


# function for reading a file
def print_char():
    f = open("/home/daneiii/Documents/AI-sokoban/test-case-one.txt", 'r')
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

print_char()
visited=[]
queue=[]

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
                temp_append.append(point)
                for i in box_list:
                    temp_append.append(i)
                if temp_append not in visited:
                    counter=0
                    popped_robot=temp_append[0]
                    for k in visited:
                        k_temp_visited=k[:]
                        
                        k_robot=k_temp_visited.pop(0)
                        temporary=[]
                        if k_robot==popped_robot:
                            count_list=0
                            temporary=temp_append[1:]
                            for m in k_temp_visited:
                                if m in temporary:
                                    count_list=count_list+1
                            if count_list==len(temporary):
                                counter=counter+1
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
            for i in box_list:
                temp_append.append(i)
            if temp_append not in visited:
                counter=0
                popped_robot=temp_append[0]
                for k in visited:
                    k_temp_visited=k[:]
                    count_list=0
                    k_robot=k_temp_visited.pop(0)
                    temporary=[]
                    if k_robot==popped_robot:
                        temporary=temp_append[1:]
                        for m in k_temp_visited:
                            if m in temporary:
                                count_list=count_list+1
                        if count_list==len(temporary):
                            counter=counter+1
                if counter==0:
                    dis_append=heuristic(box_list,storage,cur_path,point)
                    temp_append.append(cur_path)
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

def Astar_heuristic():
    start_time = timeit.default_timer()
    # temp_queue contains current queue, form: [[]]
    temp_queue = []
    # store current robot's position, form: []
    initial = robot[0]
    temp_queue.append(initial) # form: [robot[0]]: [[]]
    # box form: [[]]
    for i in box:
        temp_queue.append(i) # append each box into temp_queue
    path=[]
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
        if visited_adding not in visited:
            visited.append(visited_adding)		
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
        if not queue:
            print("solution not found")
            exit()
            
Astar_heuristic()
