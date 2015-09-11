# -*- coding:utf-8 -*-
################################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
################################################################################
'''
Created on 2015年3月11日

@author: wanhao01
'''

import Queue
import sys
import threading

import com.onehao.mlogger as mlogger


class CrawlerThread(threading.Thread):
    '''
    mini spider thread encapsulation.
    '''
    worker_count = 0   
    def __init__(self, workQueue, resultQueue, timeout=0, **kwds):   
        threading.Thread.__init__(self, **kwds)   
        self.id = CrawlerThread.worker_count   
        CrawlerThread.worker_count += 1   
        self.setDaemon(True)   
        self.workQueue = workQueue   
        self.resultQueue = resultQueue   
        self.timeout = timeout   
        self.start()
        self.__logger = mlogger
         
    def run(self):   
        ''' the get-some-work, do-some-work main loop of worker threads '''   
        while True:   
            try:   
                callable, args, kwds = self.workQueue.get(timeout=self.timeout)   
                res = callable(*args, **kwds)   
                print(res)
                self.__logger.loginfo("worker[%2d]: %s" % (self.id, str(res)))
                self.resultQueue.put(res)   
            except Queue.Empty:
                self.__logger.loginfo('the thread pool is empty.')   
                break   
            except Exception as ex:
                #print 'worker[%2d]' % self.id, sys.exc_info()[:2]  
                self.__logger.logerror('worker[%2d]' % self.id) 
                self.__logger.logerror(str(sys.exc_info()[:2]))
                

class ThreadPool(object):
    '''
    thread pool used to handle multiple thread.
    '''
    def __init__(self, num_of_workers=10, timeout=1):   
        self.workQueue = Queue.Queue()   
        self.resultQueue = Queue.Queue()   
        self.workers = []   
        self.timeout = timeout   
        self._recruitThreads(num_of_workers)
        self.__logger = mlogger
          
    def _recruitThreads(self, num_of_workers):   
        for i in range(num_of_workers):   
            worker = CrawlerThread(self.workQueue, self.resultQueue, self.timeout)   
            self.workers.append(worker) 
    
    def wait_for_complete(self):
        '''
        the function uses to wait for the exiting of all the threads.
        '''
        while len(self.workers):   
            worker = self.workers.pop()   
            worker.join()   
            if worker.isAlive() and not self.workQueue.empty():   
                self.workers.append(worker)   
        print "All jobs are are completed."  
    
    def add_job(self, callable, *args, **kwds):
        '''
        add job to the thread pool.
        '''
        self.workQueue.put((callable, args, kwds)) 
        
    def get_result(self, *args, **kwds):
        '''
        get the result from the result Queue.
        '''   
        return self.resultQueue.get(*args, **kwds) 