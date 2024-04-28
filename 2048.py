row = [0,0,4,2]

class Block()

def left():
    count = 0
    for i in range(4):
        if row[i] != 0:
            row[count] = row[i]
            count += 1
    while count < 4:
        row[count] = 0
        count += 1
    def merge():
        for i in range(3):
            if row[i] == row[i + 1]:
                row[i] *= 2
                row.pop(i+1)
                row.append(0)
    merge()
def right():
    row.reverse()
    left()
    row.reverse()
right()
print(row)
