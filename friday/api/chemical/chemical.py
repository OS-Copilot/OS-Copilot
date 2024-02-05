import random

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Union
from .chemical_prop_api import ChemicalPropAPI

router = APIRouter()


class GetNameResponse(BaseModel):
    """name list"""
    names: List[str]


class GetStructureResponse(BaseModel):
    """structure list"""
    state: int
    content: Optional[str] = None


class GetIDResponse(BaseModel):
    state: int
    content: Union[str, List[str]]


chemical_prop_api = ChemicalPropAPI


@router.get("/tools/chemical/get_name", response_model=GetNameResponse)
def get_name(cid: str):
    """prints the possible 3 synonyms of the queried compound ID"""
    ans = chemical_prop_api.get_name_by_cid(cid, top_k=3)
    return {
        "names": ans
    }


@router.get("/tools/chemical/get_allname", response_model=GetNameResponse)
def get_allname(cid: str):
    """prints all the possible synonyms (might be too many, use this function carefully).
    """
    ans = chemical_prop_api.get_name_by_cid(cid)
    return {
        "names": ans
    }


@router.get("/tools/chemical/get_id_by_struct", response_model=GetIDResponse)
def get_id_by_struct(smiles: str):
    """prints the ID of the queried compound SMILES. This should only be used if smiles is provided or retrieved in the previous step. The input should not be a string, but a SMILES formula.
    """
    cids = chemical_prop_api.get_cid_by_struct(smiles)
    if len(cids) == 0:
        return {
            "state": "no result"
        }
    else:
        return {
            "state": "matched",
            "content": cids[0]
        }


@router.get("/tools/chemical/get_id", response_model=GetIDResponse)
def get_id(name: str):
    """prints the ID of the queried compound name, and prints the possible 5 names if the queried name can not been precisely matched,
    """
    cids = chemical_prop_api.get_cid_by_name(name)
    if len(cids) > 0:
        return {
            "state": "precise",
            "content": cids[0]
        }

    cids = chemical_prop_api.get_cid_by_name(name, name_type="word")
    if len(cids) > 0:
        if name in get_name(cids[0]):
            return {
                "state": "precise",
                "content": cids[0]
            }

    ans = []
    random.shuffle(cids)
    for cid in cids[:5]:
        nms = get_name(cid)
        ans.append(nms)
    return {
        "state": "not precise",
        "content": ans
    }


@router.get("/tools/chemical/get_prop")
def get_prop(cid: str):
    """prints the properties of the queried compound ID
    """
    return chemical_prop_api.get_prop_by_cid(cid)
