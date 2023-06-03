"""
Input is a vector of F's and B's, in terms of forwards and backwards caps
Output is a set of commands (printed out) to get either all F's or all B's
Fewest commands are the goal!

Please see the problem write-up to get more details
"""

caps = ["F", "F", "B", "B", "B", "F", "B", "B", "B", "F", "F", "B", "F"] #F doi
cap2 = ["F", "F", "B", "B", "B", "F", "B", "B", "B", "F", "F", "F", "F"] #B doi
cap3 = ['F','F','B','H','B','F','B','B','B','F','H','F','F'] #B doi


def pleaseConform(caps):
    start = forward = backward = bareheaded = 0
    commands = []

    # Chia day thanh cac khoang co trang thai giong nhau
    for i in range(1, len(caps)):
        if caps[start] != caps[i]:
            commands.append((start, i - 1, caps[start]))
            start = i
        if caps[i-1] == 'F':
            forward += 1
        elif caps[i-1] == 'H':
            bareheaded += 1

    commands.append((start, len(caps) - 1, caps[start]))
    if caps[len(caps) - 1] == 'F' :
        forward += 1
    elif caps[len(caps) - 1] == 'H':
            bareheaded += 1
    backward = len(caps) - forward - bareheaded

    print(commands)
    if forward > backward:
        flip = 'F'
    else:
        flip = 'B'
    # print(forward, backward, flip)
    for t in commands:
        if t[2] != flip and t[2] != 'H':
            if t[0] != t[1]:
                print('People in position', t[0], 'through', t[1], 'flip your caps!')
            elif t[0] == t[1]:
                print('Person in position', t[0], 'flip your cap!')

pleaseConform(caps)
# pleaseConform(cap2)
# pleaseConform(cap3)