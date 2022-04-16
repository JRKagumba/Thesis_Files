# %%
import os
import sys
import glob

import shutil 
import pandas as pd



# %%
xsens_raw =r"E:\Data\Jarrod_Thesis\Xsens\raw_data"
xsens_processed = r"E:\Data\Jarrod_Thesis\Xsens\processed_data"

for subject in os.scandir(xsens_raw):

    subject_path=subject.path
    subject_name=subject.name

    for task in os.scandir(subject_path):
        if task.is_dir():
            task_path=task.path
            task_name=task.name

            dataframes_dict={}
            for file in os.scandir(task_path):
                cycle_name=file.name[13:16]
                cycle_path=file.path


                xls = pd.ExcelFile(cycle_path)
                dataframes_dict[cycle_name]=pd.read_excel(xls, 'Center of Mass')

            new_task_path=os.path.join(xsens_processed,subject_name,task_name)

            get_com_data(dataframes_dict,new_task_path)
            # shutil.rmtree(os.path.join(new_task_path,'Elbow'), ignore_errors=True)
            

            

            


# xls = pd.ExcelFile(file_path)
# subject_csv = pd.read_excel(xls, 'Joint Angles ZXY')
# subject_COM_csv = pd.read_excel(xls, 'Center of Mass')

    # print(task_set)

# %%
def get_com_data(dataframes_dict,new_task_path):
    COM={}
    joint='COM'
    for cycle_name, dataframe in dataframes_dict.items():

        for columnName in dataframe.iloc[:,1:4].columns:
            if columnName not in COM.keys():
                COM[columnName]={}
        
        for (columnName, columnData) in dataframe.iloc[:,1:4].iteritems():  
            COM[columnName][columnName+'_'+cycle_name]=pd.Series(columnData)


    for columnName in COM.keys():
        df= pd.DataFrame(COM[columnName])
        columnName=columnName.replace("/", "_")
        new_dir=os.path.join(new_task_path,joint,columnName)
        os.makedirs(new_dir, exist_ok = True)
        df.to_csv(os.path.join(new_dir, f'{columnName}.csv')) 
        print(f'New directory created at {new_dir}')


# %%
sample_path=r"E:\Data\Jarrod_Thesis\Xsens\raw_data\S07\T05\XSEN_S07_T05_C02.xlsx"

xls = pd.ExcelFile(sample_path)
pd.read_excel(xls, 'Center of Mass').iloc[:,1:4]

# %%


# %%


# %%


# %%


# %%


# %%


# %%
def get_shoulder_data(dataframes_dict,new_task_path):
    
    joint='Shoulder'

    for orientation in ['Left','Right']:
        SHOULDER={}
        if orientation == 'Left':
            for cycle_name, dataframe in dataframes_dict.items():

                for columnName in dataframe.iloc[:,23:24].columns:
                    if columnName not in SHOULDER.keys():
                        SHOULDER[columnName]={}
                
                for (columnName, columnData) in dataframe.iloc[:,23:24].iteritems():  
                    SHOULDER[columnName][columnName+'_'+cycle_name]=pd.Series(columnData)


            for columnName in SHOULDER.keys():
                df= pd.DataFrame(SHOULDER[columnName])
                new_dir=os.path.join(new_task_path,joint,orientation,columnName)
                os.makedirs(new_dir, exist_ok = True)
                df.to_csv(os.path.join(new_dir, f'{columnName}.csv')) 
                print(f'New directory created at {new_dir}')
        
        if orientation == 'Right':
            for cycle_name, dataframe in dataframes_dict.items():

                for columnName in dataframe.iloc[:,35:36].columns:
                    if columnName not in SHOULDER.keys():
                        SHOULDER[columnName]={}
                
                for (columnName, columnData) in dataframe.iloc[:,35:36].iteritems():  
                    SHOULDER[columnName][columnName+'_'+cycle_name]=pd.Series(columnData)


            for columnName in SHOULDER.keys():
                df= pd.DataFrame(SHOULDER[columnName])
                new_dir=os.path.join(new_task_path,joint,orientation,columnName)
                os.makedirs(new_dir, exist_ok = True)
                df.to_csv(os.path.join(new_dir, f'{columnName}.csv')) 
                print(f'New directory created at {new_dir}')



