DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS token;
DROP TABLE IF EXISTS website;
DROP TABLE IF EXISTS annotation;
DROP TABLE IF EXISTS comment;

CREATE TABLE user (
	user_id VARCHAR NOT NULL, 
	username VARCHAR NOT NULL, 
	password VARCHAR NOT NULL, 
	email_id VARCHAR NOT NULL, 
	bio VARCHAR, 
	authority VARCHAR NOT NULL, 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP), 
	modified_at DATETIME, 
	upvotes VARCHAR, 
	downvotes VARCHAR, 
	PRIMARY KEY (user_id), 
	UNIQUE (email_id), 
	UNIQUE (password), 
	UNIQUE (user_id), 
	UNIQUE (username)
);

CREATE TABLE token (
	user_id VARCHAR NOT NULL, 
	api_key VARCHAR NOT NULL, 
	PRIMARY KEY (user_id), 
	UNIQUE (api_key), 
	UNIQUE (user_id)
);

CREATE TABLE website (
	website_id VARCHAR NOT NULL, 
	website_url VARCHAR NOT NULL, 
	n_annotations INTEGER, 
	annotation_limit INTEGER, 
	admin VARCHAR NOT NULL, 
	admin_type VARCHAR NOT NULL, 
	PRIMARY KEY (website_id), 
	UNIQUE (admin), 
	UNIQUE (website_id)
);

CREATE TABLE annotation (
	annotation_id VARCHAR NOT NULL, 
	annotation_name VARCHAR NOT NULL, 
	website_id VARCHAR NOT NULL, 
	website_uri VARCHAR NOT NULL, 
	node_xpath VARCHAR NOT NULL, 
	html_id VARCHAR, 
	html_tag VARCHAR, 
	html_text_content VARCHAR, 
	tags VARCHAR, 
	resolved BOOLEAN, 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP), 
	updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP), 
	created_by_id VARCHAR, 
	created_by VARCHAR NOT NULL, 
	modified_by_id VARCHAR, 
	modified_by VARCHAR, 
	PRIMARY KEY (annotation_id), 
	FOREIGN KEY(created_by_id) REFERENCES user (user_id), 
	FOREIGN KEY(modified_by_id) REFERENCES user (user_id), 
	UNIQUE (annotation_id)
);

CREATE TABLE comment (
	comment_id VARCHAR NOT NULL, 
	annotation_id VARCHAR NOT NULL, 
	content VARCHAR NOT NULL, 
	content_html VARCHAR, 
	parent_node VARCHAR, 
	upvotes INTEGER, 
	downvotes INTEGER, 
	mod_required BOOLEAN, 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP), 
	updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP), 
	created_by_id VARCHAR, 
	created_by VARCHAR NOT NULL, 
	PRIMARY KEY (comment_id), 
	FOREIGN KEY(annotation_id) REFERENCES annotation (annotation_id), 
	FOREIGN KEY(created_by_id) REFERENCES user (user_id), 
	UNIQUE (comment_id)
);