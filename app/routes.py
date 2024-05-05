from flask import Flask, render_template, request, session, url_for, redirect
import pandas as pd
import datetime
import base64
import re
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter, CustomJS, HoverTool
from bokeh.resources import CDN
from bokeh.embed import file_html
from os import listdir
from app import app
from time import sleep

def validate_input_file(filename: str) -> bool:
    pattern = re.compile('^[0-9]+;[0-9]+;[0-9]+;[0-9]+$')
    with open(data_folder + filename, 'r') as csv_file:
        lines = csv_file.readlines()
        for line in lines:
            if not pattern.match(line):
                return False
    return True

def create_figure(filename: str) -> 'plot':
    # try:
    #     csv = pd.read_csv(data_folder + filename,
    #                       parse_dates=['date'], sep=';')
    # except:
    #     sleep(15)
    #     csv = pd.read_csv(data_folder + filename,
    #                       parse_dates=['date'], sep=';')
    

    colnames=['time', 'value1', 'value2', 'value3']
    try:
        csv = pd.read_csv(data_folder + filename,  sep=';', 
                          names=colnames, header=None)
    except:
        sleep(5)
        csv = pd.read_csv(data_folder + filename, sep=';', 
                          names=colnames, header=None)
        
    plot_name = filename
    p = figure(title=plot_name, width=900, height=300)
    color = ['red', 'blue', 'green', 'pink', 'orange']
    for i in range(1, len(csv.columns)):
        p.line(x=csv['time']-csv['time'][0], y=csv[csv.columns[i]], line_color=color[i-1], legend_label=str(csv.columns[i]))
        # p.line(x=csv['date'], y=csv[csv.columns[i]], line_color=color[i-1], legend_label=str(csv.columns[i]))
        # p.xaxis.formatter = DatetimeTickFormatter(
        #     hours=["%H:%M"],
        #     days=["%H:%M"],
        #     months=["%H:%M"],
        #     years=["%H:%M"],
        # )
    p.xaxis.axis_label = 'time, ms'
    p.yaxis.axis_label = 'value'
    p.legend.location = 'bottom_right'
    p.add_tools(HoverTool(tooltips= [
      ('time', '$x'),
      ('value', '$y'),
    ], formatters={'@DateTime': 'datetime'}))
    # show(p)
    return p

@app.route('/')
def archive_page() -> 'html':
    date_mask = datetime.date.today().strftime("%Y-%m-%d")
    global data_folder
    data_folder = 'C:\\GitHub\\Graph-prog\\data\\'
    arch_names = [f for f in listdir(data_folder)]
    current_arch_name = request.args.get("arch_name")
    print('arch_name from args: ' + str(current_arch_name))
    if current_arch_name is None and len(arch_names) == 0:
        current_arch_name = 'data-example'
        arch_names.append(current_arch_name)
    elif current_arch_name is None:
        current_arch_name = arch_names[0]
    print('arch_name from logic: ' + str(current_arch_name))
    if validate_input_file(current_arch_name):
        plot = create_figure(current_arch_name)
        script, div = components(plot)
    else:
        validate_err_msg = '''Incorrect input file format. <br>
        Correct file format: <br>
        [int]time; [int]value1; [int]value2; [int]value3'''
        script, div = validate_err_msg, ''
    return render_template('archive.html', the_title=current_arch_name + ' to graph',
                           script=script, div=div,
                           arch_names=arch_names,
                           current_arch_name=current_arch_name)
