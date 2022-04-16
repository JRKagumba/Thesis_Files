# %%
"""
Group 1 : (S21, S19, S22, S23, S24, S28, S29, S30)
Group 2 : (S02, S03, S05, S06, S08, S10, S09, S12)
Group 3 : (S01, S04, S07, S11, S25, S20, S26, S27) 
"""

"""
If 'processed_data', 
    subject number, 
    trial number, 
    joint, 
    joint_orientation,
    'interp' .... are in the path then append to dict
"""

# %%
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 
import spm1d
import os

import warnings
warnings.filterwarnings("ignore")

from collections import Counter

# %%
colours={
    0:{'name':"red",
       'value':["#FF0000","#FF6666"]},
    7:{'name':"red-purple",
       'value':["#953553","#C96786"]},
    1:{'name':"purple",
       'value':["#6A0DAD","#A031EF"]},
    8:{'name':"blue-purple",
       'value':["#8A2BE2","#BC85EE"]},
    2:{'name':"blue",
       'value':["#0000FF","#6666FF"]},
    9:{'name':"blue-green",
       'value':["#088F8F","#0DF0F0"]},
    3:{'name':"green",
       'value':["#009900","#33CC33"]},
    10:{'name':"yellow-green",
       'value':["#9ACD32","#C2E184"]},
    4:{'name':"yellow",
       'value':["#999900","#FFFF66"]},
    11:{'name':"yellow-orange",
       'value':["#FFAE42","#FFDAA8"]},
    5:{'name':"orange",
       'value':["#FFA500","#FFC966"]},
    12:{'name':"red-orange",
       'value':["#FF5349","#FFB3AF"]},
    6:{'name':"rose",
       'value':["#FF006C","#FF66A7"]},
    13:{'name':"brown",
       'value':["#964B00","#C97E33"]}
}

# %%

def find_file_paths(group_list, task, joint, orientation):

    xsens_processed =r"E:\Data\Jarrod_Thesis\Individual_XSEN\processed_data"
    norax_processed =r"E:\Data\Jarrod_Thesis\Individual_NORX\processed_data"

    file_path_list=[]

    for mocap in [xsens_processed,norax_processed]:
        for (root,dirs,files) in os.walk(mocap, topdown=False):

            for file in files:

                for subj in group_list:
                    
                    file_path=os.path.join(root,file)
                    file_name=file[:-4]
                    
                    if (subj in file_path) and (joint in file_path) and (orientation in file_path) and (task in file_path) and ('interp' in file_path):
                        file_path_list.append(file_path)
            #             print(f"Appended {file_path}")          
            # print ('----------------------------------------------------')

    return(file_path_list)



# %%

def filepaths_to_dataframes(path_list):
    """
    Takes in a list of file paths and return a list of dataframes
    """
    dataframe_list=[]

    for path in path_list:
        mocp_versin=path.split('\\')[3][-4:]
        subj_number=path.split('\\')[5]
        task_number=path.split('\\')[6]
        joint_type=path.split('\\')[7]
        if joint_type in ['Elbow','Shoulder']:
            joint_type=path.split('\\')[7]+'-'+path.split('\\')[8]
        
        data=pd.read_csv(path).iloc[:, 1:]
        new_column_names={column_name:f"{subj_number}_{task_number}_{joint_type}_{mocp_versin}" for column_name in data.columns}
        data=data.rename(columns=new_column_names)
        dataframe_list.append(data)

    return dataframe_list



# %%
def interpolate_dataframes(dataframe_list):

    agg_data= pd.concat(dataframe_list, axis=1)

    data_dict={}
    MaxIndex=0
    for (columnName, columnData) in agg_data.iteritems():
        if len(columnData.dropna()) > MaxIndex:
            MaxIndex = len(columnData.dropna())

    count=10
    for (columnName, columnData) in agg_data.iteritems():

        t2 = columnData.dropna()
        x0 = range(t2.size)
        x1 = np.linspace(0, t2.size, num=MaxIndex)

        data_dict[f"{columnName}_{count}"]= pd.Series(np.interp(x1, x0, t2, left=None, right=None))
        count+=1

    interp_data=pd.DataFrame(data_dict)
    new_column_names={column_name:column_name[:-3] for column_name in interp_data.columns}
    interp_data=interp_data.rename(columns=new_column_names)

    return (interp_data)


