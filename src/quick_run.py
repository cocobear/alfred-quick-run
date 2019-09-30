#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from workflow.notify import notify
from workflow import Workflow


GITHUB_SLUG = 'cocobear/alfred-quick-run'
def main(wf):
    import subprocess
    import yaml
    import os

    from subprocess import Popen, PIPE, STDOUT
    from yaml.scanner import ScannerError

    log = wf.logger.debug
    #log = print
    args = wf.args

    if (len(args) != 1):
        print('Usage: python quick_run.py <PATTERN>')
        return 1
    if wf.update_available:
        wf.add_item(u'有更新,回车开始更新',
                    autocomplete='workflow:update',
                    valid=False,
                    icon=('cloud-download.png'))
    rgbin = subprocess.check_output("which rg ", shell=True).strip()


    query = u"" + args[0]
    data_path = os.environ.get('data_path', 'None')
    log('\nquery: '+ str([query]) + '\n' + 'data_path: ' + data_path)

    results = []
    cmds = []
    remarks = []
    if os.path.isdir(data_path):
        p = subprocess.Popen([rgbin, query, data_path], stdout=PIPE, stderr=STDOUT)
        output = p.communicate()[0]
        output = output.decode('utf-8')
        results = output.split('\n')[:-1]

        for i in range(len(results)):
            cmd = results[i].split(':')[1]
            wf.logger.debug(results[i])
            wf.add_item(cmd,
                subtitle=cmd,
                arg= cmd,
                valid=True,
                icon='icon.png')
        wf.send_feedback()
        return 0

    with open(data_path, 'r') as f:
        try:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if not data:
                wf.add_item('配置文件为空',
                    subtitle=u'回车打开配置文件进行编辑',
                    arg= 'open',
                    valid=True,
                    icon='error.png')
                wf.send_feedback()
                return 1
            for i in data:
                for j in i['values']:
                    cmds.append(j['cmd'])
                    remarks.append(j['remark'])
        except (KeyError, ScannerError), e:
            log(e)
            log(e.note)
            log(e.problem)
            log(e.problem_mark)
            wf.add_item(u'错误:'+str(e.problem_mark),
                subtitle=u'回车打开配置文件进行编辑',
                arg= 'open',
                valid=True,
                icon='error.png')
            wf.send_feedback()
            return 1


    #wf.logger.debug(u"""\n""".join(cmds).encode('utf-8'))
    p = subprocess.Popen([rgbin,'--line-number', query], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    output = p.communicate(input=u"""\n""".join(cmds).encode('utf-8'))[0]

    wf.logger.debug('cmds search result: '+ output)
    log(type(output))
    if not len(output):
        p = subprocess.Popen("%s --line-number '%s' " %(rgbin, query),
                shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        output = p.communicate(input=u"""\n""".join(remarks).encode('utf-8'))[0]

        wf.logger.debug('remarks search result: '+ output)
    if len(output):
        results = output.split('\n')[:-1]
        for i in range(len(results)):
            idx = int(results[i].split(':')[0])-1
            wf.add_item(remarks[idx],
                    subtitle=cmds[idx],
                    arg = cmds[idx],
                    valid=True,
                    icon="icon.png")
        wf.send_feedback()
    if not len(output):
        wf.add_item(u'打开配置文件', subtitle=u'配置文件默认保存在安装目录下',
                arg= 'open', valid=True, icon='icon.png')
        wf.send_feedback()
    return 0


if __name__ == '__main__':
    wf = Workflow(update_settings={'github_slug': GITHUB_SLUG})
    sys.exit(wf.run(main))
