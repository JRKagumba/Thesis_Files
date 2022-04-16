# %%
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 
import spm1d
import os

import warnings
warnings.filterwarnings("ignore")

# from collections import Counter

# %%
colours={
    0:{'name':"red",
       'value':["#FF0000","#FF6666"]},
    10:{'name':"red-purple",
       'value':["#953553","#C96786"]},
    7:{'name':"purple",
       'value':["#6A0DAD","#A031EF"]},
    4:{'name':"blue-purple",
       'value':["#8A2BE2","#BC85EE"]},
    1:{'name':"blue",
       'value':["#0000FF","#6666FF"]},
    11:{'name':"blue-green",
       'value':["#088F8F","#0DF0F0"]},
    2:{'name':"green",
       'value':["#009900","#33CC33"]},
    5:{'name':"yellow-green",
       'value':["#9ACD32","#C2E184"]},
    8:{'name':"yellow",
       'value':["#999900","#FFFF66"]},
    12:{'name':"yellow-orange",
       'value':["#FFAE42","#FFDAA8"]},
    9:{'name':"orange",
       'value':["#FFA500","#FFC966"]},
    6:{'name':"red-orange",
       'value':["#FF5349","#FFB3AF"]},
    3:{'name':"rose",
       'value':["#FF006C","#FF66A7"]},
    13:{'name':"brown",
       'value':["#964B00","#C97E33"]}
}

# %%
def find_file_paths(group_list, task, joint, orientation):

    group1 =r"E:\Data\Jarrod_Thesis\Group1"
    group2 =r"E:\Data\Jarrod_Thesis\Group2"
    group3 =r"E:\Data\Jarrod_Thesis\Group3"

    file_path_list=[]

    for mocap in [group1,group2,group3]:
        for (root,dirs,files) in os.walk(mocap, topdown=False):

            for file in files:

                for group in group_list:
                    
                    file_path=os.path.join(root,file)
                    file_name=file[:-4]
                    
                    if (group in file_path) and (joint in file_path) and (orientation in file_path) and (task in file_path) and ('csv' in file_path):
                        file_path_list.append(file_path)
            #             print(f"Appended {file_path}")          
            # print ('----------------------------------------------------')

    return(file_path_list)

# path_list=find_file_paths(['Group1','Group2','Group3'], 'T08', 'Shoulder', 'Right')

# %%
def find_file_directory(task,joint,orientation=''):
    """
    creates file directories
    """
    root_path=r"E:\Data\Jarrod_Thesis"
    new_dir=os.path.join(root_path,'All',task,joint,orientation)
    return new_dir

# %%
def filepaths_to_dataframes(path_list):
    """
    Takes in a list of file paths and return a list of dataframes
    """

    dataframe_dict={}
    for path in path_list:
        group_number=path.split('\\')[3]
        task_number=path.split('\\')[4]
        joint_type=path.split('\\')[5]

        if joint_type in ['Elbow','Shoulder']:
            joint_type=path.split('\\')[5]+'-'+path.split('\\')[6]
        
        data=pd.read_csv(path).iloc[:, 1:]
        new_column_names={column_name:f"{group_number}_{task_number}_{joint_type}" for column_name in data.columns}
        data=data.rename(columns=new_column_names)


        dataframe_dict['task']=task_number
        dataframe_dict['joint']=joint_type
        dataframe_dict[group_number]={}
        dataframe_dict[group_number]['data']=data
        dataframe_dict[group_number]['length']=len(data)

        _joint = path.split('\\')[5]
        if _joint in ['Elbow','Shoulder']:
            directory=find_file_directory(task=path.split('\\')[4],
                                            joint=path.split('\\')[5],
                                            orientation=path.split('\\')[6])
        else:
            directory=find_file_directory(task=path.split('\\')[4],
                                            joint=path.split('\\')[5],
                                            orientation='')

    return directory, dataframe_dict



# directory, dataframe_dict=filepaths_to_dataframes(path_list)


# %%


# %%
def interpolate_dataframes(df_tuple,df_dict):
    """
    -takes in a tuple of group names and the dataframe_dict
    -returns 2 interpolated dataframes
    """
    name_1=df_tuple[0]
    name_2=df_tuple[1]

    length_1=df_dict[name_1]['length']
    length_2=df_dict[name_2]['length']

    MaxIndex=max(length_1,length_2)


    interp_data_dict={}
    for name in [name_1,name_2]:
        if df_dict[name]['length']==MaxIndex:
            interp_data_dict[name]=df_dict[name]['data']
        
        else:
            count=1000
            data_dict={}
            shorter_data=df_dict[name]['data']
            for (columnName, columnData) in shorter_data.iteritems():

                t2 = columnData.dropna()
                x0 = range(t2.size)
                x1 = np.linspace(0, t2.size, num=MaxIndex)

                data_dict[f"{columnName}_{count}"]= pd.Series(np.interp(x1, x0, t2, left=None, right=None))
                count+=1

                interp_data=pd.DataFrame(data_dict)
                new_column_names={column_name:column_name[:-5] for column_name in interp_data.columns}
                interp_data=interp_data.rename(columns=new_column_names)
            
            interp_data_dict[name]=interp_data

    return (MaxIndex, interp_data_dict)


