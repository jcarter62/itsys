import pandas as pd

class ImportCSV:

    data = []

    def __init__(self):
        self.data = []

    def parseCSV(self, filePath):
        col_names = ['name', 'ip', 'url', 'systype', 'location']
        csvData = pd.read_csv(filePath, names=col_names, header=0)
        for i, row in csvData.iterrows():
            self.data.append(row)
            print(i, row)
        return self.data
