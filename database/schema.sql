CREATE TABLE IF NOT EXISTS `blacklist` (
  `user_id` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `warns` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `moderator_id` varchar(20) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS 'students' (
  'pk' INTEGER PRIMARY KEY AUTOINCREMENT,
  'id' int(9) NOT NULL UNIQUE,
  'gender' varchar NOT NULL,
  'full_name' varchar NOT NULL,
  'english_name' varchar NOT NULL,
  'email' varchar NOT NULL,
  'phone' varchar NOT NULL,
  'address' varchar NOT NULL,
  'threads' int array[] NOT NULL DEFAULT [],
  'birthday' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS 'scoreboards' (
  'user_id' varchar(20) NOT NULL,
  'game' int NOT NULL,
  'score' varchar NOT NULL,
  PRIMARY KEY (user_id, game)
)