# MaxIndex, interp_data_dict=interpolate_dataframes(group_combo_lst[0],dataframe_dict)

# %%
def compute_spm_TTEST_stats(interpolated_data_1, interpolated_data_2):

    YA=interpolated_data_1
    YA=YA.T.to_numpy()

    YB=interpolated_data_2
    YB=YB.T.to_numpy()

    alpha      = 0.05
    t          = spm1d.stats.ttest2(YA, YB, equal_var=True)
    ti         = t.inference(alpha, two_tailed=True, interp=True)

    return(alpha, t, ti)

# alpha, t, ti = compute_spm_TTEST_stats(interp_data_dict['Group1'], interp_data_dict['Group2'])

# ti.plot()
# ti.plot_threshold_label(fontsize=8)
# ti.plot_p_values(size=10, offset_all_clusters=(0,0.9))

# %%
from itertools import combinations
def plot_and_save_TTEST(directory, dataframe_dict):

    group_lst=['Group1','Group2','Group3']
    group_combo_lst=[]
    combos = combinations(group_lst, 2)
    for combo in combos:
        group_combo_lst.append(combo)

  
    task=dataframe_dict['task']
    joint=dataframe_dict['joint']


    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, ncols=1, sharex=False,figsize=(18, 27))
    
    ###################################################-compute and plot TTESTS-###################################################
    
    for index, ax in enumerate([ax0, ax1, ax2]):
    
        group_i=group_combo_lst[index][0]
        group_j=group_combo_lst[index][1]
        
        plot_name=f"{group_i}-{group_j}_{task}_{joint}"
        MaxIndex, interp_data_dict=interpolate_dataframes(group_combo_lst[index],dataframe_dict)
        alpha, t, ti = compute_spm_TTEST_stats(interp_data_dict[group_i], interp_data_dict[group_j])

        ti.plot(ax=ax,color='k',label='Between Groups-Post Hoc')
        ti.plot_threshold_label(ax=ax, fontsize=8)
        ti.plot_p_values(size=10, offset_all_clusters=(0,0.9), ax=ax)

        ax.legend(fontsize=8)
        ax.set_title(f"{plot_name}_TTEST",size=15)    
        ax.set_ylabel('SPM {t}', fontsize=15)
        ax.set_xlabel('Time (%)', size=15)

        x0, x1, y0, y1 = ax.axis()
        margin_x = 0.01 * (x1-x0)
        margin_y = 0.01 * (y1-y0)
        ax.axis((x0 - margin_x,
                    x1 + margin_x,
                    y0 - margin_y,
                    y1 + margin_y))

        ax.margins(x=0.01)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(MaxIndex/5))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(MaxIndex/20))
        ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=MaxIndex))
    


    fig.suptitle(f'{task}_{joint}',size=22,y=0.92)
    # plt.show()
    image_file_path=os.path.join(directory,f"{task}_{joint}_TTEST_image.png")
    plt.savefig(image_file_path)
    plt.close(fig)

# plot_and_save_TTEST(directory, dataframe_dict)

# %%
def joints(joint,orientation=''):
    joints_list=['Neck','Trunk','COM_X','COM_Y','COM_Z','Elbow','Shoulder']

    if joint not in joints_list:
        return('Invalid joint name')
    elif (joint == 'Elbow') and (orientation not in ['Left','Right']):
        return(f'Invalid {joint} orientation')
    elif (joint == 'Shoulder') and (orientation not in ['Left','Right']):
        return(f'Invalid {joint} orientation')

    if joint in [joint for joint in joints_list if joint not in ['Elbow','Shoulder']]:
        orientation=''
    
    return (joint, orientation)


# %%
def create_TTEST_plots_with_data(_joint,_task,_orientation):
    joint, orientation =joints(_joint, _orientation)
    task=_task

    print(f'{_task}__{_joint}-{_orientation}')

    path_list=                  find_file_paths(['Group1','Group2','Group3'], task, joint, orientation)
    print("\tStep 1:\tFile paths found")

    directory, dataframe_dict=  filepaths_to_dataframes(path_list)
    print("\tStep 2:\tDestination directory and dataframe dict created")

    plot_and_save_TTEST(directory, dataframe_dict)
    print("\tStep 3:\tPlots created and saved")


# %%

['Neck','Trunk','COM_X','COM_Y','COM_Z','Elbow','Shoulder']
['T01','T02','T03','T04','T05','T06','T07','T08','T09','T10','T11','T12','T13','T14']



for _task in ['T05']:
    for _joint in ['COM_Z']:
        if _joint in ['Elbow']:
            for _orientation in ['Right']:
                create_TTEST_plots_with_data(_joint,_task,_orientation)
        else:
            create_TTEST_plots_with_data(_joint,_task,_orientation='')




# %%


# %%


# %%



