Simple Restufl API built with Flask and SQLAlchemy

Required Stack
==============
Python 2.7
Python Virtual Environments
MySql 5.5 or higher


Steps to delpoy and run:
=======================

1 - Activate virtual environment: source venv/bin/activate
2 - Configure DB settings: mv db.conf.example db.conf then fill with your db credentials 
3 - Migrate Database : flask db migrate && flask db upgrade
4 - Run Tests : nosetests -s
5 - Enjoy reviewing my code :)
