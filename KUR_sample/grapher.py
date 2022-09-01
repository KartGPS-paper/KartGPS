import json

import numpy as np
from rdflib import Graph,URIRef

class grapher(object):
    def __init__(self, dataset_dir):
        """
        Preprocess the dataset. add corresponding inverse quadruples to the data.
        :param dataset_dir: path to the graph dataset directory
        """
        self.dataset_dir = dataset_dir
        self.entity2id = json.load(open(dataset_dir + "entity2id.json"))
        self.relation2id_old = json.load(open(dataset_dir + "relation2id.json"))
        self.relation2id = self.relation2id_old.copy()
        counter = len(self.relation2id_old)
        for relation in self.relation2id_old:
            self.relation2id["_" + relation] = counter  # Inverse relation
            counter += 1
        self.ts2id = json.load(open(dataset_dir + "ts2id.json"))
        self.id2entity = dict([(v, k) for k, v in self.entity2id.items()])
        self.id2relation = dict([(v, k) for k, v in self.relation2id.items()])
        self.id2ts = dict([(v, k) for k, v in self.ts2id.items()])

        self.inv_relation_id = dict()
        num_relations = len(self.relation2id_old)
        for i in range(num_relations):
            self.inv_relation_id[i] = i + num_relations
        for i in range(num_relations, num_relations * 2):
            self.inv_relation_id[i] = i % num_relations

        self.train_idx = self.create_store("train.txt")
        self.train_g = self.create_rdf(self.train_idx)
        self.valid_idx = self.create_store("valid.txt")
        self.valid_g = self.create_rdf(self.valid_idx)
        self.test_idx = self.create_store("test.txt")
        self.test_g = self.create_rdf(self.test_idx)
        self.all_idx = np.vstack((self.train_idx, self.valid_idx, self.test_idx))

        print("Grapher initialized.")

    def preprocess_graph(self):
        """
        preprocess the graph data to build idx

        """

        def update_dict(idxdict, id, token):
            if token not in idxdict:
                idxdict[token] = id
                id += 1
            return idxdict, id

        entity2id = {}
        relation2id = {}
        ts2id = {}
        eid = 0
        rid = 0
        tid = 0
        facts = []
        for file in ['train.txt', 'valid.txt', 'test.txt']:
            with open(self.dataset_dir + file, "r", encoding="utf-8") as f:
                quads = f.readlines()
                s, p, o, t = self.split_quads(quads)
                entity2id, eid = update_dict(entity2id, eid, s)
                entity2id, eid = update_dict(entity2id, eid, o)
                relation2id, rid = update_dict(relation2id, rid, p)
                ts2id, tid = update_dict(ts2id, tid, t)
        with open(self.dataset_dir + "entity2id.json","w") as fout:
            json.dump(entity2id,fout)
        with open(self.dataset_dir + "relation2id.json","w") as fout:
            json.dump(entity2id,fout)
        with open(self.dataset_dir + "ts2id.json","w") as fout:
            json.dump(entity2id,fout)

    def create_rdf(self,data):
        g = Graph()
        for x in data:
            g.add((URIRef('http://' + str(x[0])), URIRef('http://rel/' + str(x[1]) + str(x[3])),
                   URIRef('http://' + str(x[2]))))
        return g


    def create_store(self, file):
        """
        Store the quadruples from the file as indices.
        The quadruples in the file should be in the format "subject\trelation\tobject\ttimestamp\n".

        Parameters:
            file (str): file name

        Returns:
            store_idx (np.ndarray): indices of quadruples
        """

        with open(self.dataset_dir + file, "r", encoding="utf-8") as f:
            quads = f.readlines()
        store = self.split_quads(quads)
        store_idx = self.map_to_idx(store)
        store_idx = self.add_inverses(store_idx)

        return store_idx

    def split_quads(self, quads):
        """
        Split quadruples into a list of strings.

        Parameters:
            quads (list): list of quadruples
                          Each quadruple has the form "subject\trelation\tobject\ttimestamp\n".

        Returns:
            split_q (list): list of quadruples
                            Each quadruple has the form [subject, relation, object, timestamp].
        """

        split_q = []
        for quad in quads:
            split_q.append(quad[:-1].split("\t"))

        return split_q

    def map_to_idx(self, quads):
        """
        Map quadruples to their indices.

        Parameters:
            quads (list): list of quadruples
                          Each quadruple has the form [subject, relation, object, timestamp].

        Returns:
            quads (np.ndarray): indices of quadruples
        """

        subs = [self.entity2id[x[0]] for x in quads]
        rels = [self.relation2id[x[1]] for x in quads]
        objs = [self.entity2id[x[2]] for x in quads]
        tss = [self.ts2id[x[3]] for x in quads]
        quads = np.column_stack((subs, rels, objs, tss))

        return quads

    def add_inverses(self, quads_idx):
        """
        Add the inverses of the quadruples as indices.

        Parameters:
            quads_idx (np.ndarray): indices of quadruples

        Returns:
            quads_idx (np.ndarray): indices of quadruples along with the indices of their inverses
        """

        subs = quads_idx[:, 2]
        rels = [self.inv_relation_id[x] for x in quads_idx[:, 1]]
        objs = quads_idx[:, 0]
        tss = quads_idx[:, 3]
        inv_quads_idx = np.column_stack((subs, rels, objs, tss))
        quads_idx = np.vstack((quads_idx, inv_quads_idx))

        return quads_idx
