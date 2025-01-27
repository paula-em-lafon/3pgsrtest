## Test app for new Sr Python position
# to start 
1. clone the repo
2. do a `docker-compose buld`
3. `docker-compose up`
4. in a separate terminal do `docker exec -it backend /bin/bash`
5. inside the container do `python databaseCreate.py`
6. step out of the container using `ctrl-D`
7. outside the container run `curl -X POST http://0.0.0.0:8000/initdb`
8. go to `http://localhost:3000` in your browser

# to test
1. in a terminal do `docker exec -it backend /bin/bash`
2. run `pytest`, tests for backend should run
3.  in a terminal do `docker exec -it frontend /bin/bash`
4. run `npm test` (unfortunately I ran into a lot of trouble with this one :/
