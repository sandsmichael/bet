import sys,os
from providers.atp.rankings import Rankings 

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def collect_player_ids():
    """[extract atp player ids from top player rankings and write to csv]

    :param [url]:
    ...
    :return: [None]
    :rtype: []
    """
    ranks = Rankings()
    player_links = ranks.get_top_players_links(n=None)
    ids = ranks.extract_player_id_from_url(links = player_links)
    fp_player_ids = os.path.join(basedir, 'vanilla/io/out/atp_player_ids.csv')
    ids.to_csv(fp_player_ids, index=False)
    print('[SUCCESS] ATP player IDs written to {}'.format(fp_player_ids))






# collect_player_ids()