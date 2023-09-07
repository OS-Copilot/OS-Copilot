from typing import Optional, Union, Dict, Hashable


class PromptTemplate:
    def __init__(self,
                 template: Union[Dict, str],
                 column_token_map: Dict,
                 selected_column_name: Optional[str] = None,
                 ice_token: Optional[str] = None,
                 ) -> None:
        self.template = template
        self.column_token_map = column_token_map
        self.selected_column_name = selected_column_name
        self.ice_token = ice_token

    def generate_item(self, entry: Dict, output_field: Optional[Hashable] = None,
                      output_field_replace_token: Optional[str] = '',
                      ice_field_replace_token: Optional[str] = '') -> str:

        if isinstance(self.template, str):
            tp = self.template
        else:
            pred_label = None
            if self.selected_column_name is not None:
                pred_label = entry[self.selected_column_name]
            if pred_label in self.template.keys():
                tp = self.template[pred_label]
            else:
                tp = self.template[list(self.template.keys())[0]]

        if self.ice_token is not None:
            tp = tp.replace(self.ice_token, ice_field_replace_token)

        for key, token in self.column_token_map.items():
            if output_field is not None and key == output_field:
                tp = tp.replace(token, output_field_replace_token)
            else:
                tp = tp.replace(token, str(entry[key]))
        return tp