import sys
import json

from graphviz import Digraph


def parse_specfile(path):
    with open(path) as f:
        data = json.load(f)
    return data


def record_relations(data):
    record_relations = [
        (i['name'],
         i['parent_record'] if i['parent_record'] else 'root'
         ) for i in data]
    return record_relations


def intra_record_relations(data):
    results = []
    unique_record_names = {record['name'] for record in data}
    for record in data:
        fields = record['fields']
        for field in fields:
            for external_record in unique_record_names:
                description = field['description'] or ''
                if external_record in description and record['name'] != external_record:
                    results.append((record['name'], external_record, field['name']))
    return results


def main(specfile_path, focus):
    graph = Digraph(format='svg')
    graph.attr(kw='graph',
               rankdir='LR',
               splines='true',
               sep='1',)
    data = parse_specfile(specfile_path)
    for child, parent in record_relations(data):

        if focus:
            if focus not in (child, parent):
                continue

        graph.node(child)
        graph.node(parent)
        graph.edge(parent, child)

    for target, origin, label in intra_record_relations(data):
        if focus:
            if focus not in (target, origin):
                continue
        graph.edge(origin, target, label=label, color='red', fontcolor='red',)

    graph.render('graph')


if __name__ == '__main__':
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument('-f', '--focus')
    argparser.add_argument('-s', '--specfile', required=True)

    args = argparser.parse_args()

    main(args.specfile, args.focus)
