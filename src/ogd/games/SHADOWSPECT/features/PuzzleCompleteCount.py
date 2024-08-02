#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from typing import Any, List
import json
import pandas as pd
import numpy as np
import json
import hashlib
from datetime import datetime
from datetime import timedelta
from collections import OrderedDict
# import locals
from ogd.core.generators.Generator import GeneratorParameters
from ogd.core.generators.extractors.SessionFeature import SessionFeature
from ogd.core.models.FeatureData import FeatureData
from ogd.core.models.Event import Event
from ogd.core.models.enums.ExtractionMode import ExtractionMode

class PuzzleCompleteCount(Feature):
    def __init__(self, params: GeneratorParameters, additional_param=None):
        super().__init__(params)
        
        self._additional_param = additional_param
        
        self._completed_count = 0

    @classmethod
    def _eventFilter(cls, mode: ExtractionMode) -> List[str]:
        return ["puzzle_completed"]

    @classmethod
    def _featureFilter(cls, mode: ExtractionMode) -> List[str]:
        return []

    def _updateFromEvent(self, event: Event):
        if event.type == "puzzle_completed":
            self._completed_count += 1

    def _updateFromFeatureData(self, feature: FeatureData):
        # As this is a first-order feature, this method should not do anything
        return

    def _getFeatureValues(self) -> List[int]:
        return [self._completed_count]