# %%
def compute_spm_ANOVA_stats(interpolated_data):

    Y=interpolated_data

    A=pd.Categorical(Y.columns)
    A=A.codes

    Y=Y.T.to_numpy()
    A=np.array(A)

    alpha        = 0.05
    F            = spm1d.stats.anova1(Y, A, equal_var=False)
    Fi           = F.inference(alpha)

    return(alpha, F, Fi)

# %%
def create_file_directories(group_name,task,joint,orientation=''):
    """
    creates file directories
    """
    root_path=r"E:\Data\Jarrod_Thesis"
    new_dir=os.path.join(root_path,group_name,task,joint,orientation)
    os.makedirs(new_dir, exist_ok = True)
    return new_dir

# %%
def save_file_to_path(interpolated_data, directory):

    group=      directory.split('\\')[3]
    task=       directory.split('\\')[4]
    joint=      directory.split('\\')[5]
    orientation=directory.split('\\')[6]

    file_name=f"{group}_{task}_{joint}_{orientation}"
    file_path=os.path.join(directory, f'{file_name}.csv')
    interpolated_data.to_csv(file_path) 
    print(f'\tFile saved at {file_path}')

# %%


def create_rm_anova_data(interpolated_data):
    min_occurunces=Counter(interpolated_data.columns).most_common()[-1][1]

    values_dict={}
    data_dict={}
    count=10
    for value in set(interpolated_data.columns):
        values_dict[value]=0

    for (columnName, columnData) in interpolated_data.iteritems():
        if values_dict[columnName]<min_occurunces:
            values_dict[columnName]+=1
            data_dict[f"{columnName}_{count}"]=columnData
            count+=1

    rm_anoava_data=pd.DataFrame(data_dict)
    new_column_names={column_name:column_name[:-3] for column_name in rm_anoava_data.columns}
    rm_anoava_data=rm_anoava_data.rename(columns=new_column_names)

    return(rm_anoava_data)


# %%
def compute_spm_RM_ANOVA_stats(rm_data):

    Y=rm_data

    A=pd.Categorical(Y.columns)
    A=A.codes

    unique_elements=len(set(rm_data.columns))
    total_elements=len(rm_data.columns)
    divisor=total_elements//unique_elements
    SUBJ=[ element%divisor for element in range(total_elements)]


    Y=Y.T.to_numpy()
    A=np.array(A)
    SUBJ=np.array(SUBJ)

    alpha        = 0.05
    equal_var    = True
    F            = spm1d.stats.anova1(Y, A, equal_var)  #between-subjects
    Frm          = spm1d.stats.anova1rm(Y, A, SUBJ, equal_var)  #within-subjects (repeated-measures)
    Fi           = F.inference(alpha)
    Firm         = Frm.inference(alpha)
    
    return(alpha, F, Frm, Fi, Firm)

# %%
import copy

