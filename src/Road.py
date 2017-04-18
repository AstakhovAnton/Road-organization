class Road:
    def __init__(self, listx, listy):
        self.points = []
        for i in range(len(listx)):
            self.points.append((listx[i], listy[i]))

    def roadStart(self):
        return self.points[0]
