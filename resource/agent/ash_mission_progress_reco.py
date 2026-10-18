from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context
import json
from typing import Dict, Any
from pathlib import Path
import time

from utils import Utils


@AgentServer.custom_recognition("ash_mission_progress_reco")
class AshMissionProgressRecongition(CustomRecognition):

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
                    "expected": "^今日联络进度.*$",
                    "roi": [0, 0, 0, 0]
                }
            }
        )
        if reco_detail == None:
            print("not found '今日联络进度'")
            return CustomRecognition.AnalyzeResult(
                box=[0, 0, 1, 1], detail="7"
            )

        text = reco_detail.best_result.text
        print(text)
        #  text='今日联络进度：980' or text='今日联络进度已达上限'
        if text == "今日联络进度：":
            return CustomRecognition.AnalyzeResult(
                box=reco_detail.best_result.box, detail="7"
            )
        if text == "今日联络进度已达上限":
            return None
        progress = int(text.split("：")[1].strip())
        if progress > 900:
            print("progress > 900, skip receive reward...")
            return None
        else:
            return CustomRecognition.AnalyzeResult(
                box=reco_detail.best_result.box, detail="7"
            )