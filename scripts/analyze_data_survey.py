import csv
import codecs
import json

def check_reason_no_tv(row, data):
    if row[8] == "2":
        data['Reasons_TV_no']["too_expensive"] += 1
    if row[9] == "2":
        data['Reasons_TV_no']["no_time"] += 1
    if row[10] == "2":
        data['Reasons_TV_no']["not_interesting"] += 1
    if row[11] == "2":
        data['Reasons_TV_no']["privacy"] += 1
    if row[12] == "2":
        data['Reasons_TV_no']["security"] += 1
    if row[13] == "2":
        data['Reasons_TV_no']["want_to_buy"] += 1
    if row[14] == "2":
        data['Reasons_TV_no']["reason_not_specified"] += 1
    if row[15] == "2":
        data['Reasons_TV_no']["other"].append(row[16])

def can_use_internet_connection(row, data):
    answer = row[17]
    #{'yes_smart_tv': 0, 'yes_satellitar': 0, 'yes_do_not_know_the_name': 0, 'do_not_know': 0, 'no': 0}
    if answer == "1":
        data["can_use_internet"]["yes_smart_tv"] += 1
    elif answer == "2":
        data["can_use_internet"]["yes_satellitar"] += 1
    elif answer == "3":
        data["can_use_internet"]["yes_do_not_know_the_name"] += 1
    elif answer == "4":
        data["can_use_internet"]["do_not_know"] += 1
    elif answer == "5":
        data["can_use_internet"]["no"] += 1
    else:
        data["can_use_internet"]["no_answer"] += 1

def yes_no_maybe_answers(field, element_in_row, data):
    if element_in_row == "1":
        data[field]["yes"] += 1
    elif element_in_row == "2":
        data[field]["maybe"] += 1
    elif element_in_row == "3":
        data[field]["no"] += 1
    else:
        data[field]["no_answer"] += 1

def yes_no_maybe_answers_order_modified(field, element_in_row, data):
    if element_in_row == "1":
        data[field]["yes"] += 1
    elif element_in_row == "3":
        data[field]["maybe"] += 1
    elif element_in_row == "2":
        data[field]["no"] += 1
    else:
        data[field]["no_answer"] += 1

def yes_no_answers(field, element_in_row, data):
    if element_in_row == "1":
        data[field]["yes"] += 1
    elif element_in_row == "2":
        data[field]["no"] += 1
    else:
        data[field]["no_answer"] += 1

def check_preconditions(row):
    if (row[19] == "3"):
        return False
    if (row[6] == "2" and row [13] != "2"):
        return False
    return True

def security_problems_list_and_measures(field_1, field_2, element_in_row, starting_point, data):
    number_of_identified_risks = element_in_row

    data[field_1][number_of_identified_risks] += 1

    iterations = int(number_of_identified_risks)
    while (iterations > 0):
        starting_point += 1
        data[field_2].append(row[starting_point])
        iterations -= 1

def where_do_messages_come_from(row, data):
    if(row[54] == '1'):
        data['where_it_comes_from']['internet'] += 1
    elif (row[54] == '2'):
        data['where_it_comes_from']['tv_signal'] += 1
    elif (row[54] == '3'):
        data['where_it_comes_from']['both'] += 1
    elif (row[54] == '4'):
        data['where_it_comes_from']['no_idea'] += 1

def problems_linked_to_hbbtv(row, data):
    answer = row[55]
    if answer == "1":
        data['problems']['yes_security'] += 1
    elif answer == "2":
        data['problems']['yes_privacy'] += 1
    elif answer == "6":
        data['problems']['both'] += 1
    elif answer == "3":
        data['problems']['maybe'] += 1
    elif answer == "5":
        data['problems']['no'] += 1

def read_privacy_policy(row, data):
    answer = row [38]
    if answer == "1":
        data["read_privacy_policy"]["always"] += 1
    elif answer == "2":
        data["read_privacy_policy"]["most_times"] += 1
    elif answer == "3":
        data["read_privacy_policy"]["some_times"] += 1
    elif answer == "4":
        data["read_privacy_policy"]["rarely"] += 1
    elif answer == "5":
        data["read_privacy_policy"]["never"] += 1

