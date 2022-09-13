#!/usr/bin/env python3
#m bobak, run gleaner+nabu then check the values against expected
#add timing for mockup, and expand final dropoff printout to be multiline like in
# https://github.com/earthcube/geocodes_documentation/wiki/DataValidationReportMockup
#will split out lines like this: print('sitemap-count:{sml}, Error count:{ls1}, missing:{loose_s2s}')
# from present compact return format: dropoff=f'sitemap:{sml}-{lsl}:{lose_s2s} =>{dropoff2}'
#cfg="mb_ci"
cfg="mb_ci3"
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
    #report=ec.tsc()
    report=ec.tscg() #should send in the params from yml or make it
    print(report) #archival, then cmp w/new run's endpoint

def r2():
    report2=ec.tsc(None,None,"https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql")
    print(report2) 

def all_new(new=None):
    import time
    start_sec=time.time()
    start=ec.now()
    ec.print2log(f'Start:{start}')
    if new:
        lb()
        new_run()
    lb()
    r1()
    lb()
    #r2() #no longer needed, 
    end_sec=time.time()
    elapse_sec=end_sec - start_sec
    end=ec.now()
    #print(f'End:{end}') #get w/elapse Runtime, instead
    ec.print2log(f'Elapse:{elapse_sec} seconds')

#all_new()
all_new(True)
