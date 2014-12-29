The last few months I'm working with OpenERP running on a PostgreSQL database, a complete opensource ERP and CRM system written in Python. I was amazed how easy it is to change the system the way you want by building your own modules.

One of the modules I wrote, is a module to send faxes and to handle the situation if a fax was not send succesfully (line busy or something). I used interfax.net as fax provider and integrated this api in my module 'sendfax'. The module is written for OpenERP 6.1

I used a batch wise approach for sending faxes and retrieving there results, meaning when installing the faxsend module a new task is added to the OpenERP scheduler called 'Send fax Service'. This task is executed every 15 minutes and looks for faxes to send and tries to retrieve results from faxes send previously. Of cource you can change the interval of 15 minutes in the way you want it to have.

If you are interested you can download my sendfax module from sourceforge or getting it from launchpad with bzr branch lp:sendfax. If you need help, feel free to contact me bas at ubbels dot com

installation notes 'faxsend' for openerp 6.1
For using this module the following python packages are needed :
ZSI (Python webservices package http://pywebsvcs.sourceforge.net/)
PyXML (used by ZSI)
interfax (you will find it on www.interfax.net)
IMPORTANT: To let sendfax work correctly you have to change/add some code in interfax:
open 'client.py' and find the method 'sendFax'
change 'fileBytes = file(filename).read()' into :
fo = open(filename, 'rb')
fileBytes = fo.read() # file should not be to big
fo.close()
		
now you can send binary files
create a new method 'sendFaxStream':
def sendFaxStream(self,faxNumber,dataStream,dataType):
	req = SendfaxSoapIn()
	req._Password = self._password
	req._Username = self._username
	req._FaxNumber = faxNumber
	req._FileData = dataStream
	req._FileType = dataType
	result = self._outboundProxy.Sendfax(req)._SendfaxResult
	return result
		
now you can send a binary data stream (without creating a file)
To use sendfax you must tell OpenERP your interfax account, you find this option under:
'settings->configuration->fax->Send fax account (visible after installing the 'faxsend' module)

To send a report as a fax from your own module you must call the following methods:
faxsend_pool = self.pool.get('faxsend.queue')
faxsend_pool.send_report_by_fax(cr, uid, o.id, account='accountname',
	subject='subject you like',
	report='name of the report, without report.',     # e.g. account.invoice
	faxno='faxnummer, please include the country dialing code -> +49282112344',
	triggerModel='modelname to trigger',
	triggerMethod='method to trigger',
	triggerArgs='args to pass')
		


trigger method example:
def trigger_faxresult(self, cr, uid, faxResult, sendPages, sendDuration, args=None):
	if args:
	    self.write(cr, uid, args, { 'fax_result' : faxResult })
		
You can also send an attachment from the OpenERP document management system as fax, in this case use faxsend_pool.send_attachement_by_fax. The document you want to send is taken from 'ir.attachment', you need to know the 'res_id' and the corresponding 'res_model' from the document.

faxsend_pool = self.pool.get('faxsend.queue')
faxsend_pool.send_attachment_by_fax(cr, uid, 
	o.id, # res_id from record in ir.attachment
	account='accountname you created under fax settings',
	subject='subject you like',
	model='account.invoice',   # e.g. if you want to send  an invoice
	faxno='faxnummer, please include the country dialing code -> +49282112344',
	triggerModel='modelname to trigger', # only use this parameters 
	triggerMethod='method to trigger',   # if you want to manage
	triggerArgs='args to pass')          # the send results

















Welcome to the InterFAX Python Toolkit!
-------------------------------------------

This project provides a ready-to-use Python module for accessing the 
InterFAX web service. For information about the InterFAX 
web service please see: http://www.interfax.net/

You will need a InterFAX developer account to use this toolkit.
If you don't have an account, please create one here: 
http://www.interfax.net

You must have Python installed with the Zolera SOAP Infrastructure (ZSI)
module to use this toolkit.

Getting Started.
* The examples directory in this toolkit contains several simple Python
  programs that exercise each of the methods in the InterFAX SOAP
  service.  To run them, you will have to make sure the interfax 
  Python module is on your PYTHONPATH and you will have to edit each 
  program to provide your username and password and possibly other
  information.  These examples are a good place to start.

In a Nutshell.
* The InterFAX Python module needs to be on your PYTHONPATH.
* Usage of the library is simple, just create an instance of PmClient 
  and call its methods which correspond to the web service calls provided by
  the InterFAX web service.  Here's an example:

from interfax import client
print 'Testing SendCharFax...'
c = client.InterFaxClient('USERNAME','PASSWORD')
result = c.sendCharFax('+12125554874', 'This is a test')
print '   Char Fax was sent with result code: %d' % result


More Information.
* The PyDoc information for the PmClient class is a good place to 
  look for more details.
* The InterFAX user support forums are a great place to get more 
  information and help using this toolkit and the InterFAX web
  service: http://forum.interfax.net/

Build Details.
* SOAP interface classes were generated with the ZSI tool wsdltopy
  invoked as shown below on both of the InterFAX WSDL documents.

$ wsdl2py --url http://ws.interfax.net/dfs.asmx?wsdl
$ wsdl2py --url http://ws.interfax.net/inbound.asmx?wsdl