def easy_to_read(row, data):
    answer = row [39]
    if answer == "1":
        data["easy_to_read"]["always"] += 1
    elif answer == "2":
        data["easy_to_read"]["most_times"] += 1
    elif answer == "3":
        data["easy_to_read"]["some_times"] += 1
    elif answer == "4":
        data["easy_to_read"]["never"] += 1
    elif answer == "5":
        data["easy_to_read"]["not_read"] += 1

def get_collected_data(element, data):
    if element != "":
        data["collected_data"].append(element)

def get_gender(element, data):
    if element == "1":
        data["gender"]["female"] += 1
    elif element == "2":
        data["gender"]["male"] += 1
    else:
        data["gender"]["other"] += 1

def get_matrix_choice(row, data):
    answer = row[36]
    if answer == "1":
        data["choice_matrix"]["1"] += 1
    elif answer == "2":
        data["choice_matrix"]["2"] += 1
    elif answer == "3":
        data["choice_matrix"]["3"] += 1
    elif answer == "4":
        data["choice_matrix"]["4"] += 1
    elif answer == "5":
        data["choice_matrix"]["5"] += 1

def analyze_scenario(element_risk, element_explanation, data_risk, data_explanation):
    if element_risk == "1":
        data_risk["1"] += 1
    elif element_risk == "2":
        data_risk["2"] += 1
    elif element_risk == "3":
        data_risk["3"] += 1
    elif element_risk == "4":
        data_risk["4"] += 1
    elif element_risk == "5":
        data_risk["5"] += 1
    
    data_explanation.append(element_explanation)

f = codecs.open("data_survey_2.csv", "r", "utf-16")

reader = csv.reader(f, delimiter="\t")

#skip header
next(reader)
#skip two test cases
next(reader)
next(reader)

data_first_page = {"TV_yes": 0, "TV_no": 0, "Reasons_TV_no": {"too_expensive": 0, "no_time": 0, "not_interesting": 0, "privacy": 0, "security": 0, "want_to_buy": 0, "reason_not_specified": 0, "other": []}, "can_use_internet": {'yes_smart_tv': 0, 'yes_satellitar': 0, 'yes_do_not_know_the_name': 0, 'do_not_know': 0, 'no': 0, "no_answer": 0}, "do_use_internet": {"yes": 0, "maybe": 0, "no": 0, "no_answer": 0}, "would_use_internet": {"yes": 0, "maybe": 0, "no": 0, "no_answer": 0}}

data_second_page = {"aware_of_security_and_privacy_risks": {"yes": 0, "no": 0, "no_answer": 0}, "identified_risks": [], "number_of_identified_risks_per_person": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0}, "security_measures": [], "number_of_security_measures_per_person": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0}}

data_third_page = {"have_seen_hbbtv_notifications": {"yes": 0, "no": 0, "maybe": 0, "no_answer": 0}, "where_it_comes_from": {"internet": 0, "tv_signal":0, "both": 0, "no_idea": 0}, "problems": {"yes_security": 0, "yes_privacy": 0, "both": 0, "maybe":0, "no": 0}}

data_fourth_page_1 = {"scenario_1": {"risk": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}, "explanation": []}, "scenario_2": {"risk": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}, "explanation": []}, "scenario_3": {"risk": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}, "explanation": []}, "scenario_4": {"risk": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}, "explanation": []}}

data_fourth_page_2 = {"scenario_5": {"risk": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}, "explanation": []}, "scenario_6": {"risk": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}, "explanation": []}, "scenario_7": {"risk": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}, "explanation": []}, "scenario_8": {"risk": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}, "explanation": []}}

data_fifth_page = {"read_privacy_policy": {"always": 0, "most_times": 0, "some_times": 0, "rarely": 0, "never": 0}, "easy_to_read": {"always": 0, "most_times": 0, "some_times": 0, "never": 0, "not_read": 0}, "privacy_policy_on_tv": {"yes": 0, "no": 0, "maybe": 0}, "read_privacy_policy_tv": {"yes": 0, "no": 0, "no_answer": 0}, "collected_data": []}

