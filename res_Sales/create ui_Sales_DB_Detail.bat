set now_d=%cd%
cd..
set back_d=%cd%
pyuic4 -o %back_d%\ui_Sales_DB_Detail.py %now_d%\Sales_DB_Detail.ui