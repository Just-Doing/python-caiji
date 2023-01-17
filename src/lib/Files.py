import os


def getLatestExcel(path):
    # list all .xlsx files in absolute directory
    files = (os.path.abspath(path+file)
             for file in os.listdir(path) if file.endswith('.xlsx'))
    # get their last updated time
    files_and_updated_time = ((file, os.path.getmtime(file)) for file in files)

    # sort out the lastest updated xlsx
    last_updated_xlsx = sorted(
        files_and_updated_time, key=lambda x: x[1], reverse=True)

    # check if this said xlsx exists
    # if so, store its absolute path in `result`
    if last_updated_xlsx:
        result = last_updated_xlsx[0][0]
    else:
        result = None
    return result