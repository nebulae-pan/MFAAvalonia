from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context
from maa.define import RecognitionDetail
import json
from typing import Dict, Any
from pathlib import Path
import time
from datetime import datetime

from utils import Utils

"""
usually used for interrupt tasks, resolve the endless loop problem
"""
@AgentServer.custom_recognition("combine_tasks_reco")
class CombineTasksRecongition(CustomRecognition):
    task_nodes = Utils.load_project_nodes()

    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        nexts = self.task_nodes[argv.node_name]['next']
        for next in nexts:
            if not self.reco_all_next_tasks(context, next, argv):
                return CustomRecognition.AnalyzeResult(
                    box=[0, 0, 1, 1], detail="combine_tasks_reco"
                )
        return None

    def reco_all_next_tasks(self, context: Context, entry: str, argv: CustomRecognition.AnalyzeArg) -> bool:
        reco_detail = context.run_recognition(
            entry,
            argv.image
        )
        return reco_detail == None
