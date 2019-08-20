#import timeit

#start_time = timeit.default_timer()
# ----------------------------------------------------------------------------------------------

with open("input.txt", "r") as input_txt:
    # Read dimension of grid
    grid_dimension = int(input_txt.readline())
    # print  grid_dimension

    # Number and location of walls
    num_grid_walls = int(input_txt.readline())
    # print  num_grid_walls

    grid_walls = []
    for i in range(num_grid_walls):
        grid_walls.append(input_txt.readline().rstrip("\n").split(","))
    # print  grid_walls

    # Number, location, and rewards of terminal states
    num_term_cells = int(input_txt.readline())
    # print  num_term_cells

    grid_terminals = []
    for i in range(num_term_cells):
        grid_terminals.append(input_txt.readline().rstrip("\n").split(","))
    # print  grid_terminals

    # Probability of moving
    prob = float(input_txt.readline())
    # print  prob

    # Non-reward cell Value
    step_cost = float(input_txt.readline())
    # print  step_cost

    # Discount factor
    gamma = float(input_txt.readline())
    # print  gamma
# ----------------------------------------------------------------------------------------------

matrix = [[-99.9 for i in range(grid_dimension)] for j in range(grid_dimension)]
cell_action = [["" for i in range(grid_dimension)] for j in range(grid_dimension)]

# ----------------------------------------------------------------------------------------------
# Mark Walls And Rewards
x_coord = []
y_coord = []

x_rew = []
y_rew = []
val_rew = []

for wall in range(num_grid_walls):
    x_coord.append(int(grid_walls[wall][0]) - 1)
    y_coord.append(int(grid_walls[wall][1]) - 1)

# Mark the locations of walls in matrix
for row in range(grid_dimension):
    for col in range(grid_dimension):
        for w in range(len(x_coord)):
            if row == x_coord[w] and col == y_coord[w]:
                cell_action[row][col] = "N"

for rew in range(num_term_cells):
    x_rew.append(int(grid_terminals[rew][0]) - 1)
    y_rew.append(int(grid_terminals[rew][1]) - 1)
    val_rew.append(float(grid_terminals[rew][2]))

# Mark the locations of rewards in matrix
for row in range(grid_dimension):
    for col in range(grid_dimension):
        for r in range(len(x_rew)):
            if row == x_rew[r] and col == y_rew[r]:
                cell_action[row][col] = "E"
                matrix[row][col] = val_rew[r]

# ----------------------------------------------------------------------------------------------
# MDP Simulation

