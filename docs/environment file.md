If you run the application with python (no docker) I have NOT provided the .env file needed by pydantic to 
create base configuration. 

follow this passage:

- create a file called ".env" in the root folder
- copy and paste the below code as is
- run the app as described in [Get Started](getting%20started.md)

*you can change all of this values but `ALGORITHM=HS256` since the hashing logic expect this*  

*`ACCESS_TOKEN_EXPIRE_MINUTES` is the minute life of a token (used to verify user login status)*  

---
`DATABASE_NAME=todo-db` 
`SECRET_KEY=as3f85d7asSDFWD234vffghb$d56ew2brfbe45er535vBGTY354vfgBTy`
`ALGORITHM=HS256`  
`ACCESS_TOKEN_EXPIRE_MINUTES=300`

---