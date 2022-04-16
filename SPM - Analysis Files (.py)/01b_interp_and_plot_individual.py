# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 
import spm1d

# %%
def find_file_paths(task, joint, orientation):

    norax_processed =r"E:\Data\Jarrod_Thesis\Individual_NORX\processed_data"

    file_path_list=[]

    for mocap in [norax_processed]:
        for (root,dirs,files) in os.walk(mocap, topdown=False):

            for file in files:

                file_path=os.path.join(root,file)
                file_name=file[:-4]
                
                if (joint in file_path) and (orientation in file_path) and (task in file_path) and ('Flexion' in file_path) and ('interp' not in file_path) and ('image' not in file_path):
                    file_path_list.append((file_path, root))
            #             print(f"Appended {file_path}")          
            # print ('----------------------------------------------------')

    return(file_path_list)

# %%
def interpolate_data_from_file_path(file_path,root):

    subject=        root.split('\\')[5]
    task=           root.split('\\')[6]
    joint=          root.split('\\')[7]

    print(f"\tInterpolating: {subject}_{task}_{joint}")

    df=pd.read_csv(file_path).iloc[:, 1:]
    MaxIndex=0
    for (columnName, columnData) in df.iteritems():
        if len(columnData.dropna()) > MaxIndex:
            MaxIndex = len(columnData.dropna())

    data_dict={}
    count=10
    for (columnName, columnData) in df.iteritems():

        t2 = columnData.dropna()
        x0 = range(t2.size)
        x1 = np.linspace(0, t2.size, num=MaxIndex)

        data_dict[f"{columnName}_{count}"]= pd.Series(np.interp(x1, x0, t2, left=None, right=None))
        
        count+=1

    interp_data=pd.DataFrame(data_dict)
    new_column_names={column_name:column_name[:-3] for column_name in interp_data.columns}
    interp_data=interp_data.rename(columns=new_column_names)

    file_name=f"{columnName[:-4]}_interp.csv"
    save_path=os.path.join(root,file_name)
    interp_data.to_csv(save_path) 

    return(df,interp_data)

# %%
def create_individual_plots(interp_data,raw_data,root):

    y_label=r'$\theta$ (deg)'
    subject=        root.split('\\')[5]
    task=           root.split('\\')[6]
    joint=          root.split('\\')[7]
    orientation=    root.split('\\')[8]
    mocap='Noraxon'

    plot_name=f"{subject}_{task}_{joint}_{orientation}_{mocap}"

    MaxIndex = len(interp_data)

    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, ncols=1, sharex=False,figsize=(18, 27))
        
    ###################################################-RAW_ax0-################################################### 

    column_labels=raw_data.columns.unique()   

    for column in column_labels:
        ax0.plot(raw_data[[column]], label=column[-3:])


    handles, labels = ax0.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax0.legend([x for x in by_label.values()], [x for x in by_label.keys()], fontsize=8)   
    ax0.set_title(f"{plot_name}_raw",size=15) 
    ax0.set_ylabel(y_label, size=15)
    ax0.set_xlabel('Frame Number (60fps)', size=15)
    ###################################################-Interpolated_ax1-###################################################

    column_labels=interp_data.columns.unique()   

    for column in column_labels:
        ax1.plot(interp_data[[column]], label=column[-3:])

    ax1.legend(fontsize=8)
    ax1.set_title(f"{plot_name}_interpolated",size=15)
    ax1.set_ylabel(y_label, size=15)
    ###################################################-MEAN_STDEV_ax2-###################################################
    spm1d.plot.plot_mean_sd(interp_data.T, ax=ax2, linecolor='b', edgecolor='b', facecolor=(0.7,0.7,1), label='Mean & Stddev')

    ax2.legend(fontsize=8)
    ax2.set_title(f"{plot_name}_mean_stdev",size=15)


    for ax in [ax1, ax2]:

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
        ax.set_ylabel(y_label, size=15)


    fig.suptitle(f'{plot_name}',size=22,y=0.92)

    # plt.show()
    image_file_path=os.path.join(root,f"{plot_name}_image.png")
    plt.savefig(image_file_path)
    plt.close(fig)

# %%
# paths=find_file_paths('T01', 'Elbow', 'Right')[0]
# file_path=paths[0]
# root= paths[1]
# raw_data, interp_data=interpolate_data_from_file_path(file_path,root)
# create_individual_plots(interp_data,raw_data,root)

# %%
for task in ['T01','T02','T03','T04','T05','T06','T07','T08','T09','T10','T11','T12','T13','T14']:
    for paths in find_file_paths(task, 'Elbow', 'Right'):
        file_path=paths[0]
        root= paths[1]

        raw_data, interp_data=interpolate_data_from_file_path(file_path,root)
        create_individual_plots(interp_data,raw_data,root)


