wall = []
robot=[]
storage=[]
box=[]

def print_char(filename):
    f = open(filename, 'r')
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
                robot.append(temp)
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

    if len(robot) == 0 or len(box) == 0 or len(storage) == 0 or len(wall) == 0:
        print("please provide the textfile in write format Walls :O \n storage : S \n box : B \n robot : R \n box on storage : . \n robot on storage : $ \n should include walls,storage,box,robot")
        exit(0)