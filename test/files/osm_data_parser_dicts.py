result_dict = {
    'osm': {
        '@editor': 'Attila Kun',
        '@version': '0.6',
        'node': [
            {
                '@id': '-1'
            },
            {
                '@id': '-2'
            }
        ],
        'way': {
            '@id': '-1',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ],
            'tag':
                {'@k': 'oneway',
                 '@v': 'yes'},

        },
        'relation': {
            '@id': '-99775',
            'member': {
                '@type': 'way',
                '@ref': '-1',
                '@role': 'outer'
            },
            'tag': {
                '@k': 'ref',
                '@v': '999'
            }
        }
    }
}

result_dict_multi_relation = {
    'osm': {
        '@generator': 'JOSM',
        '@version': '0.6',
        'node': [
            {
                '@id': '-1'
            },
            {
                '@id': '-2'
            }
        ],
        'way': {
            '@id': '-1',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ],
            'tag':
                {'@k': 'oneway',
                 '@v': 'yes'},

        },
        'relation': [
            {
                '@id': '-99775',
                'member': {
                    '@type': 'way',
                    '@ref': '-1',
                    '@role': 'outer'
                },
                'tag': {
                    '@k': 'ref',
                    '@v': '999'
                }
            },
            {
                '@id': '-99776',
                'member': {
                    '@type': 'way',
                    '@ref': '-1',
                    '@role': 'outer'
                },
                'tag': {
                    '@k': 'ref',
                    '@v': '999'
                }
            },
        ]
    }
}

result_dict_multi_ways = {
    'osm': {
        '@generator': 'JOSM',
        '@version': '0.6',
        'node': [
            {
                '@id': '-1',
            },
            {
                '@id': '-2',
            }
        ],
        'way': [{
            '@id': '-1',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ]
        },
            {
                '@id': '-2',
                'nd': [
                    {'@ref': '-1'},
                    {'@ref': '-2'}
                ]
            }
        ],
        'relation': {
            '@id': '-99775',
            'member': [{
                '@type': 'way',
                '@ref': '-1',
                '@role': 'outer'
            },
                {
                    '@type': 'way',
                    '@ref': '-2',
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
            '@id': '-1'
        },
        {
            '@id': '-2'
        }
    ],
    'ways': [
        {
            '@id': '-1',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ],
            'tag': {'@k': 'oneway',
                    '@v': 'yes'},
        }
    ],
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-1',
            '@role': 'outer'
        }
    ],
    'ref': '999'
}

relation_info_result_multi_ways = {
    'nodes': [
        {
            '@id': '-1'
        },
        {
            '@id': '-2'
        }
    ],
    'ways': [
        {
            '@id': '-1',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ]
        },
        {
            '@id': '-2',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ]
        }
    ],
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-1',
            '@role': 'outer'
        },
        {
            '@type': 'way',
            '@ref': '-2',
            '@role': 'outer'
        }
    ],
    'ref': '999'
}

relation_info_result_appended = {
    'nodes': [
        {
            '@id': '-1'
        },
        {
            '@id': '-2'
        }
    ],
    'ways': [
        {
            '@id': '-1',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ],
            'tag':
                {'@k': 'oneway',
                 '@v': 'yes'},
        }
    ],
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-1',
            '@role': 'outer',
            'attributes': {
                '@id': '-1'
            },
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ],
            'tag': [
                {'@k': 'oneway',
                 '@v': 'yes'},
            ]
        }
    ],
    'ref': '999'
}

result_dict_MUTCD = {
    'osm': {
        '@generator': 'JOSM',
        '@version': '0.6',
        'node': [
            {
                '@id': '-1'
            },
            {
                '@id': '-2'
            },
            {
                '@id': '-3'
            },
            {
                '@id': '-4'
            }
        ],
        'way': [
            {
                '@id': '-1',
                'nd': [
                    {'@ref': '-1'},
                    {'@ref': '-2'}
                ],
                'tag': [
                    {
                        '@k': 'oneway',
                        '@v': 'yes'
                    },
                    {
                        '@k': 'ref',
                        '@v': '3'
                    }
                ]
            },
            {
                '@id': '-2',
                'nd': [
                    {'@ref': '-3'},
                    {'@ref': '-4'}
                ],
                'tag': [
                    {
                        '@k': 'oneway',
                        '@v': 'yes'
                    },
                    {
                        '@k': 'ref',
                        '@v': '3'
                    }
                ]
            },
        ],
        'relation': {
            '@id': '-99775',
            'member': [
                {
                    '@type': 'way',
                    '@ref': '-2',
                    '@role': 'outer'
                },
                {
                    '@type': 'way',
                    '@ref': '-1',
                    '@role': 'outer'
                }],
            'tag': {
                '@k': 'network',
                '@v': 'US:WV'
            }
        }
    }
}

relation_info_result_relation_multiple_tags = {
    'nodes': [
        {
            '@id': '-1'
        },
        {
            '@id': '-2'
        },
        {
            '@id': '-3'
        },
        {
            '@id': '-4'
        }
    ],
    'ways': [
        {
            '@id': '-1',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ],
            'tag': [
                {
                    '@k': 'oneway',
                    '@v': 'yes'
                },
                {
                    '@k': 'ref',
                    '@v': '3'
                }
            ]
        },
        {
            '@id': '-2',
            'nd': [
                {'@ref': '-3'},
                {'@ref': '-4'}
            ],
            'tag': [
                {
                    '@k': 'oneway',
                    '@v': 'yes'
                },
                {
                    '@k': 'ref',
                    '@v': '3'
                }
            ]
        },
    ],
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-2',
            '@role': 'outer'
        },
        {
            '@type': 'way',
            '@ref': '-1',
            '@role': 'outer'
        }
    ],
    "isMUTCDcountry": True,
    "network": "US:WV"
}

relation_info_way_has_multiple_tags_result_appended = {
    'nodes': [
        {
            '@id': '-1'
        },
        {
            '@id': '-2'
        },
        {
            '@id': '-3'
        },
        {
            '@id': '-4'
        }
    ],
    'ways': [
        {
            '@id': '-1',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ],
            'tag': [
                {
                    '@k': 'oneway',
                    '@v': 'yes'
                },
                {
                    '@k': 'ref',
                    '@v': '3'
                }
            ]
        },
        {
            '@id': '-2',
            'nd': [
                {'@ref': '-3'},
                {'@ref': '-4'}
            ],
            'tag': [
                {
                    '@k': 'oneway',
                    '@v': 'yes'
                },
                {
                    '@k': 'ref',
                    '@v': '3'
                }
            ]
        },
    ],
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-2',
            '@role': 'outer',
            'attributes': {
                '@id': '-2'
            },
            'nd': [
                {'@ref': '-3'},
                {'@ref': '-4'}
            ],
            'tag': [
                {
                    '@k': 'oneway',
                    '@v': 'yes'
                },
                {
                    '@k': 'ref',
                    '@v': '3'
                }
            ]
        },
        {
            '@type': 'way',
            '@ref': '-1',
            '@role': 'outer',
            'attributes': {
                '@id': '-1'
            },
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ],
            'tag': [
                {
                    '@k': 'oneway',
                    '@v': 'yes'
                },
                {
                    '@k': 'ref',
                    '@v': '3'
                }
            ]
        }
    ],
    "isMUTCDcountry": True,
    "network": "US:WV"
}