def plot_and_save_RM_ANOVA(rm_data, directory):

    MaxIndex = len(rm_data)

    Y=copy.deepcopy(rm_data)
    column_labels=rm_data.columns.unique()

    A=pd.Categorical(Y.columns)
    A=A.codes

    
    Y=Y.T.to_numpy()
    A=np.array(A)
    
    if 'COM' in directory:
        y_label='Millimeters (mm)'
    else:
        y_label=r'$\theta$ (deg)'


    if ('Elbow' in directory) or ('Shoulder' in directory):
        group=      directory.split('\\')[3]
        task=       directory.split('\\')[4]
        orientation=directory.split('\\')[6]
        joint=      directory.split('\\')[5] + '-' + orientation
    else:
        group=      directory.split('\\')[3]
        task=       directory.split('\\')[4]
        joint=      directory.split('\\')[5]


    plot_name=f"{group}_{task}_{joint}"


    fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=4, ncols=1, sharex=False,figsize=(18, 27))
    
    ###################################################-RAW_ax0-###################################################

    for k, column in enumerate(column_labels):
        ax0.plot(rm_data[[column]], colours[k]['value'][0], label=column[:3])


    handles, labels = ax0.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax0.legend([x for x in by_label.values()], [x for x in by_label.keys()], fontsize=8)   
    ax0.set_title(f"{plot_name}_raw",size=15) 
    ax0.set_ylabel(y_label, size=15)

    
    ###################################################-MEAN_STDEV_ax1-###################################################

    for k, column in enumerate(column_labels[:]):
        spm1d.plot.plot_mean_sd(Y[A==k], ax=ax1, facecolor=colours[k]['value'][0], 
                                linecolor=colours[k]['value'][1], edgecolor=colours[k]['value'][1], 
                                label=column[:3])

    ax1.legend(fontsize=8)
    ax1.set_title(f"{plot_name}_mean_stdev",size=15)
    ax1.set_ylabel(y_label, size=15)

    ###################################################-ANOVA_ax2-###################################################

    alpha, F, Frm, Fi, Firm = compute_spm_RM_ANOVA_stats(rm_data)

    Fi.plot(ax=ax2, color='k',label='Between-subjects analysis')
    Fi.plot_threshold_label(ax=ax2,color='k',ha='left')

    ax2.legend(fontsize=8)
    ax2.set_title(f"{plot_name}_ANOVA",size=15)    
    ax2.set_ylabel('SPM {F}', fontsize=15)

    ###################################################-RM_ANOVA_ax3-###################################################
        
    Firm.plot(ax=ax3, color='r', thresh_color='r', facecolor=(0.8,0.3,0.3), label='Within-subjects analysis')
    Fi.plot( ax=ax3,label='Between-subjects analysis')
    
    ax3.legend(fontsize=8)
    ax3.set_title(f"{plot_name}_RM_ANOVA",size=15)    
    ax3.set_ylabel('SPM {F}', fontsize=15)

    #########################################################################################################################
    for ax in [ax0, ax1, ax2, ax3]:

        if ax != ax0:
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

        ax.set_xlabel('Time (%)', size=15)


    fig.suptitle(f'{plot_name}',size=22,y=0.92)
    # plt.show()
    image_file_path=os.path.join(directory,f"{plot_name}_RM_ANOVA_image.png")
    plt.savefig(image_file_path)
    plt.close(fig)

