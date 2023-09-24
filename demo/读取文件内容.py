def getProductType(browser, fileName):
  with open(fileName,'r') as file_to_read:
    content=file_to_read.read()
    types = json.loads(content)
