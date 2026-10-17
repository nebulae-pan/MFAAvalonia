from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context
import json
from typing import Dict, Any
from pathlib import Path
import time

from utils import Utils


@AgentServer.custom_recognition("memory_storm_progress_reco")
class MemoryStormProgressRecongition(CustomRecognition):

    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:

        reco_detail = context.run_recognition(
            "RecoORC",
            argv.image,
            {
                "RecoORC": {
                    "recognition": "OCR",
                    "expected": "全局高额次数",
                    "roi": [0, 0, 0, 0]
                }
            }
        )

        if reco_detail is None:
            return None
        
        text = reco_detail.best_result.text
        print(text)
        times = int(reco_detail.best_result.text.split("：")[1].strip().split("/")[0])
        print(f"全局高额次数: {times}")
        if times == 0:
            return None
        else:
            return CustomRecognition.AnalyzeResult(
                box=reco_detail.best_result.box, detail="found result"
            )