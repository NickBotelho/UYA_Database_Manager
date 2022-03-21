from blarg.packets.tcp import *


tcp_map = {
    '0213': tcp_0213_headset_check.tcp_0213_headset_check(),
    '0003': tcp_0003_broadcast_lobby_state.tcp_0003_broadcast_lobby_state(),
    '0211': tcp_0211_player_lobby_state_change.tcp_0211_player_lobby_state_change(),
    '0018': tcp_0018_initial_sync.tcp_0018_initial_sync(),
    '020C': tcp_020C_in_game_info.tcp_020C_in_game_info(),
    '020A': tcp_020A_player_respawn.tcp_020A_player_respawn(),
    '020B': tcp_020B_map_destruction.tcp_020B_map_destruction(),
    '0210':tcp_0210_player_join.tcp_0210_player_join(),
    '0004':tcp_0004_game_state.tcp_0004_game_state(),
    '0204':tcp_0204_player_killed.tcp_0204_player_killed(),
    '000D':tcp_000D_game_started.tcp_000D_game_started(),
    '0009':tcp_0009_set_timer.tcp_0009_set_timer(),
    '0012':tcp_0012_player_left.tcp_0012_player_left(),
}
