create table ban_words_category
(
    category_id            bigserial not null
        constraint ban_words_category_pkey
            primary key,
    name                   char(64)  not null,
    max_available_warnings integer
);

create table ban_word
(
    ban_word_id bigserial not null
        constraint ban_word_pkey
            primary key,
    word        char(64)  not null,
    category_id bigint    not null
        constraint ban_word_category_id_fkey
            references ban_words_category
);

create unique index ban_word_word_uindex
    on ban_word (word);

create table warning_user_counter
(
    user_id     bigint  not null,
    counter     integer not null,
    category_id bigint  not null
        constraint warning_user_counter_category_id_fkey
            references ban_words_category
);