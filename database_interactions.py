import pymysql
import config

class DatabaseExecutor:

    def __init__(self) -> None:
        self.database_host = config.DATABASE_HOST
        self.database_port = config.DATABASE_PORT
        self.database_user = config.DATABASE_USER
        self.database_password = config.DATABASE_PASSWORD
        self.database_name = config.DATABASE_NAME

        self.connection = None

    def create_connection(self):
        
        try:

            self.connection = pymysql.connect(
                host = self.database_host,
                port = self.database_port,
                user = self.database_user,
                password = self.database_password,
                database = self.database_name,
                cursorclass=pymysql.cursors.DictCursor
            )

            print(self.connection.open)

            

        except Exception as ex:
            print(f"[FAILURE] Connection refused: {ex}")

    def close_connection(self):
        if self.connection.open: self.connection.close()

    def create_tables(self):
        
        

        if not self.connection.open: return -1

        with self.connection.cursor() as cursor:

            query_create_variables_table = "CREATE TABLE `variables` (`variable_name` varchar(100) NOT NULL, `variable_value` varchar(1000) NOT NULL,PRIMARY KEY (`variable_name`))"
            query_create_mechanics_chat_table = "CREATE TABLE `mechanics-chat` (`message-date` date NOT NULL,`message-content` varchar(1000) NOT NULL, PRIMARY KEY(`message-date`))"
            cursor.execute(query_create_variables_table)
            cursor.execute(query_create_mechanics_chat_table)
            self.connection.commit()

            

    def get_today_message(self, date):
        
        if not self.connection.open: return -1

        with self.connection.cursor() as cursor:

            query = f'SELECT * FROM `mechanics-chat` WHERE `message-date` = "{date}";'
            cursor.execute(query)
            today_message = cursor.fetchone()

            return today_message
        
    def change_message_content_by_date(self, date, new_content):

        if not self.connection.open: return -1

        with self.connection.cursor() as cursor:

            query = f'REPLACE INTO `mechanics-chat` (`message-date`, `message-content`) VALUES ("{date}", "{new_content}")'
            cursor.execute(query)
            self.connection.commit()

    def set_group_id_to_message(self, group_id):

        if not self.connection.open: return -1
    
        with self.connection.cursor() as cursor:

            query = f'REPLACE INTO `variables` (`variable_name`, `variable_value`) VALUES ("group_id", "{group_id}")'
            cursor.execute(query)
            self.connection.commit()

    def get_group_id(self):
        if not self.connection.open: return -1

        with self.connection.cursor() as cursor:

            query = f'SELECT * FROM `variables` WHERE `variable_name` = "group_id";'
            cursor.execute(query)
            group_id = cursor.fetchone()
            
            return group_id