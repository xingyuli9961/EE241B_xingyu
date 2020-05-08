# This file contains some records of the model and verification functions I used

def update_bruteforce(model, count, test_array, outfile):
    test_insn_array = dump_instructions(outfile)
    test_sdec =  decode_simple(test_insn_array[:1000])
    compressed_switch = post_switch_in_cycle(test_array)
    for i in range(1, min(len(test_sdec), len(compressed_switch))):
        index = test_sdec[i-1]*10 + test_sdec[i]
        model[index] += compressed_switch[i]
        count[index] += 1
    return model, count

def brute_force_verification(switch_matrix0, switch_matrix1, switch_matrix2, switch_matrix3, switch_matrix4,
                             switch_matrix5, switch_matrix6, switch_matrix7, switch_matrix8, switch_matrix9,
                             switch_matrix10, switch_matrix11, switch_matrix12):
    verify_insn_array = dump_instructions('../data/towers.riscv.out')
    verify_sdec =  decode_simple(verify_insn_array[:1000])
    correctness = np.zeros(407)
    for k in range(407):
        brute_model = np.zeros(100)
        brute_count = np.zeros(100)
        the_important_index = k
        brute_model, brute_count = update_bruteforce(brute_model, brute_count, switch_matrix0[the_important_index], 'rv32ui-p-xor.out')
        brute_model, brute_count = update_bruteforce(brute_model, brute_count, switch_matrix1[the_important_index], 'rv32ui-p-beq.out')
        brute_model, brute_count = update_bruteforce(brute_model, brute_count, switch_matrix2[the_important_index], 'median.riscv.out')
        brute_model, brute_count = update_bruteforce(brute_model, brute_count, switch_matrix3[the_important_index], 'qsort.riscv-large.out')
        brute_model, brute_count = update_bruteforce(brute_model, brute_count, switch_matrix4[the_important_index], '../data/rv32ui-p-sb.out')
        brute_model, brute_count = update_bruteforce(brute_model, brute_count, switch_matrix5[the_important_index], '../data/rv32ui-p-jalr.out')
        brute_model, brute_count = update_bruteforce(brute_model, brute_count, switch_matrix6[the_important_index], '../data/rv32ui-p-addi.out')
        brute_model, brute_count = update_bruteforce(brute_model, brute_count, switch_matrix7[the_important_index], '../data/rv32ui-p-lw.out')
        brute_model, brute_count = update_bruteforce(brute_model, brute_count, switch_matrix8[the_important_index], '../data/rv32ui-p-j.out')
        brute_model, brute_count = update_bruteforce(brute_model, brute_count, switch_matrix9[the_important_index], '../data/rv32ui-p-auipc.out')
        brute_model, brute_count = update_bruteforce(brute_model, brute_count, switch_matrix10[the_important_index], '../data/multiply.riscv.out')
        brute_model, brute_count = update_bruteforce(brute_model, brute_count, switch_matrix11[the_important_index], '../data/rv32ui-p-simple.out')
        result_model = np.zeros(100)
        for i in range(100):
            if (brute_count[i] == 0):
                print(i, "empty")
            else:
                result_model[i] = brute_model[i]/brute_count[i]
        estimate_switch_array = []
        for i in range(1, len(verify_sdec)):
            index = verify_sdec[i-1]*10 + verify_sdec[i]
            estimate_switch_array.append(result_model[index])
        estimate_sum = np.sum(np.array(estimate_switch_array))
        actual_sum = np.sum(np.array(switch_matrix12[the_important_index]))
        if (actual_sum == 0):
            if (estimate_sum == 0):
                tmp = 1
            else:
                tmp = 1 - estimate_sum/1000
        else:
            tmp = estimate_sum/actual_sum
        correctness[the_important_index] = tmp
    return correctness


def update_detail_bruteforce(model, count, test_array, outfile):
    test_insn_array = dump_instructions(outfile)
    test_simple = decode_simple(test_insn_array[:1000])
    test_detail = decode_detailed(test_insn_array[:1000])
    compressed_switch = post_switch_in_cycle(test_array)
    for i in range(1, min(len(test_detail), len(compressed_switch))):
        index = test_simple[i-1]*100 + test_detail[i]
        model[index] += compressed_switch[i]
        count[index] += 1
    return model, count


