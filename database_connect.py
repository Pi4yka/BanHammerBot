import psycopg2


def get_values(url):
    conn = psycopg2.connect(url, sslmode='require')

    select = conn.cursor()
    select.execute('SELECT category_id, TRIM(word) FROM ban_word')
    ban_words = select.fetchall()

    select.close()
    conn.close()
    return ban_words


def found_word(url, ban_words, category_id, user_id):
    conn = conn = psycopg2.connect(url, sslmode='require')

    select = conn.cursor()
    select.execute('SELECT user_id, counter, category_id FROM warning_user_counter WHERE user_id = %s AND category_id = %s', (str(user_id), str(category_id)))
    user_warn = select.fetchall()
    select.close()
    
    if not user_warn:
        select = conn.cursor()
        select.execute('INSERT INTO warning_user_counter(user_id, counter, category_id) VALUES(%s, 1, %s)', (user_id, category_id))
        conn.commit()
        select.close()
        conn.close()
        return 0
    else:
        select = conn.cursor()
        select.execute('SELECT max_available_warnings FROM ban_words_category WHERE category_id = %s', str(ban_words[0][0]))
        max_available_warnings = select.fetchone()
        select.close()
        if user_warn[0][1] < max_available_warnings[0]:
            select = conn.cursor()
            select.execute('UPDATE warning_user_counter SET counter = %s WHERE user_id = %s', (str(user_warn[0][1] + 1), user_id))
            conn.commit()
            select.close()
            conn.close()
            return 0
        else:
            return 1