#iteration = 0
count = 1
while count != 0:
    count = 0
    #iteration += 1

    for row in range(grid_dimension):
        for col in range(grid_dimension):

            tot_cell_uty_u = 0.0
            tot_cell_uty_d = 0.0
            tot_cell_uty_l = 0.0
            tot_cell_uty_r = 0.0

            if cell_action[row][col] != "N" and cell_action[row][col] != "E":
                # ----------------------------------------------------------------------------------------------
                # Move North/Up

                # Checking if row above is not a wall and is within bounds
                if row - 1 >= 0 and cell_action[row - 1][col] != "N":
                    tot_cell_uty_u += float(prob) * (
                            float(gamma) * matrix[row - 1][col] + step_cost)
                else:
                    tot_cell_uty_u += float(prob) * (
                            float(gamma) * matrix[row][col] + step_cost)

                if col - 1 >= 0 and row - 1 >= 0 and cell_action[row - 1][col - 1] != "N":
                    tot_cell_uty_u += (float(gamma) * matrix[row - 1][
                        col - 1] + step_cost) * (1 - float(prob)) * 0.5
                else:
                    tot_cell_uty_u += (float(gamma) * matrix[row][col] + step_cost) * (
                            1 - float(prob)) * 0.5

                if col + 1 <= grid_dimension - 1 and row - 1 >= 0 and cell_action[row - 1][col + 1] != "N":
                    tot_cell_uty_u += (float(gamma) * matrix[row - 1][
                        col + 1] + step_cost) * (1 - float(prob)) * 0.5
                else:
                    tot_cell_uty_u += (float(gamma) * matrix[row][col] + step_cost) * (
                            1 - float(prob)) * 0.5

                # ----------------------------------------------------------------------------------------------
                # Move South/Down

                # Checking if row above is not a wall and is within bounds
                if row + 1 <= grid_dimension - 1 and cell_action[row + 1][col] != "N":
                    tot_cell_uty_d += float(prob) * (
                            float(gamma) * matrix[row + 1][col] + step_cost)
                else:
                    tot_cell_uty_d += float(prob) * (
                            float(gamma) * matrix[row][col] + step_cost)

                if col - 1 >= 0 and row + 1 <= grid_dimension - 1 and cell_action[row + 1][
                    col - 1] != "N":
                    tot_cell_uty_d += (float(gamma) * matrix[row + 1][
                        col - 1] + step_cost) * (
                                            1 - float(prob)) * 0.5
                else:
                    tot_cell_uty_d += (float(gamma) * matrix[row][col] + step_cost) * (
                            1 - float(prob)) * 0.5

                if col + 1 <= grid_dimension - 1 and row + 1 <= grid_dimension - 1 and \
                        cell_action[row + 1][col + 1] != "N":
                    tot_cell_uty_d += (float(gamma) * matrix[row + 1][
                        col + 1] + step_cost) * (
                                            1 - float(prob)) * 0.5
                else:
                    tot_cell_uty_d += (float(gamma) * matrix[row][col] + step_cost) * (
                            1 - float(prob)) * 0.5

                # ----------------------------------------------------------------------------------------------
                # Move East/Right

                # Checking if row above is not a wall and is within bounds
                if col + 1 <= grid_dimension - 1 and cell_action[row][col + 1] != "N":
                    tot_cell_uty_r += (
                            float(prob) * (float(gamma) * matrix[row][col + 1] + step_cost))
                else:
                    tot_cell_uty_r += (
                            float(prob) * (float(gamma) * matrix[row][col] + step_cost))

                if row - 1 >= 0 and col + 1 <= grid_dimension - 1 and cell_action[row - 1][
                    col + 1] != "N":
                    tot_cell_uty_r += (float(gamma) * matrix[row - 1][
                        col + 1] + step_cost) * (
                                            1 - float(prob)) * 0.5
                else:
                    tot_cell_uty_r += (float(gamma) * matrix[row][col] + step_cost) * (
                            1 - float(prob)) * 0.5

                if row + 1 <= grid_dimension - 1 and col + 1 <= grid_dimension - 1 and \
                        cell_action[row + 1][
                            col + 1] != "N":
                    tot_cell_uty_r += (float(gamma) * matrix[row + 1][
                        col + 1] + step_cost) * (
                                            1 - float(prob)) * 0.5
                else:
                    tot_cell_uty_r += (float(gamma) * matrix[row][col] + step_cost) * (
                            1 - float(prob)) * 0.5

                # ----------------------------------------------------------------------------------------------
                # Move West/Left

                # Checking if row above is not a wall and is within bounds
                if col - 1 >= 0 and cell_action[row][col - 1] != "N":
                    tot_cell_uty_l += (float(prob) * (
                            float(gamma) * matrix[row][col - 1] + step_cost))
                else:
                    tot_cell_uty_l += (
                            float(prob) * (float(gamma) * matrix[row][col] + step_cost))

                if row - 1 >= 0 and col - 1 >= 0 and cell_action[row - 1][
                    col - 1] != "N":
                    tot_cell_uty_l += (float(gamma) * matrix[row - 1][
                        col - 1] + step_cost) * (
                                            1 - float(prob)) * 0.5
                else:
                    tot_cell_uty_l += (float(gamma) * matrix[row][col] + step_cost) * (
                            1 - float(prob)) * 0.5

                if row + 1 <= grid_dimension - 1 and col - 1 >= 0 and \
                        cell_action[row + 1][col - 1] != "N":
                    tot_cell_uty_l += (float(gamma) * matrix[row + 1][
                        col - 1] + step_cost) * (
                                            1 - float(prob)) * 0.5
                else:
                    tot_cell_uty_l += (float(gamma) * matrix[row][col] + step_cost) * (
                            1 - float(prob)) * 0.5

                # ----------------------------------------------------------------------------------------------
                # Decide policy of cell

                total_utility = max(tot_cell_uty_u,tot_cell_uty_d,tot_cell_uty_l,tot_cell_uty_r)

                if total_utility > matrix[row][col]:
                    matrix[row][col] = total_utility
                    if total_utility == tot_cell_uty_u:
                        cell_action[row][col] = "U"
                    elif total_utility == tot_cell_uty_d:
                        cell_action[row][col] = "D"
                    elif total_utility == tot_cell_uty_l:
                        cell_action[row][col] = "L"
                    else:
                        cell_action[row][col] = "R"
                    count = 1

                if tot_cell_uty_u == tot_cell_uty_d and tot_cell_uty_l == tot_cell_uty_r and tot_cell_uty_u == tot_cell_uty_l:
                    matrix[row][col] = tot_cell_uty_u
                    cell_action[row][col] = "U"
                    count = 1

#print iteration
#print cell_action
# ----------------------------------------------------------------------------------------------

with open('output.txt', 'w') as output_txt:
    for row in range(grid_dimension):
        for col in range(grid_dimension):
            if col < grid_dimension - 1:
                output_txt.write(cell_action[row][col])
                output_txt.write(",")
            elif col == grid_dimension - 1:
                output_txt.write(cell_action[row][col])
            else:
                break
        if row <= grid_dimension - 1:
            output_txt.write("\n")
        else:
            break

# ----------------------------------------------------------------------------------------------

#print cell_action
#print(timeit.default_timer() - start_time)