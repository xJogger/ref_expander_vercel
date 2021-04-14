# webio整合flask需要
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
# 脚本需要
from pywebio.input import *
from pywebio.output import *
from pywebio.session import set_env
# 自己程序需要
import re

'''
说明：
将Mentor产生的压缩位号（U5-C10）粘贴到下面，运行之后输出未压缩的位号（U5,U6,U7,U8,U9,U10）
'''

# 自己程序
def expand_ref(compressed_ref):
    if '-' not in compressed_ref:
        return compressed_ref
    else:
        start = int(re.findall('\\d+', compressed_ref)[0])
        end   = int(re.findall('\\d+', compressed_ref)[1])
        pre_fix = re.findall('[a-zA-Z]+', compressed_ref)[0]
        numbers = list(range(start,end+1))
        expanded_ref = ','.join(map(lambda x:pre_fix+str(x),numbers))
        return expanded_ref

# 自己程序
def expand_line(compressed_line):
    refs = compressed_line.split(',')
    for i,ref in enumerate(refs):
        refs[i] = expand_ref(ref)
    return ','.join(refs)

# 自己程序
def task_func():
    set_env(title="Ref Expander")
    put_markdown('本页面可以将压缩位号（U5-C10）转换为未压缩的位号（U5,U6,U7,U8,U9,U10）。')
    str2process = textarea('输入压缩位号：', rows=15, placeholder='可多行，行内逗号分割。')
    lines = str2process.split('\n')
    for i,line in enumerate(lines):
        lines[i] = expand_line(line)
    expanded_lines = '\n'.join(lines)
    put_markdown('未压缩的位号为：')
    put_markdown(expanded_lines)

# Flask+WebIO框架
app = Flask(__name__)

# `task_func` is PyWebIO task function
app.add_url_rule('/', 'webio_view', webio_view(task_func),
            methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods


