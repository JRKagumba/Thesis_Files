# %%
import os
import pandas as pd
import shutil 

# %%

count=0

xsens_processed =r"E:\Data\Jarrod_Thesis\Individual_XSEN\processed_data"
# norax_processed =r"E:\Data\Jarrod_Thesis\Noraxon\processed_data"

for (root,dirs,files) in os.walk(xsens_processed, topdown=False):
    # print (root)
    # print (dirs)

    for file in files:
        file_path=os.path.join(root,file)
        file_name=file[:-4]

        if 'COM' in file_path:
            # if 'mm' in file:
            # if ('mm' in file_name) or ('image' in file_name):
            #     try:
            #         os.remove(os.path.join(root,file))
            #         print(f"{os.path.join(root,file)} has been removed")
            #     except:
            #         print(f"Error removing {os.path.join(root,file)}")
                # shutil.rmtree(os.path.join(root,file), ignore_errors=True)
                
            convert_xsens_com_to_mm(file_path,file_name,root)
            print(f"{file_path[-35:]} has been converted")

        # print (os.path.join(root,dirs,files))

    print ('----------------------------------------------------')
    # count+=1
    # if count>=1:
    #     break

# %%
def convert_xsens_com_to_mm(file_path,file_name,root):
    """
    Purpose of function:
    -convert COM data to (mm)
    -convert column name to add (mm)
    """


    # file_path=r"E:\Data\Jarrod_Thesis\Xsens\processed_data\S01\T02\COM\CoM pos z\CoM pos z.csv"

    data =pd.read_csv(file_path).iloc[:, 1:]
    data =data*1000

    column_names_dict={column:f"{column}_(mm)" for column in data.columns}
    data=data.rename(columns=column_names_dict)

    converted_file_name=os.path.join(root,f"{file_name}_(mm).csv")
    data.to_csv(converted_file_name)


# %%



# %%



