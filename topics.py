#!/usr/bin/env python
#
# Formulation:
#           We use a count/probability Naive Bayes approach that is similar to spam classification in this case too
#Program Working:
#               The program runs by running topics.py.
#               It takes input from the user about the mode i.e. training or testing along with a fraction.
#               The fraction given by the user contributes to the probability of supervised or unsupervised learning.
#               Each topics given in the training folder is parsed.
#               Once the file is encountered, a coin is flipped which is biased on the fraction provided by the user.
#               The coin decides whether or not the classification of that file is known or not.
#               If the classification of the file is known, the file text goes into supervised list with which a model is created.
#               In the training part the files for which the classification are unknown, the model of the supervised list is used
#               iteratively to get predictions on the unknown training data. Once our model is trained, we save the model into a
#                file.
#
#               In the testing mode, the model which we saved is loaded back into the variables and the probabilities are used to
#               predict the classification of the files.
#
#               To make the program stop quickly and to avoid unnecessary iterations, we stop the program as soon as the prior
#               probability of the unsupervised list in the training mode starts converging. By default, we have set the program to
#               stop if the difference in the prior probabilities is less than or equal to 10.


import sys
import os
import random
import EmailParser
import Model
import pprint

MODES = {"train", "test"}

try:
    mode = sys.argv[1]
    directory = sys.argv[2]
    file_path = sys.argv[3]
except IndexError:
    print("Usage: python topics.py mode dataset-directory model-file")
    sys.exit(1)
fraction=1
try:
    fraction = sys.argv[4]
except IndexError:
    pass
if mode not in MODES:
    print("Invalid mode. Allowed values: train, test")
    sys.exit(2)

if not os.path.isdir(directory):
    print("Directory" + directory + " does not exist")
    sys.exit(3)

try:
    fraction = float(fraction)
except ValueError:
    print("Fraction should be equal or between 0 and 1")
    sys.exit(4)

if fraction < 0 or fraction > 1:
    print("Fraction should be equal or between 0 and 1")
    sys.exit(5)


# Probability Coin flip function  (stack overflow)
def flip(p):
    return True if random.random() < p else False


p = EmailParser.Parser()

supervised_list = []
unsupervised_list = []
file_list = []
i = 0
dirs = []
for path, dirs, files in os.walk(directory):
    break
for folders in dirs:
    email_text = p.parse(directory + "/" + folders + "/")
    for f in email_text:
        if mode == "train":
            decision = flip(fraction)
            if decision == True:
                classification = folders
                supervised_list.append((f, folders))
            else:
                unsupervised_list.append((f, folders))
        elif mode == "test":
            unsupervised_list.append((f, folders))

# pprint.pprint(unsupervised_list)
# pprint.pprint(supervised_list)

if mode == "train":
    model = Model.Model(dirs)
    model.train(supervised_list, unsupervised_list, dirs)
    model.save(file_path)
if mode == "test":
    model = Model.Model(dirs)
    model.load(file_path)

    result_dictionary = {}
    for classes in dirs:
        result_dictionary[classes] = {"Correct": 0, "Incorrect": 0}
    successes=0
    totals=0
    predictions={}
    for email_file, topic in unsupervised_list:
        prediction = model.test(email_file, dirs)
        if prediction not in predictions:
            predictions[prediction]=0
        predictions[prediction]+=1

        if prediction != None:
            totals+=1
            if prediction == topic:
                result_dictionary[topic]['Correct'] += 1
                successes+=1
            else:
                result_dictionary[topic]['Incorrect'] += 1

    pprint.pprint(result_dictionary)
    pprint.pprint("Overall Accuracy:" +str((1.0*successes)/totals))


# Accuracy 1 - 77%
# Accuracy 0 - 3%
# Accuracy 0.3 - 71%
