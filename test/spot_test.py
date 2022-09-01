#!/usr/bin/env python3
#m bobak, run gleaner+nabu then check the values against expected
cfg="mb_ci"
import ec
ec.local()
def g_cmd(cmd):
    cs=f'./glcon {cmd} --cfgName {cfg}'
    ec.os_system(cs)

def g_cfg_gen(cmd="config generate"):
    g_cmd(cmd)

def gleaner(gcmd="batch"):
    cmd=f'gleaner {gcmd}'
    g_cmd(cmd)

def gleaner_setup(gcmd="setup"):
    gleaner(gcmd)

def nabu(gcmd="prefix"):
    cmd=f'nabu {gcmd}'
    g_cmd(cmd)

def new_run(new_cfg=None):
    global cfg
    if new_cfg:
        cfg=new_cfg
        g_cfg_gen()
        gleaner_setup()
    #only run anew when changes
    #g_cfg_gen()
    #gleaner_setup()
    gleaner()
    nabu()

def lb():
    print("=================================================")

def r1():
    report=ec.tsc()
    print(report) #archival, then cmp w/new run's endpoint

def r2():
    report2=ec.tsc(None,None,"https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql")
    print(report2) 

def all_new():
    lb()
    new_run()
    lb()
    r1()
    lb()
    r2()

all_new()