data_sixth_page = {"choice_matrix": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}, "important_features": []}

data_seventh_page = {"ages": [], "gender": {"male": 0, "female": 0, "other": 0}, "expertise": []}

for row in reader:
    #the participant owns a TV
    if row[6] == "1":
        data_first_page['TV_yes'] += 1
        #check whether they can use internet on their TV
        can_use_internet_connection(row, data_first_page)
        #check if they actually use internet on their TV
        yes_no_maybe_answers("do_use_internet", row[18], data_first_page)
        #check whether they would like to use internet features if their TV supported them
        yes_no_maybe_answers("would_use_internet", row[19], data_first_page)

    #the participant does not own a TV
    elif row[6] == "2":
        data_first_page["TV_no"] +=1
        check_reason_no_tv(row, data_first_page)

    #check if preconditions are met
    if check_preconditions(row):
        #2nd page
        yes_no_answers("aware_of_security_and_privacy_risks", row[43], data_second_page)
        security_problems_list_and_measures("number_of_identified_risks_per_person", "identified_risks", row[44], 44, data_second_page)
        security_problems_list_and_measures("number_of_security_measures_per_person", "security_measures", row[49], 49, data_second_page)

        #3rd page
        yes_no_maybe_answers("have_seen_hbbtv_notifications", row[53], data_third_page)
        where_do_messages_come_from(row, data_third_page)
        problems_linked_to_hbbtv(row, data_third_page)

        #4th page
        #scenario 1
        analyze_scenario(row[20], row[28], data_fourth_page_1["scenario_1"]["risk"], data_fourth_page_1["scenario_1"]["explanation"])
        #scenario 2        
        analyze_scenario(row[21], row[29], data_fourth_page_1["scenario_2"]["risk"], data_fourth_page_1["scenario_2"]["explanation"])
        #scenario 3        
        analyze_scenario(row[22], row[30], data_fourth_page_1["scenario_3"]["risk"], data_fourth_page_1["scenario_3"]["explanation"])
        #scenario 4        
        analyze_scenario(row[23], row[31], data_fourth_page_1["scenario_4"]["risk"], data_fourth_page_1["scenario_4"]["explanation"])
        #scenario 5
        analyze_scenario(row[24], row[32], data_fourth_page_2["scenario_5"]["risk"], data_fourth_page_2["scenario_5"]["explanation"])
        #scenario 6
        analyze_scenario(row[25], row[33], data_fourth_page_2["scenario_6"]["risk"], data_fourth_page_2["scenario_6"]["explanation"])
        #scenario 7
        analyze_scenario(row[26], row[34], data_fourth_page_2["scenario_7"]["risk"], data_fourth_page_2["scenario_7"]["explanation"])
        #scenario 8
        analyze_scenario(row[27], row[35], data_fourth_page_2["scenario_8"]["risk"], data_fourth_page_2["scenario_8"]["explanation"])

        #5th page
        read_privacy_policy(row, data_fifth_page)
        easy_to_read(row, data_fifth_page)
        yes_no_maybe_answers_order_modified("privacy_policy_on_tv", row[40], data_fifth_page)
        yes_no_answers("read_privacy_policy_tv", row[41], data_fifth_page)
        get_collected_data(row[42], data_fifth_page)

        #6th page
        get_matrix_choice(row, data_sixth_page)
        if (row[37] != ""):
            data_sixth_page["important_features"].append(row[37])

    #7th page
    data_seventh_page["ages"].append(int(row[56]))
    get_gender(row[57], data_seventh_page)
    data_seventh_page['expertise'].append(row[58])


#TODO
def check_reason_no_tv(row, data):
    if row[58] == "2":
        data['Reasons_TV_no']["too_expensive"] += 1
    if row[59] == "2":
        data['Reasons_TV_no']["no_time"] += 1
    if row[60] == "2":
        data['Reasons_TV_no']["not_interesting"] += 1
    if row[61] == "2":
        data['Reasons_TV_no']["privacy"] += 1
    if row[62] == "2":
        data['Reasons_TV_no']["security"] += 1
    if row[63] == "2":
        data['Reasons_TV_no']["want_to_buy"] += 1
    if row[64] == "2":
        data['Reasons_TV_no']["reason_not_specified"] += 1
    if row[65] == "2":
        data['Reasons_TV_no']["other"].append(row[66])

