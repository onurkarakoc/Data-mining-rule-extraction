import pandas as pd
import itertools


# Takes attributes and empty list as arguments, computes all the double and
# triple combinations. Then appends the list one by one.
# Returns combination list.
def generate_twice_and_triple_combination_of_attributes(attributes, comb_list):
    for number_of_comb in range(2, 4):
        for subset in itertools.combinations(attributes, number_of_comb):
            comb_list.append(subset)
    return comb_list


# Takes attributes, set of data and empty rules list as arguments.
# Drops all the duplicated rows from the data, so we can see all the combination
# results. Converts the achieved data to array. Rules are created.
# Returns rule list with single attribute.
def obtain_rules_with_single_attribute(attributes, data, rules):
    for element in attributes:
        manipulated_data = data[[element, 'Class']].drop_duplicates().to_numpy()
        for row in manipulated_data:
            rules.append(element + "=" + row[0] + "->" + row[1])
    return rules


# Takes twice and triple combinations of attributes, set of data and set of rules
# as arguments. Drops all the duplicated rows from the data, so we can see all the
# combination results. Converts achieved data to array. Rules are appended to list of rule
# set. Returns rule list.
def obtain_rules_with_twice_triple_attributes(combinations, data, rules):
    for combination in combinations:
        if len(combination) == 2:
            manipulated_data = data[[combination[0], combination[1], 'Class']].drop_duplicates().to_numpy()
            for row in manipulated_data:
                rules.append(combination[0] + "=" + row[0] + "^" + combination[1] + "=" + row[1] + "->" + row[2])
        elif len(combination) == 3:
            manipulated_data = data[
                [combination[0], combination[1], combination[2], 'Class']].drop_duplicates().to_numpy()
            for row in manipulated_data:
                rules.append(
                    combination[0] + "=" + row[0] + "^" + combination[1] + "=" + row[1] + "^" + combination[2] + "=" +
                    row[2] + "->" + row[3])
    return rules


# Rules are splitted according the appropriate conditions. First, split the rule as condition and
# result. Then split the condition.
# Takes rule set, data and a list as arguments. Computes the coverage value, then rule and coverage value added to list.
# Returns the list.
# Note: Coverage and accuracy functions implemented as independent functions in order to use them for different
# purpose in the future.
def coverage(rules, data, coverage_list):
    print("Coverage percentage of rules:")
    for element in rules:
        without_class = element.split('->')
        if "^" in element:
            attributes = without_class[0].split('^')
            manipulated_data = data
            for attribute in attributes:
                attribute = attribute.split('=')
                manipulated_data = manipulated_data[manipulated_data[attribute[0]] == attribute[1]]
        else:
            attribute = without_class[0].split('=')
            manipulated_data = data[data[attribute[0]] == attribute[1]]
        coverage_list.append([element, manipulated_data.shape[0] / data.shape[0] * 100 ])
    coverage_list.sort(key=take_second, reverse=True)
    return coverage_list


# Just like coverage. Implementation is almost the same.
# Just computation is different.
def accuracy(rules, data, accuracy_list):
    print("Accuracy percentage of rules:")
    for element in rules:
        split_class = element.split('->')
        if "^" in element:
            attributes = split_class[0].split('^')
            manipulated_data = data
            for attribute in attributes:
                attribute = attribute.split('=')
                manipulated_data = manipulated_data[manipulated_data[attribute[0]] == attribute[1]]
        else:
            attribute = split_class[0].split('=')
            manipulated_data = data[data[attribute[0]] == attribute[1]]
        accuracy_list.append([element, manipulated_data[manipulated_data["Class"] == split_class[1]].shape[0] / manipulated_data.shape[0] * 100 ])
    accuracy_list.sort(key=take_second, reverse=True)
    return accuracy_list


# Helper function for sort function.
def take_second(element):
    return element[1]


vertebrates_data = pd.read_csv("/Users/onurkarakoc/Desktop/vertebrates.csv")
print(vertebrates_data)
# Is there any null value
print("Number of null values of attributes:")
print(vertebrates_data.isnull().sum())
# Number of classes
print("Number of classes:", vertebrates_data['Class'].nunique())
# Number of attributes
vertebrates_data_without_name_and_class = vertebrates_data.iloc[:, 1:5]
attribute_list = list(vertebrates_data_without_name_and_class)
print("Number of attributes:", len(attribute_list))
# Twice and triple combinations of attributes
combination_list = []
print("Twice and triple combination of attributes: ")
combination_list = generate_twice_and_triple_combination_of_attributes(attribute_list, combination_list)
print(combination_list)
rule_set = []
rule_set = obtain_rules_with_single_attribute(attribute_list, vertebrates_data, rule_set)
# Print rules with single attribute one by one
print("Rules with single attribute:")
for rule in rule_set:
    print(rule)
rule_set = obtain_rules_with_twice_triple_attributes(combination_list, vertebrates_data, rule_set)
# Print total rule count
print("Total rule count:", len(rule_set))
# Print all of the rules one by one
print("----------All Rules----------")
for rule in rule_set:
    print(rule)
coverage_rules = []
# Coverage percentage of every rule will be printed.
coverage_rules = coverage(rule_set, vertebrates_data, coverage_rules)
for coverage_rule in coverage_rules:
    print("Coverage percentage of", coverage_rule[0], coverage_rule[1], "%")
accuracy_rules = []
# Accuracy percentage of every rule will be printed.
accuracy_rules = accuracy(rule_set, vertebrates_data, accuracy_rules)
for accuracy_rule in accuracy_rules:
    print("Accuracy percentage of", accuracy_rule[0], accuracy_rule[1], "%")