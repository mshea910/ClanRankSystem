import Rank_Data as rd

race = 1
player_date_joined = []
player_name_compare = []
player_name = []
player_total_lvl = []
player_rank_current = []

# Data Retrieval Functions
rd.name_and_level(race, player_name, player_total_lvl)
rd.date_joined(race, player_date_joined, player_name_compare)
rd.get_rank(race, player_rank_current)

# Data Manipulation Functions
player_date_joined, player_rank_current = rd.combine_and_reorganize(player_name_compare, player_rank_current, player_date_joined, player_name)
player_rank_recommend = rd.rank_changes(player_name, player_total_lvl, player_rank_current)

# Final Data Printing Function
rd.print_to_file(player_name, player_total_lvl, player_date_joined, player_rank_current, player_rank_recommend)
