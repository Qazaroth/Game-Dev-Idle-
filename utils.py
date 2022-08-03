import os

def clear():
    command = "clear"
    if os.name in ("nt", "dos"):  # If Machine is running on Windows, use cls
        command = "cls"

    os.system(command)

def printProgressBar(iteration, total, prefix="", suffix="", decimals=1, length=100, fill = "█", printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration/float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    
    print("\r{} |{}| {}% {}".format(prefix, bar, percent, suffix), end=printEnd)
    
    if iteration == total:
        print()