import win32com.client
wmi = win32com.client.GetObject("winmgmts:")
for serial in wmi.InstancesOf("Win32_SerialPort"):
       print (serial.Name, serial.Description)