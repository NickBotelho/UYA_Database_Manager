from blarg.packets.udp import *

udp_map = {
    '0209': udp_0209_movement_update.udp_0209_movement_update(),
    '020E': udp_020E_player_firing.udp_020E_player_firing(),
    '0200': udp_0200_player_death.udp_0200_player_death(),
    '020F': udp_020F_damaging.udp_020F_damaging(),
    '0001':udp_0001_timer_update.udp_0001_timer_update(),
}
