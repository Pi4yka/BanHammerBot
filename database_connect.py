import psycopg2

default_counter_value = 1
pos_num_in_user_tuple = 0
pos_num_in_user_list = 1
pos_num_in_user_warn = 0
pos_num_in_word_list = 0
pos_num_in_word_tuple = 0

#подключение к базе данных
def connect_to_database(url):
    conn = psycopg2.connect(url, sslmode='require')
    return conn

#подключение к базе данных и получение списка запрещенных слов и их категорий
def get_values(url):
    conn = connect_to_database(url)

    select = conn.cursor()
    select.execute('SELECT category_id, TRIM(word) FROM ban_word')
    received_word_list = select.fetchall()

    select.close()
    conn.close()
    return received_word_list

#подключение к базе данных и получение информации о нарушении пользователем
def get_user_data(url, category_id, user_id):
    conn = connect_to_database(url)

    select = conn.cursor()
    select.execute('SELECT user_id, counter, category_id FROM warning_user_counter WHERE user_id = %s AND category_id = %s', 
                        (str(user_id), str(category_id)))
    user_data = select.fetchall()

    select.close()
    conn.close()
    return user_data

#подключение к базе данных и добавление пользователя в таблицу нарушителей
def add_user_data_counter(url, user_id, category_id):
    conn = connect_to_database(url)

    select = conn.cursor()
    select.execute('INSERT INTO warning_user_counter(user_id, counter, category_id) VALUES(%s, %s, %s)', 
        (user_id, default_counter_value, category_id))
    conn.commit()

    select.close()
    conn.close()

#подключение к базе данных и получение данных о запрещенных словах 
def get_available_warnings(url, category_id):
    conn = connect_to_database(url)

    select = conn.cursor()
    select.execute('SELECT max_available_warnings FROM ban_words_category WHERE category_id = %s', str(category_id))
    max_available_warnings = select.fetchone()

    select.close()
    conn.close()
    return max_available_warnings

#подключение к базе данных и обновлении данных счетчика
def increase_user_counter(url, user_id, user_data, category_id):
    conn = connect_to_database(url)

    select = conn.cursor()
    select.execute('UPDATE warning_user_counter SET counter = %s WHERE user_id = %s AND category_id = %s', 
        (str(user_data[pos_num_in_user_tuple][pos_num_in_user_list] + default_counter_value), user_id, category_id))
    conn.commit()

    select.close()
    conn.close()

#инициализация получения данных и взаимодействия с базой для добавления/обновления данных
def found_word(url, category_id, user_id):
    user_data = get_user_data(url, category_id, user_id)
    if not user_data:
        add_user_data_counter(url,user_id, category_id)
        return 0
    else:
        max_available_warnings = get_available_warnings(url, category_id)
        if user_data[pos_num_in_user_tuple][pos_num_in_user_list] < max_available_warnings[pos_num_in_user_warn]:
            increase_user_counter(url, user_id, user_data, category_id)
            return 0
        else:
            return 1
