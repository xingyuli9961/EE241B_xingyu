# This is the python vcd_parser used in this project.

# read the file
def read_file(file):
    file = open(file, "r")
    lines = [l.strip() for l in file.readlines() if l.strip() != ""]
    return lines

# get a dictionary of all signals
def get_signals_all(lines):
    signal_dict = {}
    prefix=""
    prefix_length=[]

    while (len(lines) != 0):
        curr_line = lines.pop(0)
        if (curr_line[0:4] == "$var"):
            tmplist = curr_line.split()
            name = prefix + tmplist[4]
            key = tmplist[3]
            if (key in signal_dict.keys()):
                name = signal_dict[key] + ", " + name
            signal_dict[key] = name
            continue
        elif (curr_line[0:15] == "$enddefinitions"):
            break
        elif (curr_line[0:4] == "$end" or curr_line[0:8] == "$version"
              or curr_line[0:8] == "$comment" or curr_line[0:5] == "$date"):
            continue
        elif (curr_line[0:10] == "$timescale"):
            print(curr_line)
            continue
        elif (curr_line[0:6] == "$scope"):
            tmp = curr_line.split()[2] + "."
            prefix += tmp
            prefix_length.append(len(tmp))
            continue
        elif (curr_line[0:8]=="$upscope"):
            tmp = prefix_length.pop()
            prefix = prefix[0:-tmp]
            continue
        else:
            print("Exception: " + curr_line)
            continue
    return signal_dict


# get a dictionary of selected signals
def get_signals_selected(lines, signal_lists):
    signal_dict = {}
    prefix=""
    prefix_length=[]

    while (len(lines) != 0):
        curr_line = lines.pop(0)
        if (curr_line[0:4] == "$var"):
            tmplist = curr_line.split()
            name = prefix + tmplist[4]
            key = tmplist[3]
            if (name in signal_lists):
                signal_dict[key] = name
            continue
        elif (curr_line[0:15] == "$enddefinitions"):
            break
        elif (curr_line[0:4] == "$end" or curr_line[0:8] == "$version"
              or curr_line[0:8] == "$comment" or curr_line[0:5] == "$date"):
            continue
        elif (curr_line[0:10] == "$timescale"):
            print(curr_line)
            continue
        elif (curr_line[0:6] == "$scope"):
            tmp = curr_line.split()[2] + "."
            prefix += tmp
            prefix_length.append(len(tmp))
            continue
        elif (curr_line[0:8]=="$upscope"):
            tmp = prefix_length.pop()
            prefix = prefix[0:-tmp]
            continue
        else:
            print("Exception: " + curr_line)
            continue
    return signal_dict


# dump all the vcd data into a switching behaviour matrix, a timestamp array, and a dictionary for the signals and its index in the matrix
def dump_all(lines, signals):
    signal_list = list(signals.keys())
    index_dict = {}
    time = []
    database = []
    tmpdata = [0]*len(signal_list)
    for i in range(len(signal_list)):
        index_dict[signal_list[i]] = i
    while (len(lines) != 0):
        curr_line = lines.pop(0)
        if (curr_line[0] == "#"):
        # update timestamp
            if (len(time) > 0):
                database.append(tmpdata.copy())
            time.append(int(curr_line[1:]))
            if (int(curr_line[1:])%500 == 0):
                print(int(curr_line[1:]))
        else:
            if (curr_line[0] == 'b'):
                if (curr_line.split()[0][1:] == 'x'):
                    continue
                value = int(curr_line.split()[0][1:], 2)
                index = index_dict.get(curr_line.split()[1])
                tmpdata[index] = value
            elif (curr_line[0] == "0" or curr_line[0] == "1"):
                value = int(curr_line[0])
                index = index_dict.get(curr_line[1:])
                tmpdata[index] = value
            elif (curr_line[0] == 'x'):
                pass
            else:
                print("Error：" + curr_line)

    database.append(tmpdata)
    return database, time, index_dict


