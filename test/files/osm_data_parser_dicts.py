result_dict = {
    'osm': {
        '@generator': 'JOSM',
        '@version': '0.6',
        'node': [
            {
                '@id': '-101768'
            },
            {
                '@id': '-101769'
            }
        ],
        'way': {
            '@id': '-101789',
            'nd': [
                {'@ref': '-101768'},
                {'@ref': '-101769'}
            ]
        },
        'relation': {
            '@id': '-99775',
            'member': {
                '@type': 'way',
                '@ref': '-101789',
                '@role': 'outer'
            },
            'tag': {
                '@k': 'ref',
                '@v': '999'
            }
        }
    }
}

result_dict_multi_ways = {
    'osm': {
        '@generator': 'JOSM',
        '@version': '0.6',
        'node': [
            {
                '@id': '-101768',
            },
            {
                '@id': '-101769',
            }
        ],
        'way': [{
            '@id': '-101789',
            'nd': [
                {'@ref': '-101768'},
                {'@ref': '-101769'}
            ]
        },
            {
                '@id': '-101790',
                'nd': [
                    {'@ref': '-101768'},
                    {'@ref': '-101769'}
                ]
            }
        ],
        'relation': {
            '@id': '-99775',
            'member': [{
                '@type': 'way',
                '@ref': '-101789',
                '@role': 'outer'
            },
                {
                    '@type': 'way',
                    '@ref': '-101790',
                    '@role': 'outer'
                },
            ],
            'tag': {
                '@k': 'ref',
                '@v': '999'
            }
        }
    }
}

relation_info_result = {
    'nodes': [
        {
            '@id': '-101768'
        },
        {
            '@id': '-101769'
        }
    ],
    'ways': [
        {
            '@id': '-101789',
            'nd': [
                {'@ref': '-101768'},
                {'@ref': '-101769'}
            ]
        }
    ],
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-101789',
            '@role': 'outer'
        }
    ],
    'ref': '999'
}

relation_info_result_multi_ways = {
    'nodes': [
        {
            '@id': '-101768'
        },
        {
            '@id': '-101769'
        }
    ],
    'ways': [
        {
            '@id': '-101789',
            'nd': [
                {'@ref': '-101768'},
                {'@ref': '-101769'}
            ]
        },
        {
            '@id': '-101790',
            'nd': [
                {'@ref': '-101768'},
                {'@ref': '-101769'}
            ]
        }
    ],
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-101789',
            '@role': 'outer'
        },
        {
            '@type': 'way',
            '@ref': '-101790',
            '@role': 'outer'
        }
    ],
    'ref': '999'
}

relation_info_result_appended = {
    'nodes': [
        {
            '@id': '-101768'
        },
        {
            '@id': '-101769'
        }
    ],
    'ways': [
        {
            '@id': '-101789',
            'nd': [
                {'@ref': '-101768'},
                {'@ref': '-101769'}
            ]
        }
    ],
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-101789',
            '@role': 'outer',
            'attributes': {
                '@id': '-101789'
            },
            'nd': [
                {'@ref': '-101768'},
                {'@ref': '-101769'}
            ]
        }
    ],
    'ref': '999'
}
