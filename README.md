# tickets
tickets

### How to setup ->
python3 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt

### How to run the service ->
uvicorn main:app --reload 


### How to run the service -> 
http://127.0.0.1:8000/tickets


User
	/register
    /token

Ticket
	/list
	/get
	/create
	/update
	/delete
	