def can_use_internet_connection(row, data):
    answer = row[67]
    #{'yes_smart_tv': 0, 'yes_satellitar': 0, 'yes_do_not_know_the_name': 0, 'do_not_know': 0, 'no': 0}
    if answer == "1":
        data["can_use_internet"]["yes_smart_tv"] += 1
    elif answer == "2":
        data["can_use_internet"]["yes_satellitar"] += 1
    elif answer == "3":
        data["can_use_internet"]["yes_do_not_know_the_name"] += 1
    elif answer == "4":
        data["can_use_internet"]["do_not_know"] += 1
    elif answer == "5":
        data["can_use_internet"]["no"] += 1
    else:
        data["can_use_internet"]["no_answer"] += 1

def check_preconditions(row):
    if (row[69] == "3"):
        return False
    if (row[56] == "2" and row [63] != "2"):
        return False
    return True

def where_do_messages_come_from(row, data):
    if(row[12] == '1'):
        data['where_it_comes_from']['internet'] += 1
    elif (row[12] == '2'):
        data['where_it_comes_from']['tv_signal'] += 1
    elif (row[12] == '3'):
        data['where_it_comes_from']['both'] += 1
    elif (row[12] == '4'):
        data['where_it_comes_from']['no_idea'] += 1

def problems_linked_to_hbbtv(row, data):
    answer = row[13]
    if answer == "1":
        data['problems']['yes_security'] += 1
    elif answer == "2":
        data['problems']['yes_privacy'] += 1
    elif answer == "6":
        data['problems']['both'] += 1
    elif answer == "3":
        data['problems']['maybe'] += 1
    elif answer == "5":
        data['problems']['no'] += 1

def read_privacy_policy(row, data):
    answer = row [51]
    if answer == "1":
        data["read_privacy_policy"]["always"] += 1
    elif answer == "2":
        data["read_privacy_policy"]["most_times"] += 1
    elif answer == "3":
        data["read_privacy_policy"]["some_times"] += 1
    elif answer == "4":
        data["read_privacy_policy"]["rarely"] += 1
    elif answer == "5":
        data["read_privacy_policy"]["never"] += 1

def easy_to_read(row, data):
    answer = row [52]
    if answer == "1":
        data["easy_to_read"]["always"] += 1
    elif answer == "2":
        data["easy_to_read"]["most_times"] += 1
    elif answer == "3":
        data["easy_to_read"]["some_times"] += 1
    elif answer == "4":
        data["easy_to_read"]["never"] += 1
    elif answer == "5":
        data["easy_to_read"]["not_read"] += 1

def get_matrix_choice(row, data):
    answer = row[9]
    if answer == "1":
        data["choice_matrix"]["1"] += 1
    elif answer == "2":
        data["choice_matrix"]["2"] += 1
    elif answer == "3":
        data["choice_matrix"]["3"] += 1
    elif answer == "4":
        data["choice_matrix"]["4"] += 1
    elif answer == "5":
        data["choice_matrix"]["5"] += 1

#read data from 2022
f = codecs.open("data_2022/data_hbbtv-privacy_2022-11-15_15-44.csv", "r", "utf-16")

reader = csv.reader(f, delimiter="\t")

#skip header
next(reader)
next(reader)
#skip two test cases
next(reader)

