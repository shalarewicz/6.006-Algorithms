import imagematrix


class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):

        dp = [[None for x in range(self.height)] for y in range(self.width)]

        for j in range(0, self.height):
            for i in range(0, self.width):
                if j == 0:
                    dp[i][j] = (self.energy(i, j), (None, None))
                else:
                    choices = []
                    if i > 0:
                        left, lp = dp[i-1][j-1]
                        choices.append((left, (i-1, j-1)))
                    if i < self.width - 1:
                        right, rp = dp[i+1][j-1]
                        choices.append((right, (i + 1, j - 1)))

                    center, cp = dp[i][j-1]
                    choices.append((center, (i, j-1)))

                    energy, coord = min(choices)
                    dp[i][j] = (energy + self.energy(i, j), coord)

        seam_start = dp[0][self.height - 1]
        start = 0

        # Best seam is the pixel with the minimum seam energy in the bottom row
        for i in range(0, self.width):
            new = dp[i][self.height - 1]
            if new < seam_start:
                seam_start = new
                start = i

        result = [(start, self.height-1)]

        energy, (x, y) = seam_start
        while y is not None:
            result.append((x, y))
            new, (x, y) = dp[x][y]

        result.reverse()
        return result

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
