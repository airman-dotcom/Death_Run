import random

class NeuralNetwork:
    def __init__(self, input_dim, hidden_dim, output_dim, w1=None, w2=None, b1=None, b2=None):
        # Initialize weights and biases
        if w1 is None:
            self.w1 = [[random.uniform(-0.01, 0.01) for _ in range(input_dim)] for _ in range(hidden_dim)]
        else:
            self.w1 = w1
        if b1 is None:
            self.b1 = [0] * hidden_dim
        else:
            self.b1 = b1

        if w2 is None:
            self.w2 = [[random.uniform(-0.01, 0.01) for _ in range(hidden_dim)] for _ in range(output_dim)]
        else:
            self.w2 = w2
        if b2 is None:
            self.b2 = [0] * output_dim
        else:
            self.b2 = b2

    def forward(self, a, b, c):
        # First layer computations
        inn = a + b
        inn.append(c)
        X = inn
        self.input = X
        self.z1 = [sum(x * w for x, w in zip(X, col)) + b for col, b in zip(zip(*self.w1), self.b1)]
        # Apply ReLU activation
        self.a1 = [max(0, z) for z in self.z1]

        # Second layer computations
        self.z2 = [sum(a * w for a, w in zip(self.a1, col)) + b for col, b in zip(zip(*self.w2), self.b2)]
        return round(self.z2[0])

    def compute_loss(self, y_pred, y_true):
        # Mean Squared Error Loss
        return sum((yp - yt) ** 2 for yp, yt in zip(y_pred, y_true)) / len(y_true)

    def backward(self, y_pred, y_true):
        # Calculate error
        error = [yp - yt for yp, yt in zip(y_pred, y_true)]
        
        # Calculate gradients for w2 and b2
        dL_dw2 = [[e * a for a in self.a1] for e in error]
        dL_db2 = error

        # Calculate gradient for w1 and b1
        dL_da1 = [sum(e * w for e, w in zip(error, col)) for col in zip(*self.w2)]
        dL_dz1 = [da * (1 if z > 0 else 0) for da, z in zip(dL_da1, self.z1)]
        dL_dw1 = [[dz * x for x in self.input] for dz in dL_dz1]
        dL_db1 = dL_dz1

        return dL_dw1, dL_db1, dL_dw2, dL_db2

    def update_params(self, gradients, learning_rate):
        dL_dw1, dL_db1, dL_dw2, dL_db2 = gradients
        
        # Update weights and biases for the first layer
        self.w1 = [[w - learning_rate * dw for w, dw in zip(row, grad_row)] for row, grad_row in zip(self.w1, dL_dw1)]
        self.b1 = [b - learning_rate * db for b, db in zip(self.b1, dL_db1)]

        # Update weights and biases for the second layer
        self.w2 = [[w - learning_rate * dw for w, dw in zip(row, grad_row)] for row, grad_row in zip(self.w2, dL_dw2)]
        self.b2 = [b - learning_rate * db for b, db in zip(self.b2, dL_db2)]

    def train(self, y, learning_rate):
        
        y_pred = [1]
        y2 = [y]
        loss = self.compute_loss(y_pred, y2)
        gradients = self.backward(y_pred, y2)
        self.update_params(gradients, learning_rate)
    def output(self):
        print(self.w1)
        print("\n")
        print(self.w2)
        print("\n")
        print(self.b1)
        print("\n")
        print(self.b2)


