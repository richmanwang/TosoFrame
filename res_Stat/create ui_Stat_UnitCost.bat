set now_d=%cd%
cd..
set back_d=%cd%
pyuic4 -o %back_d%\ui_Stat_UnitCost.py %now_d%\Stat_UnitCost.ui