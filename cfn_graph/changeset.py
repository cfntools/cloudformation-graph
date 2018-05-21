from graphviz import Digraph

from .exceptions import UnknownChangeTypeException, UnknownChangeSourceException, UnknownTargetAttributeException


class ChangeSetGraph(object):
    action_colors = {
        'Add': 'green',
        'Modify': 'orange',
        'Remove': 'red',
    }
    replacement_colors = {
        None: 'grey',
        'False': 'green',
        'Conditional': 'orange',
        'True': 'red',
    }
    node_shape = 'box'
    node_style = 'filled'

    evaluation_style = {
        'Static': 'solid',
        'Dynamic': 'dashed',
    }

    requires_recreation_color = {
        'Never': 'green',
        'Conditionally': 'orange',
        'Always': 'red',
    }

    def __init__(self, input_dict: dict, include_type=False, include_id=False):
        self.changes = input_dict['Changes']
        self.include_type = include_type
        self.include_id = include_id
        self._graph = Digraph()

    def graph(self) -> Digraph:
        for change in self.changes:
            if change['Type'] == 'Resource':
                self._resource_change(change['ResourceChange'])
            else:
                raise UnknownChangeTypeException
        return self._graph

    def _resource_change(self, change: dict) -> None:
        name = change['LogicalResourceId']

        label_elements = [name]
        if self.include_type:
            label_elements.append(change['ResourceType'])
        if self.include_id:
            x = change.get('PhysicalResourceId')  # can be none or not present on Add
            if x:
                label_elements.append(x)

        attributes = {
            'fillcolor': self.action_colors[change['Action']],
            'color': self.replacement_colors[change.get('Replacement')],
            'shape': self.node_shape,
            'style': self.node_style,
            'label': '\n'.join(label_elements)
        }

        self._graph.node(name, **attributes)
        for detail in change.get('Details', []):  # only on Modify
            self._resource_change_detail(detail, name)

    def _resource_change_detail(self, detail: dict, node_name: str) -> None:
        # Target, CausingEntity

        change_source = detail['ChangeSource']
        target = detail['Target']

        if change_source == 'ResourceReference':
            from_node = detail['CausingEntity']
            from_label = ''
        elif change_source == 'ParameterReference':
            from_node = detail['CausingEntity']
            from_label = ''
        elif change_source == 'ResourceAttribute':
            from_node = detail['CausingEntity'].split('.')[0]
            from_label = detail['CausingEntity'].split('.')[1]
        elif change_source == 'DirectModification':
            from_node = '__Direct__'
            from_label = ''
        elif change_source == 'Automatic':  # nested stacks
            from_node = detail['CausingEntity']
            from_label = '__Automatic__'
        else:
            raise UnknownChangeSourceException()

        if target['Attribute'] == 'Properties':
            to_label = target['Name']
        elif target['Attribute'] == 'Metadata':
            to_label = '_Metadata_'
        elif target['Attribute'] == 'Tags':
            to_label = '_Tags_'
        else:
            raise UnknownTargetAttributeException()

        attrbutes = {
            'style': self.evaluation_style[detail['Evaluation']],
            'color': self.requires_recreation_color[target['RequiresRecreation']],
            'taillabel': from_label,
            'headlabel': to_label,
        }

        self._graph.edge(from_node, node_name, **attrbutes)
