import csv
import requests
import json
import matplotlib.pyplot as plt


#funtcion to put data from csv or json into a list
def get_data_from_file(fn, format=""):

    lst = []
    f = open(fn, 'r')

    if format == 'csv' or 'csv' in fn:
        reader = csv.reader(f)

        for row in reader:
            lst.append(row)

    elif format == 'json' or 'json' in fn:
        contents = json.load(f)

        for i in contents:
            lst.append(i)

    return lst


# function retreive data from a url website
def get_data_from_internet(url, format='json'):
    if format == 'csv' or 'csv' in url:
        pass

    if format == 'json' or 'json' in url:
        f = requests.get(url)
        contents = f.json()
        return contents


# function to retreive the index of a column from the tax data
def get_index_for_column_label(header_row, column_label):
    index = header_row.index(column_label)
    return index


# fucntion to return the abbreviation of a state using its name
def get_state_abbreviation(state_names, state_code):
    for state in state_names:
        if state.get('name') == state_code:
            return state.get('abbreviation')


# fucntion to return the name of a state using its abbreviation
def get_state_name(state_names, state_code):
    for state in state_names:
        if state.get('abbreviation') == state_code:
            return state.get('name')


# fuction to retreive the population of a state
def get_state_population(state_populations, state_name):
    statename = '.' + state_name
    for state in state_populations:
        if statename in state:
            return state[statename]


