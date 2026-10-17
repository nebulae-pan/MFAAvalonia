import sys

from maa.agent.agent_server import AgentServer
from maa.toolkit import Toolkit

import mecha_supply_reco
import ash_mission_progress_reco
import memory_storm_progress_reco
import daily_tasks_reco
import combine_tasks_reco
import warehouse_reco
import swipe_to_end_reco
import overclock_progress_reco

def main():
    Toolkit.init_option("./maa_option.json")

    socket_id = sys.argv[-1]
    
    AgentServer.start_up(socket_id)
    AgentServer.join()
    AgentServer.shut_down()


if __name__ == "__main__":
    main()
