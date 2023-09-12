# DND Character Tracker - No UI 

Thought: I'm DMing a campaign and want easy access to basic character info I can update after bi-weekly sessions. 

This API is being developed in an effort to practice creating an API with various functionalities. 

SQLite3 is used as the database. 

Current: 9/12/2023
  - Endpoints creating, reading, and updating characters. These are available to all          users. 

Goals: 
  - Add authentification.
      - Allow users to read.
      - Allow admins to create, update, delete.
  - Store users (players) who are linked to their characters.
      - Allow viewing of characters played by the user by all users by querying users name
      - Allow list of all users to be viewed by users
      - Give admins CRUD privileges over 'users' data 
