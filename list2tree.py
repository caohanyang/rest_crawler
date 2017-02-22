#!/usr/bin/env python
# coding=utf-8
import itertools
import pprint
from ete3 import Tree

pages = ['https://www.instagram.com/developer/endpoints/users',
'https://www.instagram.com/developer/endpoints/likes',
'https://www.instagram.com/developer/endpoints/tags',
'https://www.instagram.com/developer/endpoints/relationships',
'https://www.instagram.com/developer/endpoints/comments',
'https://www.instagram.com/developer/endpoints/locations',
'https://www.instagram.com/developer/endpoints/media',
'https://www.instagram.com/developer/endpoints',
'https://www.instagram.fr/developer/endpoints/media',]



def group_urls(url_set, depth=0):
    """
    Fetches the actions for a particular domain
    """
    url_set = sorted(url_set, key=lambda x: x[depth])

    t = Tree()

    leaves = filter(lambda x: len(x) - 1 == depth, url_set)
    for cluster, group in itertools.groupby(leaves, lambda x: x[depth]):
        branch = list(group)
        t.add_child(name='/'+cluster)

    twigs = filter(lambda x: len(x) - 1 > depth, url_set)
    for cluster, group in itertools.groupby(twigs, lambda x: x[depth]):
        group_list = list(group)
        branch = group_urls(group_list, depth+1)
        # tree.append({cluster: branch})
        if depth == 0:
           branch.name = cluster
        else:
           branch.name = '/'+cluster
        t.add_child(branch)
    return t

if __name__ == '__main__':
    page_list = []
    for page in pages:
        page = page.split('://')[-1].split('/')
        page_list.append(page)
    t = group_urls(page_list)
    print t.get_ascii(show_internal=True)

    for leaf in t:
      print leaf.name