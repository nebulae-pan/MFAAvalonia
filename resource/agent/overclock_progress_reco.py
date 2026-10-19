from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context
import json
from typing import Dict, Any
from pathlib import Path
import time

from utils import Utils

@AgentServer.custom_recognition("overclock_progress_reco")
class OverclockProgressRecongition(CustomRecognition):

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
                    "expected": r'^\d+%$',  # 匹配整数百分比的正则表达式
                    "roi": [485, 182, 327, 352]
                }
            }
        )

        if reco_detail is None:
            return None

        text = reco_detail.best_result.text
        # 移除百分号并转换为整数
        percentage = int(text.rstrip('%'))
        if percentage < 120:
            return CustomRecognition.AnalyzeResult(
                box=reco_detail.best_result.box, detail="found result"
            )
        else:
            return None