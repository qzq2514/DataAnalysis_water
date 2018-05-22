from getNewTableFromOther_func import func

path1=["4-1-2001/39055058热表.xls","5-1-1003/39054897热表.xls","5-1-2401/39057047热表.xls"]
path2=["4-1-2001/16130016客厅南.xls","5-1-1003/16130005客厅南.xls","5-1-2401/16130017客厅南.xls"]

for n in range(3):
 func(path1[n],path2[n],n+1)