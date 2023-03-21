class DSU:
    def __init__(self, n):
        self.parents = [-1 for _ in range(n)]
    
    def find(self,x):
        if self.parents[x] >= 0:
            return self.find(self.parents[x])
        return x
    
    def union(self, x, y):
        rootA, rootB = self.find(x), self.find(y)
        if rootA == rootB:
            return 0
        elif abs(self.parents[rootA]) > abs(self.parents[rootB]):
            self.parents[rootA] += self.parents[rootB]
            self.parents[rootB] = rootA
        else:
            self.parents[rootB] += self.parents[rootA]
            self.parents[rootA] = rootB
            
        return 1
    
    def distinctParents(self):
        cnt = 0
        for _ in self.parents:
            cnt += 1 if _ < 0 else 0
        return cnt
    
    def hasParent(self, x):
        return False if self.parents[x] == -1 else True
    
