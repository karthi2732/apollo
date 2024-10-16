
from . import DatabaseSession
from .entities import GStk, GStkDayStat


def get_stk_by_id(search_id):
    """
    get stk data of given search_id
    """

    with DatabaseSession() as session:
        return session.query(GStk).filter(GStk.search_id == search_id).all()
    

def get_all_stks(offset, limit):

    with DatabaseSession() as session:
        return session.query(GStk).offset(offset).limit(limit).all()

def get_stk_by_exchange_and_code(exchange, code):
    """
    get stk data of given exchange and exchange_code
    """

    with DatabaseSession() as session:
        return session.query(GStk).filter_by(exchange=exchange, code=code).all()


def get_stk_by_ids(search_ids):
    """
    get stk data of given list of search_ids
    """

    with DatabaseSession() as session:
        return session.query(GStk).filter(GStk.search_id.in_(search_ids)).all()
    

def get_stk_stats_by_ids(search_ids):
    """
    get stk data of given list of search_ids
    """

    with DatabaseSession() as session:
        return session.query(GStkDayStat).filter(GStkDayStat.search_id.in_(search_ids)).all()
    

def get_stk_table_size():
    """
    get stk data of given list of search_ids
    """

    with DatabaseSession() as session:
        return session.query(GStk).count()
    

def delete_all_stk_by_ids(search_ids):
    """
    delete all stk data of given list of search_ids
    """

    with DatabaseSession() as session:
        return session.query(GStk).filter(GStk.search_id.in_(search_ids)).delete()
    

def delete_all_stk_day_stat():
    """
    delete stk day stat data
    """

    with DatabaseSession() as session:
        return session.query(GStkDayStat).filter(GStkDayStat.search_id is not None).delete()


def save_stks(stks):
    """
    saves the list of stks in db
    """

    with DatabaseSession() as session:

        session.bulk_save_objects(stks)
        session.flush()
        session.commit()


def save_stk_stats(stk_stats):
    """
    saves the list of stk stats in db
    """

    with DatabaseSession() as session:

        session.bulk_save_objects(stk_stats)
        session.flush()
        session.commit()


