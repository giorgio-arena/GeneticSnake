import numpy as np


class Brain:

    input_nodes   = 24
    hidden1_nodes = 16
    hidden2_nodes = 8
    output_nodes  = 4

    def __init__(self):
        """
            The class Brain represents the virtual brain with which our snake's AI think.
            It is a simple feed-forward neural network with 24 inputs (the snake's visual inputs), 2 hidden layer
            of 16 and 8 nodes respectively, and 4 outputs (left, up, right, down)
            Each set of weights between two layers is represented by a matrix with (num_layer1_nodes * num_layer2_nodes)
            elements
        """

        # Initialize weights matrices randomly
        self.input_hidden1   = np.random.uniform(low=-1.0, high=1.0, size=(Brain.input_nodes, Brain.hidden1_nodes))
        self.hidden1_hidden2 = np.random.uniform(low=-1.0, high=1.0, size=(Brain.hidden1_nodes, Brain.hidden2_nodes))
        self.hidden2_output  = np.random.uniform(low=-1.0, high=1.0, size=(Brain.hidden2_nodes, Brain.output_nodes))

    def think(self, inputs):
        """
        :param inputs: Set of 24 visual inputs taken from the snake
        :return:       Next direction the snake will take (0: up, 1: down, 2: left, 3: right)

                       Activation function used: Step function (perceptron returns 1 if positve, 0 if negative)
        """
        assert len(inputs) == Brain.input_nodes

        perceptrons = np.transpose([inputs])  # Make inputs into a column so they can be multiplied to the first weights

        # Input layer -> hidden1
        perceptrons = np.sum(self.input_hidden1 * perceptrons, axis=0)  # Apply inputs to the first set of weights
        perceptrons = np.heaviside(perceptrons, 1)                      # Perform activation function
        perceptrons = np.transpose([perceptrons])                       # Make them ready to be multiplied again

        # Hidden1 -> hidden2
        perceptrons = np.sum(self.hidden1_hidden2 * perceptrons, axis=0)
        perceptrons = np.heaviside(perceptrons, 1)
        perceptrons = np.transpose([perceptrons])

        # Hidden2 -> output layer
        perceptrons = np.sum(self.hidden2_output * perceptrons, axis=0)

        return np.argmax(perceptrons)
