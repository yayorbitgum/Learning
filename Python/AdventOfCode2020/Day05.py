# https://adventofcode.com/2020/day/5

seat_ids = []
with open('inputs\day05_input.txt', 'r') as file:
    file = file.readlines()

for ticket in file:
    # Plane seating dimensions and arrangement.
    rows = [row for row in range(0, 128)]
    columns = [seat for seat in range(0, 8)]

    for instruction in ticket.strip():
        # Determine row. -------------------------------------------------------
        if len(rows) > 2:
            if instruction == 'F':
                # F means to take the lower half.
                del rows[(len(rows) // 2):]
            elif instruction == 'B':
                # B means to take the upper half.
                del rows[:(len(rows) // 2)]
        else:
            # The final F/B keeps the lower/upper of the two, respectively.
            if instruction == 'F':
                del rows[1]
            elif instruction == 'B':
                del rows[0]

        # Determine column. ----------------------------------------------------
        if len(columns) > 2:
            if instruction == 'L':
                # L means to take the lower half.
                del columns[(len(columns) // 2):]
            elif instruction == 'R':
                # R means to take the upper half.
                del columns[:(len(columns) // 2)]
        else:
            # The final L/R keeps the lower/upper of the two, respectively.
            if instruction == 'L':
                del columns[1]
            elif instruction == 'R':
                del columns[0]

    # Determine seat ID. -------------------------------------------------------
    seat_id = (rows[0] * 8) + columns[0]
    seat_ids.append(seat_id)
    print(f"Ticket {ticket.strip()}: Row {rows[0]} | Column {columns[0]} | Seat {seat_id}.")


# Part one answer!
print(f"The highest seat ID on a boarding pass is {max(seat_ids)}.")

# Part two answer!
seat_ids.sort()
for index, seat in enumerate(seat_ids):
    try:
        if seat_ids[index+1] != seat + 1:
            print(f"Your seat is {seat + 1}.")
    except IndexError:
        pass