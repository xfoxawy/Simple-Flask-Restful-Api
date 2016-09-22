Simple Restufl API built with Flask and SQLAlchemy

Required Stack
==============
Python 2.7 <br>
Python Virtual Environments <br>
MySql 5.5 or higher <br>


Steps to delpoy and run:
=======================

1 - Activate virtual environment: source venv/bin/activate <br>
2 - Configure DB settings: mv db.conf.example db.conf then fill with your db credentials  <br>
3 - Migrate Database : flask db migrate && flask db upgrade <br>
4 - Run Tests : nosetests -s  <br>
5 - Enjoy reviewing my code :) <br>
