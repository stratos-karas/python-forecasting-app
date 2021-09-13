class LRL:

    def __init__(self, Y, X=None):
        self.Y = Y
        self.X = X

    def create_coefficients(self):
        
        if self.X == None:
            self.X = [t for t in range(1, len(self.Y) + 1)] 
        
        mean_Y = sum(self.Y) / len(self.Y)
        mean_X = sum(self.X) / len(self.X)
        prod_XY = [(x * y) for x, y in list( zip(self.X, self.Y) )]
        X2 = [x ** 2 for x in self.X]

        beta = (sum(prod_XY) / len(prod_XY) - mean_X * mean_Y) / (sum(X2) / len(X2) - mean_X ** 2)
        alpha = mean_Y - beta * mean_X

        return beta, alpha

    def predict(self, horizon):
        
        beta, alpha = self.create_coefficients()

        predictions = []
        for t in range(1, len(self.X) + horizon + 1):
            predictions.append(beta * t + alpha)

        return predictions