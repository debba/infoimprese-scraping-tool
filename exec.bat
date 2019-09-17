rem For you fucking Windows User

set /P query="What are you looking for? "
set /P where="Where? "
set /P filename="Filename "

IF NOT DEFINED sleep SET "sleep=1"
IF NOT DEFINED filename SET "filename=1"

python main.py -q %query% -l %where% -o risultati/%filename%.csv