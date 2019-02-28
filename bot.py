#!/bin/python
import os
import sys
import time
import hashlib
import requests
import xml.dom.minidom as minidom

try:
    import thread
except:
    import _thread as thread



__DIR__ = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, __DIR__ + "/dependencies")

import logger
import config
import emailer


class GitScannerBot:
    ts_start = 0
    max_live_time = 3600 - 50


    def __init__(self, file_loc):
        self.ts_start = time.time()
        self.email_ref = emailer.Emailer()

        logger.dump('Git Scanner Bot', 'good')
        
        self.username = ''
        self.password = ''
        self.notify_email = ''
        self.tracking_urls = []
        self.load_file(file_loc)


        thread.start_new_thread(self.watchdog, (self.max_live_time,))

        try:
            os.mkdir(__DIR__ + '/data/')
        except:
            pass
        
        self.main()


    #
    # Load file
    #
    def load_file(self, file_loc):
        with open(file_loc, 'r') as infile:
            for line in infile:
                line = line.replace('\r', '')
                line = line.replace('\n', '')
                line = line.replace('\t', '')

                line = line.strip()
                
                if line.startswith('email: ') == True:
                    line = line.replace('email: ', '')
                    line = line.strip()
                    line = line.lower()
                    logger.dump('notify email is %s' %(line), 'info')
                    self.notify_email = line


                if line.startswith('username: ') == True:
                    line = line.replace('username: ', '')
                    line = line.strip()
                    line = line.lower()
                    logger.dump('username is %s' %(line), 'info')
                    self.username = line

                if line.startswith('password: ') == True:
                    line = line.replace('password: ', '')
                    line = line.strip()
                    line = line.lower()
                    logger.dump('password is %s' %(line), 'info')
                    self.password = line


                if line == '':
                    continue

                if line.startswith('#') == True:
                    continue

                if line.startswith('http') == True:
                    logger.dump('[ %s ] loaded for tracking' %(line), 'good')
                    self.tracking_urls.append(line)


    
    #
    # watchdog
    #
    def watchdog(self, live_time):
        while 1:
            diff = time.time() - self.ts_start
            if diff >= live_time:
                os._exit(1)
            
            time.sleep(2)
        
    
    
    #
    # Gen ID
    #
    def gen_id(self, input):
        input = input.encode('utf-8')
        id = hashlib.sha256(input).hexdigest()
        return id
    


    #
    # Save last title
    #
    def save_last_title(self, id, url, title):
        id_dir = __DIR__ + '/data/' + id + '/'

        try:
            os.mkdir(id_dir)
        except:
            pass

        # CHECK OLD TITLE ##############################
        is_title_changed = False
        try:
            infile = open(id_dir + '/last_title', 'r')
            line = infile.readline()
            line = line.replace('\r', '')
            line = line.replace('\n', '')
            line = line.replace('\t', '')
            infile.close()

            old_title = line
            if old_title != title:
                is_title_changed = True
            
        except:
            is_title_changed = True
        
        # EOF CHECK OLD TITLE ##########################

        if is_title_changed == True:
            logger.dump('New release detected "%s" for %s' %(title, url), 'good')

            try:
                outfile = open(id_dir + '/last_title', 'w')
                outfile.write(title)
                outfile.flush()
                outfile.close()
            except:
                pass
            

            try:
                os.remove(id_dir + '/sent')
            except:
                pass



    #
    # Check URL
    #
    def process_url(self, id, url):

        title = 'Error'

        try:
            headers = {
                'User-Agent': config.c['user_agent'],
            }

            errors = 0
            while errors < 5:
                try:
                    logger.dump('Checking %s' %(url), 'info')
                    
                    res = requests.get(url, timeout=5, headers=headers, verify=False)
                    errors = 10
                    break
                except:
                    errors += 1
                    pass
                
            

            obj = minidom.parseString(res.text)
            entry = obj.getElementsByTagName('entry')[0]
            title = entry.getElementsByTagName('title')[0]
            title = title.childNodes[0]
            title = title.nodeValue

            self.save_last_title(id, url, title)
        except:
            logger.dump('process_url(%s): %s' %(url, str(sys.exc_info())), 'error')
        

        can_send = True
        id_dir = __DIR__ + '/data/' + id + '/'

        if os.path.isfile(id_dir + '/sent') == True:
            can_send = False
        


        return {
            'title': title,
            'can_send': can_send,
        }
    

    #
    # Check last sent
    #
    def set_last_sent(self, id):
        id_dir = __DIR__ + '/data/' + id + '/'

        try:
            os.mkdir(id_dir)
        except:
            pass
        

        try:
            outfile = open(id_dir + '/sent', 'w')
            outfile.close()
        except:
            pass
        
    

    #
    # Send email
    #
    def send_email(self, id, email, url, title):
        
        url = url.rstrip('.atom')

        subject = 'New release "%s" of %s' %(title, url)
        
        text = ''
        text += '<h1>' + url + '</h1>'
        text += '<h3>New release detected "%s"</h3>' %(title)

        res_email = self.email_ref.send(self.username, self.password, subject, email, text)
        logger.dump('[ %s ] Sending email to %s - new release \'%s\' of %s' %(res_email, email, title, url), 'good')
        
        if res_email == True:
            self.set_last_sent(id)
        
    

 
    #
    # Main thread
    #
    def main(self):


        for url in self.tracking_urls:
            
            id = self.gen_id(url + self.notify_email)
            res = self.process_url(id, url)

            if res['can_send'] == True:
                self.send_email(id, self.notify_email, url, res['title'])



if __name__ == '__main__':
    n = GitScannerBot(sys.argv[1])


