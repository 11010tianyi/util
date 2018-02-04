# _*_ coding: utf-8 _*_
__author__ = 'tiany'
__date__ = '2018/2/1 13.50'

import os,time,re,sys
import argparse,datetime
from collections import OrderedDict
###定义全局变量
ErrFile=[]
time_dict = OrderedDict()
##得到给定目录下的文件和子目录名称
def listdir(dir):
    dirList=[]
    fileList=[]
    for fileOrDir in os.listdir(dir):
        if os.path.isdir(fileOrDir):
            dirList.append(dir+"/"+fileOrDir)
        elif os.path.isfile(fileOrDir):
            fileList.append(dir+"/"+fileOrDir)
    return (fileList,dirList)


##检查qsub目录下的sh格式和投递qsub文件行数是否一致，所有的sh文件是否都check
def checkQsubDir(dir):
    global ErrFile
    (sh_file, ext) = os.path.splitext(os.path.splitext(dir)[0])
    sh_file_line_num = len(open(sh_file).readlines())
    qsub_sh_file_num=0
    qsub_check_file_num=0
    sh_time_dict = OrderedDict()
    check_time_dict = OrderedDict()
    global  time_dict
    for tmp in os.listdir(dir):
        if tmp.endswith("sh"):
            tmp = dir + "/" + tmp
            #print (tmp)
            sh_time_dict[tmp] = os.path.getmtime(tmp)
    for tmp in os.listdir(dir):
        if tmp.endswith("Check"):
            tmp = dir + "/" + tmp
            x = "heck"
            y = ".C"
            tmp = tmp.rstrip(x)
            tmp = tmp.rstrip(y)
            if tmp in sh_time_dict.keys():
                check_time_dict[tmp] = os.path.getmtime(tmp)
                check_file = tmp + ".Check"
                check_time = os.path.getmtime(check_file)
                #print(datetime.datetime.fromtimestamp(check_time))
                #print(datetime.datetime.fromtimestamp(sh_time_dict[tmp]))
                ##################################
                diff_seconds = (datetime.datetime.fromtimestamp(check_time)-datetime.datetime.fromtimestamp(sh_time_dict[tmp])).seconds
                diff_hours1 = diff_seconds/60
                diff_days = (datetime.datetime.fromtimestamp(check_time)-datetime.datetime.fromtimestamp(sh_time_dict[tmp])).days
                diff_hours2 = diff_days*24*60
                #print("diff_seconds ,hours1 ,diff_days ,hours2 : ",diff_seconds,diff_hours1,diff_days,diff_hours2)
                if diff_hours2 < 0:
                    pass
                else:
                    diff_time = diff_hours1 + diff_hours2
                    #print(tmp," : ",diff_time)
                    #ErrFile.append("%s use time :  %s" % (tmp,diff_time))
                    time_dict[tmp] = diff_time
                            #if sh_file_line_num != qsub_sh_file_num:
    #    ErrFile.append("%s line number is not equal the %s sh file number" %(sh_file,dir))
    #elif qsub_check_file_num != qsub_sh_file_num:
    #    ErrFile.append("some sh files donot have Check file from %s" %(dir))

def main():
    newParser = argparse.ArgumentParser(usage = "Usage: %s [options]" %(sys.argv[0]),version = "v1.0")
    newParser.add_argument("-d", dest="directory", help="the root directory for check error",required=True)
    newParser.add_argument("-o", dest="output", help="the out file to store error file",required=True)
    options = newParser.parse_args()
    optionsDict = options.__dict__
    ####
    directory = os.path.abspath(optionsDict["directory"])
    #print directory
    ####
    (logFiles,qsubLists)=([],[])
    for dirpath,dirnames,filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith("log"):
                logFiles.append(dirpath+'/'+filename)
        if dirpath.endswith("qsub"):
            qsubLists.append(dirpath)
    #print (logFiles,qsubLists)
    ErrFile.append("The log file : ")
    for file in logFiles:
        #print "logFile:"+file
        # f = open(file,"rb")
        # lineNum=0
        # for line in f.readlines():
        #     lineNum +=1
        #     if re.match("^\s*$",line):
        #         continue
        #     elif re.findall("No such file( or directory)*|Error|initialization",line):
        ErrFile.append(file)
        # f.close()

    for dir in qsubLists:
        checkQsubDir(dir)
    ######################
    print("Sort sh Check time : ")
    file_rtime_sort_dict = sorted(time_dict.items(), key=lambda d: d[1], reverse=True)
    for x in file_rtime_sort_dict:
        print(x[0] + " : " + str(x[1]))
    out = open(optionsDict["output"],"w")
    #sorted(ErrFile)
    out.write("\n".join(ErrFile))
    out.close()


if __name__ == "__main__":
    main()
