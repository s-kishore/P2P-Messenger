'''
Created on Aug 7, 2018
@author: krish
'''
import time,os,wx,sys,socket
import traceback
from wx.lib.masked import IpAddrCtrl
from _thread import start_new_thread

port=6300
app_icon = 'app.ico'

class Main_wd(wx.Frame):
    dest_ip=''
    logfl = None

    def __init__(self,parent, title):
        super(Main_wd,self).__init__(parent,title = title,size=(600,500))
        
        self.intilize()
        self.Center()
        self.Show()
        self.Logger('Application Opened')
        start_new_thread(start_server,(self,))

    def intilize(self):
        icon = resource_path(app_icon)
        self.SetIcon(wx.Icon(icon, wx.BITMAP_TYPE_ICO))
        self.populateMenu()
        self.populateBars()
        self.populateControls()
        self.DisableDISCON(True)

    def DisableDISCON(self,x):
        if x:
            self.ip_box.Enable()
            self.con_btn.Enable()
            self.dcon_btn.Disable()
            self.chat_send_btn.Disable()
            self.flsend_btn.Disable()
        else:
            self.ip_box.Disable()
            self.con_btn.Disable()
            self.dcon_btn.Enable()
            self.chat_send_btn.Enable()
            self.flsend_btn.Enable()

    def populateMenu(self):
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        view_menu = wx.Menu()
        
        qtbtn = wx.MenuItem(file_menu, 0 , 'Quit \tCtrl+Q')
        qtbtn.SetHelp('Quit Application')
        self.Bind(wx.EVT_MENU, self.OnQuit, id=0)
        
        self.shstb = view_menu.Append(wx.ID_ANY,'Show StatusBar\tF6','Hide/UnHide StatusBar',kind= wx.ITEM_CHECK)
        view_menu.Check(self.shstb.GetId(),True)
        self.Bind(wx.EVT_MENU, self.onSHSTB, self.shstb)
        
        file_menu.Append(qtbtn)
        
        menubar.Append(file_menu, '&File ')
        menubar.Append(view_menu, '&View ')
        self.SetMenuBar(menubar)
        
    def populateBars(self):
        self.StatusBar = self.CreateStatusBar()
        self.StatusBar.SetStatusText('Ready: Listening for Incoming Connections')
        self.ToolBar = self.CreateToolBar()
    
    def populateControls(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.SetDimension((0,0),(500,400))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        ip_lbl = wx.StaticText(panel,label='Enter Destination IP: ')
        self.ip_box = IpAddrCtrl(panel)
        
        hbox.Add(ip_lbl,flag=wx.RIGHT)
        hbox.Add(self.ip_box)
        
        vbox.Add(hbox,flag=wx.ALIGN_CENTER_HORIZONTAL|wx.RIGHT|wx.TOP, border=10)
        vbox.Add((-1,5))
        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.con_btn = wx.Button(panel,label='Connect',size=(70,30))
        hbox2.Add( self.con_btn)
        
        self.Bind(wx.EVT_BUTTON, self.onConnect,  self.con_btn)
         
        self.dcon_btn = wx.Button(panel,label='Disconnect',size=(70,30))
        hbox2.Add(self.dcon_btn)
        self.Bind(wx.EVT_BUTTON, self.onDisconnect, self.dcon_btn)
        
        vbox.Add(hbox2,flag=wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM, border=10)
        vbox.Add((-1,5))
        
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.chat_box = wx.TextCtrl(panel,size=(500,200),style = wx.TE_MULTILINE|wx.TE_READONLY)
        hbox3.Add(self.chat_box,wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
        vbox.Add(hbox3,flag= wx.ALIGN_CENTER_HORIZONTAL)
        
        vbox.Add((-1,10))
        
        hbox4 = wx.BoxSizer(wx.HORIZONTAL) 
        self.chat_type = wx.TextCtrl(panel,size=(380,40),style=wx.TE_MULTILINE) #| wx.TE_AUTO_SCROLL
        hbox4.Add(self.chat_type,wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL)
        self.Bind(wx.EVT_TEXT_ENTER, self.onSend, self.chat_type)
        
        self.flsend_btn = wx.Button(panel,label="Send File",size=(70,40))
        hbox4.Add(self.flsend_btn,flag = wx.ALIGN_CENTER_HORIZONTAL)
        self.Bind(wx.EVT_BUTTON, self.onAttachClick, self.flsend_btn)
        
        self.chat_send_btn = wx.Button(panel,label="Send",size=(70,40)) 
        hbox4.Add(self.chat_send_btn,flag = wx.ALIGN_CENTER_HORIZONTAL)
        self.Bind(wx.EVT_BUTTON, self.onSend, self.chat_send_btn)   
        
        vbox.Add(hbox4,flag = wx.ALIGN_CENTER_HORIZONTAL)
        vbox.Add((-1,25))
        
        panel.SetSizer(vbox)
        
    def onSHSTB(self,e):
        if self.shstb.IsChecked():
            self.StatusBar.Show()
        else:
            self.StatusBar.Hide()       
    
    def OnQuit(self,e):
        self.closeLog
        self.Close()
    
    def onDisconnect(self,e):
        self.Logger('Disconnect requested')
        self.DisableDISCON(True)
        self.StatusBar.SetStatusText('Ready: Listening for incoming connections')
        self.Logger('Disconnect Successful')

    def onConnect(self,e):
        self.local_ip = str(socket.gethostbyname(socket.gethostname()))
        self.dest_ip = self.ip_box.GetValue().replace(' ','')
        self.Logger('Connect Requested from ' + str(self.local_ip) + " to " + self.dest_ip)
        
        if self.SendData('Connection established with ' + self.local_ip):
            self.DisableDISCON(False)
            self.StatusBar.SetStatusText('Ready: Connected to' + self.dest_ip)
            self.update_chat('Connection established with ' + self.dest_ip,'system')
        else:
            self.update_chat('Failed to Connect to ' + self.dest_ip,'system')
            
    def onAttachClick(self,e):
        file_choose = wx.FileDialog(None,message='Send File',style=wx.FD_OPEN,size=(70,40))
        
        if file_choose.ShowModal() == wx.ID_CANCEL:
            pass
        else:
            self.onFileSend(file_choose.GetPath())
        
    def onFileSend(self,file_loc):
        if os.path.getsize(file_loc) < 15728640:
            file_out = open(file_loc,'rb')
            f_data = file_out.read()
            f_name = file_out.name.split('\\')
            f_name = f_name[len(f_name)-1]
            file_out.close()
            
            self.SendData('%%%file%%%')
            self.SendData('%%%file_name%%% ' + f_name)
            self.SendData('%%%file_len%%% ' + str(len(f_data)))
            self.SendData('%%%file_data%%% ' + f_data)
            self.SendData('%%%file_end%%% ')
            self.update_chat('File ' + f_name + 'of size ' + str(len(f_data)/1024) + ' KB sent','ougoing')
        else:
            self.update_chat('File Size too large. Limit 15MB','system')
        
    def onSend(self,e):
        data = self.chat_type.GetValue().rstrip()
        if self.SendData(data):
            self.update_chat(data,'outgoing')
            self.chat_type.Clear()
        else:
            self.update_chat("Error Sending data",'system')
        

    def SendData(self,data):
        # Conver string to bytes
        data = str.encode(data)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connOut:
                connOut.connect((self.dest_ip, port))
                connOut.sendall(data)
                connOut.close()
            self.connIn.sendall(data)
        except:
            self.Logger('connection establish error' + str(sys.exc_info()[0]))
            traceback.print_exc()
            print (sys.exc_info()[0])
            return -1
        else:
            return 1
    
    def update_chat(self,data,dir):
        if dir == 'outgoing':
            self.chat_box.AppendText('\n' + 'Me: '+ data + ' \n')
            self.Logger('Data Sent: ' + str(len(data)) + ' bytes') 
        elif dir == 'system':
            self.chat_box.AppendText('\n' + 'SYS MSG: '+ data + ' \n\n')
            self.Logger(data) 
        else:
            self.chat_box.AppendText('\n' + 'Partner: '+ data + ' \n')
            self.Logger('Data Received: ' + str(len(data)) + ' bytes') 
                   
    def Logger(self,msg):
        date = time.asctime( time.localtime(time.time()) )
        try:
            if self.logfl != None:
                self.logfl.write('\n' + str(date) + ' ' + str(msg))
        except:
            traceback.print_exc()
            self.logfl=open('app_log.txt','a')
            self.logfl.write('\n' + date + " " + str(msg))
    
    def closeLog(self):
        try:
            self.logfl.write('Closing Application')
            self.logfl.close()
        except:
            traceback.print_exc()
            pass
           
def start_server(self):
    self.dest_ip = str(self.ip_box.GetValue()).replace(" ", "")
    try:
        self.connIn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connIn.bind(('',port))
        self.connIn.listen(1)

    except socket.error as e:
        traceback.print_exc()
        print (str(e))
    except TypeError as e:
        traceback.print_exc()
        print (str(e))
    except:
        traceback.print_exc()
        self.Logger(str(sys.exc_info()[0]) + 'error')
    self.Logger('Socket created and Listening on port '+ str(port))
    enbl=0
    
    while 1:
        client,addr = self.connIn.accept()
        self.Logger('connected to ' + str(addr))
        in_ip = str(addr[0])
        dest_ip = str(self.ip_box.GetValue()).replace(' ','')
        self.Logger('connected to ' + str(addr))
        down_size = 4096
        
        if len(dest_ip) < 7:
            self.ip_box.SetValue(in_ip)
            self.update_chat('Incoming Connection from ' + in_ip + ' accepted','system')
            dest_ip = in_ip
            
        if (in_ip != dest_ip):
            self.update_chat('Incoming Connection from ' + in_ip + ' Rejected','system')
            client.close() 
        
        else:
            if enbl == 0:
                self.DisableDISCON(False)
                enbl=1
            self.StatusBar.SetStatusText('Ready: Connected to' + in_ip)
            data = client.recv(down_size)
            
            if str(data).startswith('%%%file'):
                if data.startswith('%%%file_name%%% '):
                    file_name = data.strip('%%%file_name%%% ')
                
                elif data.startswith('%%%file_len%%%'):
                    down_size = int(data.strip('%%%file_len%%% '))
                    #print ('download size ' + str(down_size))
                    
                elif data.startswith('%%%file_data%%% '):
                    file_data = data.strip('%%%file_data%%% ')
                    down_size=4096
                    
                elif data.startswith('%%%file_end%%%'):
                    downloadFile(self,file_name,file_data)
                    
            else:
                if not data: break
                self.update_chat(data,'incoming')
        
    self.StatusBar.SetStatusText('Ready: Listening for incoming connections')    
    client.close()
    self.DisableDISCON(True)  

def downloadFile(self,name,data):
    file = open(name,'wb')
    file.write(data)
    file.close()
    self.update_chat('File ' + name + ' of size '  + str(len(data)/1024) + ' KB received','incoming')
    
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        return os.path.join(base_path, relative_path)
    except Exception:
        traceback.print_exc()
        base_path = os.path.abspath(".")
    return relative_path

if __name__ == '__main__':
    app= wx.App()
    Main_wd(None,'P2P Messenger Ver. 1.0')
    app.MainLoop()