# dump the vcd data before the endtime into a switching behaviour matrix, a timestamp array, and a dictionary for the signals and its index in the matrix
def dump_selected(lines, signals, endtime):
    signal_list = list(signals.keys())
    index_dict = {}
    time = []
    database = []
    tmpdata = [0]*len(signal_list)
    for i in range(len(signal_list)):
        index_dict[signal_list[i]] = i
    while (len(lines) != 0):
        curr_line = lines.pop(0)
        if (curr_line[0] == "#"):
        # update timestamp
            if (int(curr_line[1:]) > endtime):
                break
            else:
                if (len(time) > 0):
                    database.append(tmpdata.copy())
                time.append(int(curr_line[1:]))
                if (int(curr_line[1:])%500 == 0):
                    print(int(curr_line[1:]))
        else:
            if (curr_line[0] == 'b'):
                if (curr_line.split()[0][1:] == 'x'):
                    continue
                value = int(curr_line.split()[0][1:], 2)
                symbol = curr_line.split()[1]
                if (symbol in signal_list):
                    index = index_dict.get(symbol)
                    tmpdata[index] = value
            elif (curr_line[0] == "0" or curr_line[0] == "1"):
                value = int(curr_line[0])
                symbol = curr_line[1:]
                if (symbol in signal_list):
                    index = index_dict.get(symbol)
                    tmpdata[index] = value
            elif (curr_line[0] == 'x'):
                pass
            else:
                print("Error：" + curr_line)

    database.append(tmpdata)
    return database, time, index_dict

# convert the switching matrix from the dump_* functions into a new matrix that each row the matrix represent the behaviour of a signal
def toggle_matrix(signal_list, index_dict, database):
    switches = []
    for i in signal_list:
        tmpswitches = []
        index = index_dict.get(i)
        old = database[0][index]
        for j in range(1, len(database)):
            curr = database[j][index]
            imm = str(old ^ curr)
            count = 0
            for k in range(len(imm)):
                if (imm[k] == '1'):
                    count += 1
            tmpswitches.append(count)
            old = int(curr)
        switches.append(tmpswitches)
            
    return switches

# calculate the total switching activity of a signal over the program
def switching_count(switch_matrix):
    switching_behaviour = []
    for i in range(len(switch_matrix)):
        switching_behaviour.append(sum(switch_matrix[i]))
    return switching_behaviour

# the function to call if you want to get all the data for a certain vcd file
def get_all_switching_behavior(filename):
    file = read_file(filename)
    signals = get_signals_all(file)
    signal_list = list(signals.keys())
    data, timelist, index_dict = dump_all(file, signals)
    switch_matrix = toggle_matrix(signal_list, index_dict, data)
    switching_behaviour = switching_count(switch_matrix)
    return signals, signal_list, switching_behaviour, switch_matrix


# the function to call if you want to get the data before endtime for a certain vcd file
def get_selected_switching_behavior(filename, signal_list, time):
    file = read_file(filename)
    if (signal_list == 0):
        signals = get_signals_all(file)
    else:
        signals = get_signals_selected(file, signal_list)
    signal_list = list(signals.keys())
    if (time == -1):
        data, timelist, index_dict = dump_all(file, signals)
    else:
        data, timelist, index_dict = dump_selected(file, signals, time)
    switch_matrix = toggle_matrix(signal_list, index_dict, data)
    switching_behaviour = switching_count(switch_matrix)
    return signals, signal_list, switching_behaviour, switch_matrix

# convert an array of switching beviour into the cycle format
def post_switch_in_cycle(switch_array):
    post_array = []
    cycles = int(len(switch_array)/10)
    for i in range(cycles):
        tmp = 0
        for k in range(10):
            tmp += switch_array[i+k]
        post_array.append(tmp)
    return post_array

# vector add the matrix
def compress_matrix(switch_matrix):
    imm = np.array(switch_matrix)
    result = np.zeros(len(switch_matrix[0]))
    for i in range(len(switch_matrix)):
        result = np.add(result, switch_matrix[i])
    print("Compression finished!")
    return result
