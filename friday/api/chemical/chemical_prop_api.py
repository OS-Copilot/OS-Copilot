import json
from typing import Optional, List

import requests
from bs4 import BeautifulSoup


class ChemicalPropAPI:
    def __init__(self) -> None:
        self._endpoint = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"

    def get_name_by_cid(self, cid: str, top_k: Optional[int] = None) -> List[str]:
        html_doc = requests.get(f"{self._endpoint}cid/{cid}/synonyms/XML").text
        soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
        syns = soup.find_all('synonym')
        ans = []
        if top_k is None:
            top_k = len(syns)
        for syn in syns[:top_k]:
            ans.append(syn.text)
        return ans

    def get_cid_by_struct(self, smiles: str) -> List[str]:
        html_doc = requests.get(f"{self._endpoint}smiles/{smiles}/cids/XML").text
        soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
        cids = soup.find_all('cid')
        if cids is None:
            return []
        ans = []
        for cid in cids:
            ans.append(cid.text)
        return ans

    def get_cid_by_name(self, name: str, name_type: Optional[str] = None) -> List[str]:
        url = f"{self._endpoint}name/{name}/cids/XML"
        if name_type is not None:
            url += f"?name_type={name_type}"
        html_doc = requests.get(url).text
        soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
        cids = soup.find_all('cid')
        if cids is None:
            return []
        ans = []
        for cid in cids:
            ans.append(cid.text)
        return ans

    def get_prop_by_cid(self, cid: str) -> str:
        html_doc = requests.get(
            f"{self._endpoint}cid/{cid}/property/MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES,IUPACName,XLogP,ExactMass,MonoisotopicMass,TPSA,Complexity,Charge,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,HeavyAtomCount,CovalentUnitCount/json").text
        return json.loads(html_doc)['PropertyTable']['Properties'][0]