def main():

    # defines the list that will hold all of the gathered information on the state
    answers = []

    # defines list for data in csv
    returns_data = get_data_from_file("tax_return_data_2018.csv")

    # defines list for data in json
    states = get_data_from_file("states_titlecase.json")

    # defines list for data from the internet
    populations = get_data_from_internet(
        "https://raw.githubusercontent.com/heymrhayes/class_files/main/state_populations_2018.txt"
    )

    #input and conversion
    print('Please enter the name of the state you would like information on.')
    state_input = input()
    state = get_state_abbreviation(states, state_input)

    # defines the states number in the returns data list to narow down the amount of data being sorted through
    for i in returns_data:
        if state in i:
            state_number = i[0]

            #BEGGINING OF FINDING NEW DATA

    # Find the average taxable icome per return across all groups within the state
    t = 0
    y = 0
    for i in returns_data[1::]:
        t += int(i[96])
        y += int(i[4])
    ans1 = round(t / y * 1000)
    print('Average taxable icome per return across all groups')
    print(' ')
    print(" ${:8.0f}".format(ans1))
    print(' ')
    print(' ')
    answers.append('Average taxable icome per return across all groups\n')
    answers.append(" ${:8.0f}".format(ans1) + '\n')

    # Find the average taxable income per return for each AGI group within the state
    print('average taxable income per return for each AGI group')
    answers.append('Average taxable income per return for each AGI group\n')
    print(' ')
    z = 1
    while z < 7:
        x = 0
        y = 0
        for i in returns_data[1::]:
            if i[3] == str(z):
                x += int(i[96])
                y += int(i[4])
        ans2 = round(x / y * 1000)
        group = 'Group' + str(z)
        answers.append(group + ": ${:8.0f}".format(ans2) + '\n')
        print('Group', str(z) + ": ${:8.0f}".format(ans2))
        z += 1
    print(' ')
    print(' ')

    #Find the average taxable income (per resident) per state (all states not just the given one)
    print('Average taxable income (per resident) per state')
    answers.append('average taxable income (per resident) per state\n')
    print(' ')
    f = 0
    answer_103 = []
    answer_103_2 = []
    count = 0
    for i in returns_data[0::5]:
        income = 0
        if i[0] != 'STATEFIPS' and i[0] != '49':
            for a in returns_data:
                if i[1] in a:
                    income += int(a[96])
            pop_name = get_state_name(states, i[1])
            pop = get_state_population(populations, pop_name)

            ans3 = (round(income / pop * 1000))
            answer_103.append(ans3)
            answer_103_2.append(states[f]['abbreviation'])
            answers.append(states[f]['abbreviation'] +
                           ": ${:8.0f}".format(ans3) + '\n')
            print(states[f]['abbreviation'] + ":  ${:8.0f}".format(ans3))
            f += 1

    print(' ')
    print(' ')

    #Find the average taxable income across all groups within the state
    o = 0
    p = 0
    for i in returns_data[1::]:
        if i[0] == state_number:
            o += int(i[96])
            p += int(i[4])
    print('Average taxable income across all groups')
    print(' ')
    ans4 = round(o / p * 1000)
    answers.append('average taxable income across all groups\n')
    answers.append(" ${:8.0f}".format(ans4) + '\n')
    print(" ${:8.0f}".format(ans4))
    print(' ')
    print(' ')

    #Find the average taxable income per return for each AGI group within the state
    print('Average taxable income per return for each AGI group')
    answers.append('average taxable income per return for each AGI group\n')
    print(' ')
    s = 1
    while s < 7:
        x = 0
        y = 0
        for i in returns_data[1::]:
            if i[0] == state_number:
                if i[3] == str(s):
                    x += int(i[96])
                    y += int(i[4])
        ans5 = round(x / y * 1000)
        group = 'Group' + str(s)
        answers.append(group + ": ${:8.0f}".format(ans5) + '\n')
        print('Group', str(s) + ": ${:8.0f}".format(ans5))
        s += 1
    print(' ')
    print(' ')

    #Find the average dependents per return for each agi group within the state
    print('Average dependents per return for each agi group')
    answers.append('average dependents per return for each agi group\n')
    print(' ')
    count = 1
    while count < 7:
        numdep = 0
        numret = 0
        for i in returns_data[1::]:
            if i[0] == state_number:
                if i[3] == str(count):
                    numdep += int(i[13])
                    numret += int(i[4])
        ans6 = numdep / numret
        group = 'Group' + str(count)
        answers.append(group + ": {:8.2f}".format(ans6) + '\n')
        print('Group', str(count) + ": {:8.2f}".format(ans6))
        count += 1
    print(' ')
    print(' ')

    #Find the percentage of returns with no taxable income for each agi group within the state
    print('Percentage of returns with no taxable income for each agi group')
    answers.append(
        'percentage of returns with no taxable income for each agi group\n')
    print(' ')
    count = 1
    while count < 7:
        numret = 0
        for i in returns_data[1::]:
            if i[0] == state_number:
                if i[3] == str(count):
                    numret = int(i[4]) - int(i[95])
                    tret = int(i[4])
        ans7 = numret / tret * 100
        group = 'Group' + str(count)
        answers.append(group + ": {:8.2f}%".format(ans7) + '\n')
        print('Group', str(count) + ": {:8.2f}%".format(ans7))
        count += 1
    print(' ')
    print(' ')

    #Find the average taxable income per resident within the state
    print('Average taxable income per resident')
    answers.append('average taxable income per resident\n')
    print(' ')
    g = 0
    pop = get_state_population(populations, state_input)
    for i in returns_data[1::]:
        if i[0] == state_number:
            g += int(i[96])
    ans8 = round(g / pop * 1000)
    answers.append(" ${:8.0f}".format(ans8) + '\n')
    print(" ${:8.0f}".format(ans8))
    print(' ')
    print(' ')

    #Find the percentage of returns for each agi group within the state
    print('Percentage of returns for each agi group')
    answers.append('percentage of returns for each agi group\n')
    print(' ')
    ans102 = []
    count = 1
    while count < 7:
        numret = 0
        for i in returns_data[1::]:
            if i[0] == state_number:
                if i[3] == str(count):
                    numret += int(i[4])
        ans9 = numret / p * 100
        ans102.append(ans9)
        group = 'Group' + str(count)
        answers.append(group + ": {:8.2f}%".format(ans9) + '\n')
        print('Group', str(count) + ": {:8.2f}%".format(ans9))
        count += 1
    print(' ')
    print(' ')

    #Find the percentage of taxable income for each agi group within the state
    print('Question ten')
    answers.append('Question 10\n')
    answers.append('percentage of taxable income for each agi group\n')
    print(' ')
    ans101 = []
    s = 1
    while s < 7:
        x = 0
        y = 0
        for i in returns_data[1::]:
            if i[0] == state_number:
                if i[3] == str(s):
                    x += int(i[96])
                y += int(i[96])
        ans10 = round(x / y * 100, 2)
        print('Group', str(s) + ": {:8.2f}%".format(ans10))
        group = 'Group' + str(s)
        answers.append(group + ": {:8.2f}%".format(ans10) + '\n')
        s += 1
        ans101.append(ans10)
        count += 1
    print(' ')
    print(' ')

    print(answers)

    #Creates a bar chart to compare the taxable income for each agi group within the state using data gathered earlier in the program. Will be in a file after run
    labels = [
        "Group 1",
        "Group 2",
        "Group 3",
        "Group 4",
        "Group 5",
        "Group 6",
    ]
    plt.figure(figsize=(10, 8))
    plt.title("Percentage of returns for each agi group")
    plt.pie(ans101,
            labels=labels,
            autopct='%1.0f%%',
            pctdistance=1.1,
            labeldistance=1.2)

    # svaes chart to file
    plt.savefig('pie1.' + state + '.png')
    plt.clf()

    #creates a pie chart to compare the percentage of returns for each agi group within the state using data gathered earlier in the program. Will be in a file after run
    labels = [
        "Group 1",
        "Group 2",
        "Group 3",
        "Group 4",
        "Group 5",
        "Group 6",
    ]
    plt.figure(figsize=(10, 8))
    plt.title("Percentage of taxable income for each agi group")
    plt.pie(ans102,
            labels=labels,
            autopct='%1.0f%%',
            pctdistance=1.1,
            labeldistance=1.2)

    # saves chart to file
    plt.savefig('pie2.' + state + '.png')
    plt.clf()

    #Creates a vertical bar chart to compare the average texable income per resident per state using data gathered earlier in the program. Will be in a file affter run

    plt.bar(answer_103_2, answer_103, label="Data")
    plt.legend()

    plt.xlabel('State')
    plt.ylabel('avergae taxable income')
    plt.title('Average taxable income per resident per state')

    # saves chart to file
    plt.savefig('bar.' + state + '.png')

    #saves all of the gathered data to a file withe explanations and formating
    f = open('answers' + state + '.txt', 'w')
    for i in answers:
        f.write(str(i) + '/n')
    f.close()


main()  #end of program