# %%
def get_elbow_data(dataframes_dict,new_task_path):
    
    joint='Elbow'

    for orientation in ['Left','Right']:
        ELBOW={}
        if orientation == 'Left':
            for cycle_name, dataframe in dataframes_dict.items():

                for columnName in dataframe.iloc[:,28:29].columns:
                    if columnName not in ELBOW.keys():
                        ELBOW[columnName]={}
                
                for (columnName, columnData) in dataframe.iloc[:,28:29].iteritems():  
                    ELBOW[columnName][columnName+'_'+cycle_name]=pd.Series(columnData)


            for columnName in ELBOW.keys():
                df= pd.DataFrame(ELBOW[columnName])
                new_dir=os.path.join(new_task_path,joint,orientation,columnName)
                os.makedirs(new_dir, exist_ok = True)
                df.to_csv(os.path.join(new_dir, f'{columnName}.csv')) 
                print(f'New directory created at {new_dir}')
        
        if orientation == 'Right':
            for cycle_name, dataframe in dataframes_dict.items():

                for columnName in dataframe.iloc[:,41:42].columns:
                    if columnName not in ELBOW.keys():
                        ELBOW[columnName]={}
                
                for (columnName, columnData) in dataframe.iloc[:,41:42].iteritems():  
                    ELBOW[columnName][columnName+'_'+cycle_name]=pd.Series(columnData)


            for columnName in ELBOW.keys():
                df= pd.DataFrame(ELBOW[columnName])
                new_dir=os.path.join(new_task_path,joint,orientation,columnName)
                os.makedirs(new_dir, exist_ok = True)
                df.to_csv(os.path.join(new_dir, f'{columnName}.csv')) 
                print(f'New directory created at {new_dir}')




# %%
def get_com_data(dataframes_dict,new_task_path):
    COM={}
    joint='COM'
    for cycle_name, dataframe in dataframes_dict.items():

        for columnName in dataframe.iloc[:,-3:].columns:
            if columnName not in COM.keys():
                COM[columnName]={}
        
        for (columnName, columnData) in dataframe.iloc[:,-3:].iteritems():  
            COM[columnName][columnName+'_'+cycle_name]=pd.Series(columnData)


    for columnName in COM.keys():
        df= pd.DataFrame(COM[columnName])
        new_dir=os.path.join(new_task_path,joint,columnName)
        os.makedirs(new_dir, exist_ok = True)
        df.to_csv(os.path.join(new_dir, f'{columnName}.csv')) 
        print(f'New directory created at {new_dir}')

# %%
def get_trunk_data(dataframes_dict,new_task_path):
    TRUNK={}
    joint='Trunk'
    for cycle_name, dataframe in dataframes_dict.items():

        for columnName in dataframe.iloc[:,13:14].columns:
            if columnName not in TRUNK.keys():
                TRUNK[columnName]={}
        
        for (columnName, columnData) in dataframe.iloc[:,13:14].iteritems():  
            TRUNK[columnName][columnName+'_'+cycle_name]=pd.Series(columnData)


    for columnName in TRUNK.keys():
        df= pd.DataFrame(TRUNK[columnName])
        new_dir=os.path.join(new_task_path,joint,columnName)
        os.makedirs(new_dir, exist_ok = True)
        df.to_csv(os.path.join(new_dir, f'{columnName}.csv')) 
        print(f'New directory created at {new_dir}')

# %%
def get_neck_data(dataframes_dict,new_task_path):
    NECK={}
    joint='Neck'
    for cycle_name, dataframe in dataframes_dict.items():

        for columnName in dataframe.iloc[:,18:19].columns:
            if columnName not in NECK.keys():
                NECK[columnName]={}
        
        for (columnName, columnData) in dataframe.iloc[:,18:19].iteritems():  
            NECK[columnName][columnName+'_'+cycle_name]=pd.Series(columnData)


    for columnName in NECK.keys():
        df= pd.DataFrame(NECK[columnName])
        new_dir=os.path.join(new_task_path,joint,columnName)
        os.makedirs(new_dir, exist_ok = True)
        df.to_csv(os.path.join(new_dir, f'{columnName}.csv')) 
        print(f'New directory created at {new_dir}')

# %%
    # task_set=set()
    # for file in os.listdir(directory):
    #     if file[:4]=='XSEN':
    #         task_set.add(file[9:12])
    


    # for task in task_set:
    #     path = os.path.join(directory, task)
    #     os.mkdir(path)

    #     for item in os.scandir(directory):
            
    #         if (item.is_file()) and (task in item.name):
                
    #             source=item.path
    #             destination= os.path.join(directory, task, item.name)
                

    #             shutil.move(source, destination)
    #             print(f"{item.name} has been moved to {task}")



