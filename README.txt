This is a project for demonstrating several server task.
1. Managing diffrent request types.
2. Handling CRUD commands using sql databases.
3. Implement authentification and user registration. 
4. Managing endpoint routing and access restrictions.

In this case the DB and the server runs on a Virtual machine powered by VirtualBox.
Vagrant is the software that sets up your VM and let you share documents from your local machine and your VM.
This requires vagrant to install Linux on your VM so it may take a while. 

Install VirtualBox:

https://www.virtualbox.org/wiki/Download_Old_Builds_5_1

To install Virtualbox use the link above and install the platform package for your os. You won't need the extension 
packages. You don't need to run Virtualbox after installation. Vagrant will do that for you.

Install Vagrant:

https://www.vagrantup.com/downloads.html

To install Vagrant use the link above.

Get the necessary files and set up vagrant:

https://github.com/udacity/fullstack-nanodegree-vm

Fork and clone the repo above. Once you done that navigate to the repo where you see a directory called vagrant. 
Change to this directory and run the command: vagrant up. If it is the first time, this will cause the installation 
of linux and may take a while. Once this is done, you can always start your VM using the command vagrant up. 
Eitherway to log on to your vm us the commant: vagrant ssh. After your log in was sucessfully, you have access to 
all the files in your local directory from where you setted up vagrant. 

Create the db:

Change to the directory with all the python files.To create the necessary database called parts.db 
run the command python setupDb.py. This will initialize the parts database.

Add items to the db:
Run python addparts.py to add pseudo users, categories and some parts to the db.

Run the server:
Run python catalog.py to actually run the server. In your favorite browser go to http://localhost:5000 and you'll
see the main page of the server.

Get JSON data:
To easy scrape the data of the db. You can use the end point /JSON. There will be found the json formatted content 
of all parts which are in the db. 