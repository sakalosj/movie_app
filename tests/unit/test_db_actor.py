from contextlib import nullcontext as does_not_raise
from operator import itemgetter

import pytest
from sqlalchemy.exc import IntegrityError

from db import ActorModel

user_data_list = [
    ('jozko', 'mrkvicka', 'l1'),
    ('jozko2', 'mrkvicka2', 'l1'),
    ('jozko', 'mrkvicka3', 'l3'),
    ('jozko4', 'mrkvicka', 'l4'),
    ('jozko5', '', 'l5'),
    ('jozko6', None, 'l6'),
    ('', 'mrkvicka7', 'l7'),
    (None, 'mrkvicka8', 'l8'),
    ('jozko', 'mrkvicka', 'l9'),
    ('jozko10', 'mrkvicka10', ''),
    ('jozko11', 'mrkvicka11', None),
]


@pytest.mark.parametrize('users_data, exc',
                         [
                             pytest.param([user_data_list[0]], does_not_raise(), id='ok-add-one'),
                             pytest.param(itemgetter(0, 2)(user_data_list), does_not_raise(), id='ok_same_first'),
                             pytest.param(itemgetter(0, 3)(user_data_list), does_not_raise(), id='ok_same_second'),
                             pytest.param(itemgetter(0, 8)(user_data_list), does_not_raise(), id='ok_same_first_second'),
                             pytest.param([user_data_list[4]], does_not_raise(), id='ok_second_empty'),
                             pytest.param([user_data_list[5]], does_not_raise(), id='ok_second_None'),
                             pytest.param([user_data_list[6]], does_not_raise(), id='ok_first_empty'),
                             pytest.param([user_data_list[7]], does_not_raise(), id='ok_first_None'),
                             pytest.param([user_data_list[9]], does_not_raise(), id='link_empty'),
                             pytest.param([user_data_list[10]], pytest.raises(IntegrityError), id='link_none'),
                             pytest.param(itemgetter(0, 1)(user_data_list), pytest.raises(IntegrityError),
                                          id='err_same_link'),
                             pytest.param([user_data_list[1]] * 2, pytest.raises(IntegrityError), id='err_same_items'),
                         ]
                         )
def test_add(init_db, sa_session, users_data, exc):
    with exc:
        with sa_session() as s:
            s.add_all([ActorModel(first_name=i[0], last_name=i[1], link=i[2]) for i in users_data])
            s.commit()