def brute_force_detailed_verification(switch_matrix0, switch_matrix1, switch_matrix2, switch_matrix3, switch_matrix4,
                             switch_matrix5, switch_matrix6, switch_matrix7, switch_matrix8, switch_matrix9,
                             switch_matrix10, switch_matrix11, switch_matrix12):
    verify_insn_array = dump_instructions('../data/towers.riscv.out')
    verify_simple = decode_simple(verify_insn_array[:1000])
    verify_detail = decode_detailed(verify_insn_array[:1000])
    correctness = np.zeros(407)
    for k in range(407):
        brute_model = np.zeros(1000)
        brute_count = np.zeros(1000)
        the_important_index = k
        brute_model, brute_count = update_detail_bruteforce(brute_model, brute_count, switch_matrix0[the_important_index], 'rv32ui-p-xor.out')
        brute_model, brute_count = update_detail_bruteforce(brute_model, brute_count, switch_matrix1[the_important_index], 'rv32ui-p-beq.out')
        brute_model, brute_count = update_detail_bruteforce(brute_model, brute_count, switch_matrix2[the_important_index], 'median.riscv.out')
        brute_model, brute_count = update_detail_bruteforce(brute_model, brute_count, switch_matrix3[the_important_index], 'qsort.riscv-large.out')
        brute_model, brute_count = update_detail_bruteforce(brute_model, brute_count, switch_matrix4[the_important_index], '../data/rv32ui-p-sb.out')
        brute_model, brute_count = update_detail_bruteforce(brute_model, brute_count, switch_matrix5[the_important_index], '../data/rv32ui-p-jalr.out')
        brute_model, brute_count = update_detail_bruteforce(brute_model, brute_count, switch_matrix6[the_important_index], '../data/rv32ui-p-addi.out')
        brute_model, brute_count = update_detail_bruteforce(brute_model, brute_count, switch_matrix7[the_important_index], '../data/rv32ui-p-lw.out')
        brute_model, brute_count = update_detail_bruteforce(brute_model, brute_count, switch_matrix8[the_important_index], '../data/rv32ui-p-j.out')
        brute_model, brute_count = update_detail_bruteforce(brute_model, brute_count, switch_matrix9[the_important_index], '../data/rv32ui-p-auipc.out')
        brute_model, brute_count = update_detail_bruteforce(brute_model, brute_count, switch_matrix10[the_important_index], '../data/multiply.riscv.out')
        brute_model, brute_count = update_detail_bruteforce(brute_model, brute_count, switch_matrix11[the_important_index], '../data/rv32ui-p-simple.out')
        result_model = np.zeros(1000)
        for i in range(1000):
            if (brute_count[i] == 0):
                print(i, "empty")
            else:
                result_model[i] = brute_model[i]/brute_count[i]
        estimate_switch_array = []
        for i in range(1, len(verify_detail)):
            index = verify_simple[i-1]*100 + verify_detail[i]
            estimate_switch_array.append(result_model[index])
        estimate_sum = np.sum(np.array(estimate_switch_array))
        actual_sum = np.sum(np.array(switch_matrix12[the_important_index]))
        if (actual_sum == 0):
            tmp = estimate_sum/1000
        else:
            tmp = estimate_sum/actual_sum
        correctness[the_important_index] = tmp
    return correctness

# The following codes is a helper to see the correctness
in95 = 0
in90 = 0
in80 = 0
in60 = 0
fail = 0
signal_success_index = []
signal_success_name = []
signal_6080_index = []
signal_6080_name = []
signal_fail_index = []
signal_fail_name = []
for i in range(len(correctness_array)):
    if (np.abs(1 - correctness_array[i]) < 0.05):
        in95 += 1
        signal_success_index.append(i)
        signal_success_name.append(signal_dict12[signal_array12[i]])
    elif (np.abs(1 - correctness_array[i]) < 0.1):
        in90 += 1
        signal_success_index.append(i)
        signal_success_name.append(signal_dict12[signal_array12[i]])
    elif (np.abs(1 - correctness_array[i]) < 0.2):
        in80 += 1
        signal_6080_index.append(i)
        signal_6080_name.append(signal_dict12[signal_array12[i]])
    elif (np.abs(1 - correctness_array[i]) < 0.4):
        in60 += 1
        signal_6080_index.append(i)
        signal_6080_name.append(signal_dict12[signal_array12[i]])
    else:
        fail += 1
        signal_fail_index.append(i)
        signal_fail_name.append(signal_dict12[signal_array12[i]])
