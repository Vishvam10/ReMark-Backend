INSERT INTO user (
  user_id, 
	username, 
	password, 
	email_id, 
	authority, 
	bio,
	created_at, 
	modified_at, 
	upvotes,
	downvotes
)
VALUES (
  "4fa8e53790154685b993fe90eeasf209", 
  "testing_admin", "$2b$12$DBhImT3w9IzhMRbh6aYVOe234dFPTGCi17iIfWp8a27GJNsFRhbu",
  "testadmin@gmail.com", 
  "admin", 
  "test_bio",
  "2018-01-01 00:00:00",
  "2018-01-01 00:00:00",
  "none",
  "none"
);

INSERT INTO token (
  user_id, 
  api_key
)
VALUES (
  "4fa8e53790154685b993fe90eeasf209",
  "Vgtl_3-aChp6Clil1vGYObrNvHmRRZts_xOan13dfg4"
);