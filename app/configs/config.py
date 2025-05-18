from dotenv import dotenv_values

env_variables = dotenv_values(".env")

db_protocol = env_variables.get('db_protocol', '')
db_diletics = env_variables.get('db_diletics', '')
db_username = env_variables.get('db_username', '')
db_password = env_variables.get('db_password', '')
db_url = env_variables.get('db_url', '')
db_port = env_variables.get('db_port', 0000)
db_name = env_variables.get('db_name', '')
email_host = env_variables.get('email_host', '')
email_port = env_variables.get('email_port', 000)
email_admin = env_variables.get('email_admin', '')
email_pass = env_variables.get('email_pass', '')