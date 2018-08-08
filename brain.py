import numpy as np

class Brain:
    def __init__(self):
        """
            The class Brain represents the virtual brain with which our snake's AI think.
            It is a simple feed-forward neural network with 24 inputs (the snake's visual inputs), 2 hidden layer
            of 16 and 8 nodes respectively, and 4 outputs (left, up, right, down)
            Each set of weights between two layers is represented by a matrix with (num_layer1_nodes * num_layer2_nodes)
            elements
        """

        self.input_nodes   = 24
        self.hidden1_nodes = 16
        self.hidden2_nodes = 8
        self.output_nodes  = 4

        self.input_hidden1_mat   = np.random.uniform(low=-1.0, high=1.0, size=(self.input_nodes, self.hidden1_nodes))
        self.hidden1_hidden2_mat = np.random.uniform(low=-1.0, high=1.0, size=(self.hidden1_nodes, self.hidden2_nodes))
        self.hidden2_output_mat  = np.random.uniform(low=-1.0, high=1.0, size=(self.hidden2_nodes, self.output_nodes))

    def think(self, inputs):
        """
        :param inputs: TODO
        :return: TODO

                Activation function used: Step function (perceptron returns 1 if positve, 0 if negative)
        """
        assert len(inputs) == self.input_nodes

        perceptrons = np.transpose([inputs])

        # Input layer -> hidden1
        perceptrons = np.sum(self.input_hidden1_mat * perceptrons, axis=0)
        perceptrons = np.heaviside(perceptrons, 1)
        perceptrons = np.transpose([perceptrons])

        # Hidden1 -> hidden2
        perceptrons = np.sum(self.hidden1_hidden2_mat * perceptrons, axis=0)
        perceptrons = np.heaviside(perceptrons, 1)
        perceptrons = np.transpose([perceptrons])

        # Hidden2 -> output layer
        perceptrons = np.sum(self.hidden2_output_mat * perceptrons, axis=0)

        return np.argmax(perceptrons)