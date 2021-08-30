import os


class BuilderBase(object):
    def __init__(self, repo, gitbranch):
        self.repo = repo
        self.gitbranch = gitbranch

    def conn(self):
        """返回连接实例"""
