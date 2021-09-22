import sys
import numpy as np
import timeit
import board

directions={}
directions['N'] = [-1,0]
directions['E'] = [0,1]
directions['W'] = [0,-1]
directions['S'] = [1,0] 
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

if len(sys.argv)<2:
	print("please provide textfile name as system argument \n python bfs.py <filename>")
	exit(0)

board.print_char(sys.argv[1])
wall = board.wall[:]
robot = board.robot[:]
storage = board.storage[:]
box = board.box[:]

visited={}
queue=[]

# function for movement of a state
def move(point,dir,path,temp_box_list):
    box_list = []
    box_list = temp_box_list[:] 
    temp_append = []
    cur_path = []
    cur_path = path[:]
    cur_path.append(dir)

    # next-pos of robot not be wall
    if wall[point[0]][point[1]] == 0:
        if point in box_list:
            ind = box_list.index(point)
            temp_box = [x + y for x, y in zip(point, directions[dir])]
            if temp_box not in box_list and wall[temp_box[0]][temp_box[1]] == 0:
                box_list[ind]=[x + y for x, y in zip(point, directions[dir])]
                # Sort to avoid duplicate. Ex: [1,3,2] -> [1,2,3] same as [1,2,3]
                box_list.sort()

                temp_append.append(point)
                for i in box_list:
                    temp_append.append(i)
                
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
                    dis_append=heuristic(box_list,storage,cur_path,point)
                    temp_append.append(dis_append)
                    queue.append(temp_append)

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
            temp_append.append(point)
            box_list.sort()
            for i in box_list:
                temp_append.append(i)
            
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
                dis_append=heuristic(box_list,storage,cur_path,point)
                temp_append.append(dis_append)
                queue.append(temp_append)

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

# function for A* algorithm
start_time = timeit.default_timer()
def Astar_heuristic():        
    temp_queue = []    # temp_queue contain current state
    initial = robot[0] # store current robot's position
    temp_queue.append(initial)

    for i in box:
        temp_queue.append(i) # append each box into temp_queue
    path=[]
    temp_queue
    temp_queue.append(path)
    temp_queue.append(0)
    queue.append(temp_queue)
    count = 0
    
    while queue:
        temp_box_list = []
        visited_adding = []
        # Chose (state) with min distance
        queue.sort(key = lambda x: x[-1])

        # Get a robot position and a state
        robot_position_list = queue.pop(0)
        robot_position = robot_position_list[0]
        visited_adding = robot_position_list[:-2] 

        # Dictionary visited contain key: robot position
        # and value: corresponding [states] 
        # state: [robot, box1, box2]
        idx = robot_position[0]*10 + robot_position[1] 

        # check if there is a duplicate state
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
        # box only 
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
