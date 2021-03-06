#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author: Jiang Shanshan
Email: univeroner@gmail.com
Date: 2021/1/15

"""

from fastapi import APIRouter
from modelci.persistence.service import ModelService
from modelci.types.bo.model_objects import Engine
from torchviz import make_dot
import torch

router = APIRouter()


@router.get('/{id}')
def generate_model_graph(*, id: str):  # noqa
    model_bo = ModelService.get_model_by_id(id)
    dot_graph = ''
    if model_bo.engine == Engine.PYTORCH:
        pytorch_model = torch.load(model_bo.saved_path)
        sample_data = torch.zeros(1, *model_bo.inputs[0].shape[1:], dtype=torch.float, requires_grad=False)
        out = pytorch_model(sample_data)
        dot_graph = make_dot(out, params=dict(list(pytorch_model.named_parameters()) + [('x', sample_data)]))

    return {'dot': str(dot_graph)}