# %%
def plot_and_save_ANOVA(interpolated_data, directory):

    MaxIndex = len(interpolated_data)
    column_labels=interpolated_data.columns.unique()

    Y=copy.deepcopy(interpolated_data)
    A=pd.Categorical(Y.columns)
    A=A.codes
    Y=Y.T.to_numpy()
    A=np.array(A)

    if 'COM' in directory:
        y_label='Millimeters (mm)'
    else:
        y_label=r'$\theta$ (deg)'


    if ('Elbow' in directory) or ('Shoulder' in directory):
        group=      directory.split('\\')[3]
        task=       directory.split('\\')[4]
        orientation=directory.split('\\')[6]
        joint=      directory.split('\\')[5] + '-' + orientation
    else:
        group=      directory.split('\\')[3]
        task=       directory.split('\\')[4]
        joint=      directory.split('\\')[5]


    plot_name=f"{group}_{task}_{joint}"


    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, ncols=1, sharex=False,figsize=(18, 27))
    
    ###################################################-RAW_ax0-###################################################

    for k, column in enumerate(column_labels):
        ax0.plot(interpolated_data[[column]], colours[k]['value'][0], label=column[:3])


    handles, labels = ax0.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax0.legend([x for x in by_label.values()], [x for x in by_label.keys()], fontsize=8)   
    ax0.set_title(f"{plot_name}_raw",size=15) 
    ax0.set_ylabel(y_label, size=15)

    
    ###################################################-MEAN_STDEV_ax1-###################################################

    for k, column in enumerate(column_labels[:]):
        spm1d.plot.plot_mean_sd(Y[A==k], ax=ax1, facecolor=colours[k]['value'][0], 
                                linecolor=colours[k]['value'][1], edgecolor=colours[k]['value'][1], 
                                label=column[:3])

    ax1.legend(fontsize=8)
    ax1.set_title(f"{plot_name}_mean_stdev",size=15)
    ax1.set_ylabel(y_label, size=15)

    ###################################################-ANOVA_ax2-###################################################

    alpha, F, Fi = compute_spm_ANOVA_stats(interpolated_data)

    Fi.plot(ax=ax2, color='k',label='Between-subjects analysis')
    Fi.plot_threshold_label(ax=ax2,color='k',ha='left')

    ax2.legend(fontsize=8)
    ax2.set_title(f"{plot_name}_ANOVA",size=15)    
    ax2.set_ylabel('SPM {F}', fontsize=15)


    #########################################################################################################################
    for ax in [ax0, ax1, ax2]:

        if ax != ax0:
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

        ax.set_xlabel('Time (%)', size=15)


    fig.suptitle(f'{plot_name}',size=22,y=0.92)
    # plt.show()
    image_file_path=os.path.join(directory,f"{plot_name}_ANOVA_image.png")
    plt.savefig(image_file_path)
    plt.close(fig)

# %%

def groups(group):
    groups_dict={
    'Group1' : ['S21', 'S19', 'S22', 'S23', 'S24', 'S28', 'S29', 'S30'],
    'Group2' : ['S02', 'S03', 'S05', 'S06', 'S08', 'S10', 'S09', 'S12'],
    'Group3' : ['S01', 'S04', 'S07', 'S11', 'S25', 'S20', 'S26', 'S27'] }

    if group not in groups_dict.keys():
        return ('Invalid group name')
    else:
        return (group, groups_dict[group])



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
def create_groups_with_data(_group,_joint,_task,_orientation):
    group_name, group_list=groups(_group)
    joint, orientation =joints(_joint, _orientation)
    task=_task

    print(group_name.upper())
    directory= create_file_directories(group_name,task,joint,orientation)
    print(f"\tStep 1:\tDirectory created for {group_name}\t{task}\t{joint}\t{orientation}")
    path_list=              find_file_paths(group_list, task, joint, orientation)
    print("\tStep 2:\tFile paths found")
    dataframe_list=         filepaths_to_dataframes(path_list)
    print("\tStep 3:\tDataframe list created")
    interpolated_data=      interpolate_dataframes(dataframe_list)
    print("\tStep 4:\tData interpolated")
    rm_data=                create_rm_anova_data(interpolated_data)


    print("\tStep 5a:ANOVA data preparing to be plotted")
    plot_and_save_ANOVA(interpolated_data, directory)
    print("\tStep 5b:ANOVA data plotted and saved")

    print("\tStep 6a:RM_ANOVA data preparing to be plotted")
    plot_and_save_RM_ANOVA(rm_data, directory)
    print("\tStep 6b:RM_ANOVA data plotted and saved")

    save_file_to_path(interpolated_data, directory)



# %%

['Neck','Trunk','COM_X','COM_Y','COM_Z','Elbow','Shoulder']
['T01','T02','T03','T04','T05','T06','T07','T08','T09','T10','T11','T12','T13','T14']

for _group in ['Group1']:
    for _task in ['T05']:
        for _joint in ['COM_Z']:
            if _joint in ['Elbow']:
                for _orientation in ['Right']:
                    create_groups_with_data(_group,_joint,_task,_orientation)
            else:
                create_groups_with_data(_group,_joint,_task,_orientation='')




# %%


# %%



