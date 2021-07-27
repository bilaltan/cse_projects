class FileReader:

    def __init__(self) -> None:
        self.config = {}
        self.paths = ["./inputs/test1.seq","./inputs/test2.seq","./inputs/test3.seq","./inputs/test4.seq","./inputs/test5.seq"]
        for path in self.paths:
            self.read_file(path)
        pass

    def read_file(self,path):
        file = open(path,"r")
        lines = []
        linesRaw = file.readlines()
        for line in linesRaw:
            tempLine = line.split("\n")[0]
            lines.append(tempLine)
        self.config[path] = lines
