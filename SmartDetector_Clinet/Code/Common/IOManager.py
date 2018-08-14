# -*- coding: utf-8 -*-

class IOMgr(object):
    def WriteToFile(self,path,str):
        print(path+"||"+str)
        try:
            FileHandle = open(path, 'w')
            FileHandle.write(str)
            FileHandle.close()
        finally:
            if (FileHandle):
                FileHandle.close()

    def PrintFile(self,path):
        try:
            FileHandle = open(path,"r")
            while True:
                chunk = FileHandle.readline()
                if not chunk:
                    break
                print(path+chunk)
            FileHandle.close()
        finally:
            if(FileHandle):
                FileHandle.close()
