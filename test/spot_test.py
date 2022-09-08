#!/usr/bin/env python3
#m bobak, run gleaner+nabu then check the values against expected
#add timing for mockup, and expand final dropoff printout to be multiline like in
# https://github.com/earthcube/geocodes_documentation/wiki/DataValidationReportMockup
#will split out lines like this: print('sitemap-count:{sml}, Error count:{ls1}, missing:{loose_s2s}')
# from present compact return format: dropoff=f'sitemap:{sml}-{lsl}:{lose_s2s} =>{dropoff2}'
cfg="mb_ci"
import ec
import logging
import os

logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s', level=os.environ.get("LOGLEVEL", "INFO"), stream=sys.stdout)

reportfile = logging.getLogger("reports")
log = logging.getLogger()

ec.local()
def g_cmd(cmd):
    cs=f'./glcon {cmd} --cfgName {cfg}'
    log.debug( ec.os_system(cs) )

def g_cfg_gen(cmd="config generate"):
    log.info("calling cibfug generate")
    g_cmd(cmd)

def gleaner(gcmd="batch"):
    cmd=f'gleaner {gcmd}'
    log.info("calling gleaner batch")
    g_cmd(cmd)

def gleaner_setup(gcmd="setup"):
    log.info("calling gleaner setup")
    gleaner(gcmd)

def nabu(gcmd="prefix"):
    log.info("calling nabu prefix")
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
    reportfile.info("=================================================")

def r1():
    report=ec.tsc()
    reportfile.info(report) #archival, then cmp w/new run's endpoint

def r2():
    report2=ec.tsc(None,None,"https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql")
    reportfile.info(report2)

def all_new(new=None):
    import time
    start_sec=time.time()
    start=ec.now()
    reportfile.info(f'Start:{start}')
    if new:
        lb()
        new_run()
    lb()
    r1()
    lb()
    r2()
    end_sec=time.time()
    elapse_sec=end_sec - start_sec
    end=ec.now()
    #print(f'End:{end}') #get w/elapse Runtime, instead
    reportfile.info(f'Elapse:{elapse_sec} seconds')

all_new()
