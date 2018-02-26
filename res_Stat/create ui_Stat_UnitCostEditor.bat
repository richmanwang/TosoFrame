set now_d=%cd%
cd..
set back_d=%cd%
pyuic4 -o %back_d%\ui_Stat_UnitCostEditor.py %now_d%\Stat_UnitCostEditor.ui