set now_d=%cd%
cd..
set back_d=%cd%
pyuic4 -o %back_d%\ui_Sales_SelectCus.py %now_d%\Sales_SelectCus.ui