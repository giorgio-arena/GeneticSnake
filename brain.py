import numpy as np
import random
import copy


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def crossover(mat_1, mat_2):
    assert mat_1.shape == mat_2.shape

    res = np.zeros(mat_1.shape)
    for index in np.ndindex(res.shape):
        probab = random.randint(0, 100)
        if probab < 50:
            res[index] = mat_1[index]
        else:
            res[index] = mat_2[index]

    return res


def mutate(arr):
    for index in np.ndindex(arr.shape):
        probab = random.randint(0, 100)
        if probab < (Brain.mutation_rate * 100):
            arr[index] = random.uniform(-1.0, 1.0)  #+= random.uniform(-Brain.mutation_quant, Brain.mutation_quant)


class Brain:
    input_nodes    = 24
    hidden1_nodes  = 16
    output_nodes   = 4
    mutation_rate  = 0.01
    mutation_quant = 0.1

    def __init__(self, brain_1=None, brain_2 = None):
        """
            The class Brain represents the virtual brain with which our snake's AI think.
            It is a simple feed-forward neural network with 24 inputs (the snake's visual inputs), 2 hidden layer
            of 16 and 8 nodes respectively, and 4 outputs (left, up, right, down)
            Each set of weights between two layers is represented by a matrix with (num_layer1_nodes * num_layer2_nodes)
            elements
        """

        if brain_1 is None and brain_2 is None:
            # Initialize weights and biases randomly
            self.input_hidden1   = np.random.uniform(low=-1.0, high=1.0, size=(Brain.input_nodes, Brain.hidden1_nodes))
            self.hidden1_output  = np.random.uniform(low=-1.0, high=1.0, size=(Brain.hidden1_nodes, Brain.output_nodes))
            self.bias_1          = np.random.uniform(low=-1.0, high=1.0, size=Brain.hidden1_nodes)
            self.bias_2          = np.random.uniform(low=-1.0, high=1.0, size=Brain.output_nodes)
        elif brain_2 is None:
            # Copy constructor
            self.input_hidden1   = copy.deepcopy(brain_1.input_hidden1)
            self.hidden1_output  = copy.deepcopy(brain_1.hidden1_output)
            self.bias_1          = copy.deepcopy(brain_1.bias_1)
            self.bias_2          = copy.deepcopy(brain_1.bias_2)
        else:
            # Crossover
            self.input_hidden1   = crossover(brain_1.input_hidden1, brain_2.input_hidden1)
            self.hidden1_output  = crossover(brain_1.hidden1_output, brain_2.hidden1_output)
            self.bias_1          = crossover(brain_1.bias_1, brain_2.bias_1)
            self.bias_2          = crossover(brain_1.bias_2, brain_2.bias_2)

    def think(self, inputs):
        """
        :param inputs: Set of 24 visual inputs taken from the snake
        :return:       Next direction the snake will take (0: up, 1: down, 2: left, 3: right)

                       Activation function used: Sigmoid function
        """
        assert len(inputs) == Brain.input_nodes

        perceptrons = np.transpose([inputs])  # Make inputs into a column so they can be multiplied to the first weights

        # Input layer -> hidden1
        perceptrons  = np.multiply(self.input_hidden1, perceptrons);     # Apply inputs to input layer
        perceptrons  = np.sum(perceptrons, axis=0)                       # Apply first set of weights
        perceptrons += self.bias_1                                       # Apply bias
        perceptrons  = sigmoid(perceptrons)                              # Perform activation function
        perceptrons  = np.transpose([perceptrons])                       # Make them ready to be multiplied again

        # Hidden1 -> output layer
        perceptrons  = np.multiply(self.hidden1_output, perceptrons);
        perceptrons  = np.sum(perceptrons, axis=0)
        perceptrons += self.bias_2
        perceptrons  = sigmoid(perceptrons)

        return np.argmax(perceptrons)

    def mutate(self):
        mutate(self.input_hidden1)
        mutate(self.bias_1)

        mutate(self.hidden1_output)
        mutate(self.bias_2)