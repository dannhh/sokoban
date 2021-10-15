# sokoban

Members:
- Nguyen Hoai Thuong - 1912184
- Nguyen Huynh Tien - 1915482
- Nguyen Hong Dan - 1910916

# How to run the program?

First, open file in VSCode, run in terminal

Second, input the command python3 sokoban_solver "filename1" "filename2"
- "filename1" is the testcase you want to run, we provide two types: MiniCosmos.txt or MicroCosmos.txt
- "filename2" is the result file name you want to save the result of the program. It should be test.txt

Third, after run the command, it asks you to choose testcase number to run. Enter the number form 1 to 40 (it means 40 levels in MiniCosmos or MicroCosmos) or enter -1 to out the program

Then it asks you to choose algorithm to run, enter 1 to run BFS, 2 to run A_star.

After the algorithm finished, the terminal print the solution of the test-case (include: list of move (U, D, L, R), total time taken to run algorithm, total steps, total space taken, total states created in the test) and show "Done algorithm".

Then, the game window appears and demo the test.

Having fun with our Sokoban Solver