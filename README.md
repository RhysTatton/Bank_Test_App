# Bank_Test_App

**How to run:**

- Make sure you run the BankTEST Database.py first to create the basic_bank database
- You will need to create 2 users to be able to use the full function of this app


Currently a work in progress

This is a basic bank app that uses 2 SQL tables to save users information (username and password) and the tranasaction history 

The user can create an account which saves it to the user table in which the passwords are hashed for data protection. The user then will be able to log in and be able to perform 3 actions, check balance, add funds and transfer funds.
Currently the only functions that are finished are the add funds and check balance for the user.

The plan is to be able to call an api to handle thee request for sending and recieving the transaction
