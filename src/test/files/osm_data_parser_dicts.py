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
            'tag': [
                {
                    '@k': 'ref',
                    '@v': '999'
                },
                {
                    '@k': 'type',
                    '@v': 'route'
                },
                {
                    '@k': 'route',
                    '@v': 'road'
                }
            ]
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
                'tag': [
                    {
                        '@k': 'ref',
                        '@v': '999'
                    },
                    {
                        '@k': 'type',
                        '@v': 'route'
                    },
                    {
                        '@k': 'route',
                        '@v': 'road'
                    }
                ]
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
    'ref': '999',
    'route': 'road',
    'type': 'route'
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
            'tag': {'@k': 'oneway',
                    '@v': 'yes'}
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
    'ref': '999',
    'route': 'road',
    'type': 'route'
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

corrected_relation_data = {'osm': {
    '@version': '0.6',
    '@editor': 'Attila Kun',
    'node': [
        {'@id': '-1'},
        {'@id': '-2'},
        {'@id': '-3'},
        {'@id': '-4'},
        {'@id': '-5'},
        {'@id': '-6'},
        {'@id': '-7'},
        {'@id': '-8'},
        {'@id': '-9'},
        {'@id': '-10'},
        {'@id': '-11'},
        {'@id': '-12'},
        {'@id': '-13'},
        {'@id': '-14'},
        {'@id': '-15'},
        {'@id': '-16'},
        {'@id': '-17'},
    ],
    'way': [
        {'@id': '-1', 'nd': [
            {'@ref': '-1'},
            {'@ref': '-2'},
            {'@ref': '-3'},
            {'@ref': '-4'},
            {'@ref': '-5'},
            {'@ref': '-6'},
            {'@ref': '-7'},
        ], 'tag': [{'@k': 'highway', '@v': 'primary'}]},
        {
            '@id': '-2',
            '@action': 'modify',
            'nd': [{'@ref': '-11'}, {'@ref': '-14'}, {'@ref': '-13'},
                   {'@ref': '-12'}],
            'tag': [{'@k': 'highway', '@v': 'primary'}, {'@k': 'oneway'
                , '@v': 'yes'}],
        },
        {'@id': '-3', 'nd': [{'@ref': '-11'}, {'@ref': '-15'},
                             {'@ref': '-16'}, {'@ref': '-17'}], 'tag': [{'@k': 'highway',
                                                                         '@v': 'primary'}]},
        {'@id': '-4', 'nd': [{'@ref': '-7'}, {'@ref': '-8'},
                             {'@ref': '-9'}], 'tag': [{'@k': 'highway', '@v': 'primary'},
                                                      {'@k': 'oneway', '@v': 'yes'}]},
        {
            '@id': '-5',
            '@action': 'modify',
            'nd': [{'@ref': '-12'}, {'@ref': '-7'}],
            'tag': [{'@k': 'highway', '@v': 'primary'}, {'@k': 'oneway'
                , '@v': 'yes'}],
        },
        {
            '@id': '-6',
            '@action': 'modify',
            'nd': [{'@ref': '-9'}, {'@ref': '-10'}, {'@ref': '-11'}],
            'tag': [{'@k': 'highway', '@v': 'primary'}, {'@k': 'oneway'
                , '@v': 'yes'}],
        },
    ],
    'relation': {
        '@id': '-99802',
        '@visible': 'true',
        'member': [
            {'@type': 'way', '@ref': '-1', '@role': ''},
            {'@type': 'way', '@ref': '-4', '@role': 'forward'},
            {'@type': 'way', '@ref': '-6', '@role': 'forward'},
            {'@type': 'way', '@ref': '-5', '@role': 'forward'},
            {'@type': 'way', '@ref': '-2', '@role': 'forward'},
            {'@type': 'way', '@ref': '-3', '@role': ''},
        ],
        'tag': [{'@k': 'ref', '@v': 'CR 999'}, {'@k': 'route',
                                                '@v': 'road'}, {'@k': 'type', '@v': 'route'}],
        '@action': 'modify',
    },
}}
