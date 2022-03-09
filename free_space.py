import os

folder = r"D:\DIP_large\saved_runs\runs\new_run_2"

keep = range(0,121,5)

for i in range(0,121):
    f = "checkpoint_epoch_{}.pt".format(i)
    full = os.path.join(folder,f)
    if os.path.isfile(full):
        if i not in keep:
            
            os.remove(full)
        else:
            print("keep " + f)