for row in reader:
    #the participant owns a TV
    if row[56] == "1":
        data_first_page['TV_yes'] += 1
        #check whether they can use internet on their TV
        can_use_internet_connection(row, data_first_page)
        #check if they actually use internet on their TV
        yes_no_maybe_answers("do_use_internet", row[68], data_first_page)
        #check whether they would like to use internet features if their TV supported them
        yes_no_maybe_answers("would_use_internet", row[69], data_first_page)

    #the participant does not own a TV
    elif row[56] == "2":
        data_first_page["TV_no"] +=1
        check_reason_no_tv(row, data_first_page)

    #check if preconditions are met
    if check_preconditions(row):
        #2nd page
        yes_no_answers("aware_of_security_and_privacy_risks", row[39], data_second_page)
        security_problems_list_and_measures("number_of_identified_risks_per_person", "identified_risks", row[40], 40, data_second_page)
        security_problems_list_and_measures("number_of_security_measures_per_person", "security_measures", row[45], 45, data_second_page)

        #3rd page
        yes_no_maybe_answers("have_seen_hbbtv_notifications", row[11], data_third_page)
        where_do_messages_come_from(row, data_third_page)
        problems_linked_to_hbbtv(row, data_third_page)

        #4th page
        #scenario 1
        analyze_scenario(row[23], row[31], data_fourth_page_1["scenario_1"]["risk"], data_fourth_page_1["scenario_1"]["explanation"])
        #scenario 2        
        analyze_scenario(row[24], row[32], data_fourth_page_1["scenario_2"]["risk"], data_fourth_page_1["scenario_2"]["explanation"])
        #scenario 3        
        analyze_scenario(row[25], row[33], data_fourth_page_1["scenario_3"]["risk"], data_fourth_page_1["scenario_3"]["explanation"])
        #scenario 4        
        analyze_scenario(row[26], row[34], data_fourth_page_1["scenario_4"]["risk"], data_fourth_page_1["scenario_4"]["explanation"])
        #scenario 5
        analyze_scenario(row[27], row[35], data_fourth_page_2["scenario_5"]["risk"], data_fourth_page_2["scenario_5"]["explanation"])
        #scenario 6
        analyze_scenario(row[28], row[36], data_fourth_page_2["scenario_6"]["risk"], data_fourth_page_2["scenario_6"]["explanation"])
        #scenario 7
        analyze_scenario(row[29], row[37], data_fourth_page_2["scenario_7"]["risk"], data_fourth_page_2["scenario_7"]["explanation"])
        #scenario 8
        analyze_scenario(row[30], row[38], data_fourth_page_2["scenario_8"]["risk"], data_fourth_page_2["scenario_8"]["explanation"])

        #5th page
        read_privacy_policy(row, data_fifth_page)
        easy_to_read(row, data_fifth_page)
        yes_no_maybe_answers_order_modified("privacy_policy_on_tv", row[53], data_fifth_page)
        yes_no_answers("read_privacy_policy_tv", row[54], data_fifth_page)
        get_collected_data(row[55], data_fifth_page)

        #6th page
        get_matrix_choice(row, data_sixth_page)
        if (row[10] != ""):
            data_sixth_page["important_features"].append(row[10])

    #7th page
    data_seventh_page["ages"].append(int(row[6]))
    get_gender(row[7], data_seventh_page)
    data_seventh_page['expertise'].append(row[8])

#merge together the dictionaries of the different pages
data_all = {}
data_all.update(data_first_page)
data_all.update(data_second_page)
data_all.update(data_third_page)

#merge data from 4th page
data_fourth_page = {}
data_fourth_page.update(data_fourth_page_1)
data_fourth_page.update(data_fourth_page_2)

data_all.update(data_fourth_page)
data_all.update(data_fifth_page)
data_all.update(data_sixth_page)
data_all.update(data_seventh_page)

#Print all data
#print(json.dumps(data_all, indent=4))

#write all data in the different files
with open('data_first_page_merged.json', 'w') as first_page:
    json.dump(data_first_page, first_page)

with open('data_second_page_merged.json', 'w') as second_page:
    json.dump(data_second_page, second_page)

with open('data_third_page_merged.json', 'w') as third_page:
    json.dump(data_third_page, third_page)

with open('data_fourth_page_merged.json', 'w') as fourth_page:
    json.dump(data_fourth_page, fourth_page)

with open('data_fifth_page_merged.json', 'w') as fifth_page:
    json.dump(data_fifth_page, fifth_page)

with open('data_sixth_page_merged.json', 'w') as sixth_page:
    json.dump(data_sixth_page, sixth_page)

with open('data_seventh_page_merged.json', 'w') as seventh_page:
    json.dump(data_seventh_page, seventh_page)

with open('data_all_merged.json', 'w') as data_all_page:
    json.dump(data_all, data_all_page)