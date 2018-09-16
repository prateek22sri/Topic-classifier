# Topic-classifier

### Formulation:
We use a count/probability Naive Bayes approach that is similar to spam classification in this implementation

### Program Working:

The program runs by running topics.py.
It takes input from the user about the mode i.e. training or testing along with a fraction.
The fraction given by the user contributes to the probability of supervised or unsupervised learning.
Each topics given in the training folder is parsed.
Once the file is encountered, a coin is flipped which is biased on the fraction provided by the user.
The coin decides whether or not the classification of that file is known or not.
If the classification of the file is known, the file text goes into supervised list with which a model is created.
In the training part the files for which the classification are unknown, the model of the supervised list is used
iteratively to get predictions on the unknown training data. Once our model is trained, we save the model into a
file.
In the testing mode, the model which we saved is loaded back into the variables and the probabilities are used to
predict the classification of the files.

To make the program stop quickly and to avoid unnecessary iterations, we stop the program as soon as the prior
probability of the unsupervised list in the training mode starts converging. By default, we have set the program to
stop if the difference in the prior probabilities is less than or equal to 10.
