result_dict_multi_ways_rail = {
    'osm': {
        'node': [
            {
                '@id': '-1',
            },
            {
                '@id': '-2',
            },
            {
                '@id': '-3',
            },
            {
                '@id': '-4',
            },
            {
                '@id': '-5',
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
                    {'@ref': '-2'},
                    {'@ref': '-3'}
                ]
            },
            {
                '@id': '-3',
                'nd': [
                    {'@ref': '-4'},
                    {'@ref': '-5'}
                ]
            },
        ],
        'relation': {
            '@id': '-1',
            'member': [{
                '@type': 'way',
                '@ref': '-1',
                '@role': ''
            },
                {
                    '@type': 'way',
                    '@ref': '-2',
                    '@role': ''
                },
                {
                    '@type': 'way',
                    '@ref': '-3',
                    '@role': ''
                }
            ],
            'tag': [{
                '@k': 'ref',
                '@v': '999'
            }, {
                '@k': 'type',
                '@v': 'route'
            },
                {
                    '@k': 'route',
                    '@v': 'railway'
                }
            ]
        }
    }
}

relation_info_railway_result_appended = {
    'nodes': [
        {
            '@id': '-1',
        },
        {
            '@id': '-2',
        },
        {
            '@id': '-3',
        },
        {
            '@id': '-4',
        },
        {
            '@id': '-5',
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
                {'@ref': '-2'},
                {'@ref': '-3'}
            ]
        },
        {
            '@id': '-3',
            'nd': [
                {'@ref': '-4'},
                {'@ref': '-5'}
            ]
        },
    ],
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-1',
            '@role': '',
            'attributes': {
                '@id': '-1'
            },
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ]
        },
        {
            '@type': 'way',
            '@ref': '-2',
            '@role': '',
            'attributes': {
                '@id': '-2'
            },
            'nd': [
                {'@ref': '-2'},
                {'@ref': '-3'}
            ]
        },
        {
            '@type': 'way',
            '@ref': '-3',
            '@role': 'outer',
            'attributes': {
                '@id': '-3'
            },
            'nd': [
                {'@ref': '-4'},
                {'@ref': '-5'}
            ]
        },
    ],
    'ref': '999',
    'type': 'route',
    'route': 'railway'
}

relation_info_highway_to_test_backward_role = {
    'ways_to_search': [
        {
            '@role': 'backward',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'},
                {'@ref': '-3'},
                {'@ref': '-4'}
            ]
        },
    ],
}

relation_info_highway_to_test_if_roundabout = {
    'ways_to_search': [
        {
            '@role': '',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ],
            'tag': [
                {"@k": "junction",
                 "@v": "roundabout"}
            ]
        },
        {
            '@role': '',
            'nd': [
                {'@ref': '-3'},
                {'@ref': '-4'}
            ]
        }
    ],
}

relation_info_highway_forward = {
    'ways_to_search': [
        {
            '@role': 'forward',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ],
        },
        {
            '@role': 'forward',
            'nd': [
                {'@ref': '-2'},
                {'@ref': '-3'}
            ]
        },
        {
            '@role': '',
            'nd': [
                {'@ref': '-3'},
                {'@ref': '-4'}
            ]
        },
        {
            '@role': 'forward',
            'nd': [
                {'@ref': '-4'},
                {'@ref': '-5'}
            ]
        },
        {
            '@role': 'forward',
            'nd': [
                {'@ref': '-5'},
                {'@ref': '-6'}
            ]
        },
    ],
}

relation_info_gap_in_first_forward_series = {
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-1',
            '@role': 'forward',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ],
        },
        {
            '@type': 'way',
            '@ref': '-2',
            '@role': 'forward',
            'nd': [
                {'@ref': '-2'},
                {'@ref': '-3'}
            ]
        },
        {
            '@type': 'way',
            '@ref': '-3',
            '@role': 'forward',
            'nd': [
                {'@ref': '-4'},
                {'@ref': '-3'}
            ]
        },
        {
            '@type': 'way',
            '@ref': '-4',
            '@role': '',
            'nd': [
                {'@ref': '-5'},
                {'@ref': '-6'}
            ]
        }
    ],
}

relation_info_no_gap_in_first_forward_series = {
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-1',
            '@role': 'forward',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ],
            'tag': [
                {
                    "@k": "oneway",
                    "@v": "yes"
                }
            ]
        },
        {
            '@type': 'way',
            '@ref': '-2',
            '@role': 'forward',
            'nd': [
                {'@ref': '-2'},
                {'@ref': '-3'}
            ],
            'tag': [
                {
                    "@k": "oneway",
                    "@v": "yes"
                }
            ]
        },
        {
            '@type': 'way',
            '@ref': '-3',
            '@role': 'forward',
            'nd': [
                {'@ref': '-4'},
                {'@ref': '-3'}
            ],
            'tag': [
                {
                    "@k": "oneway",
                    "@v": "yes"
                }
            ]
        },
        {
            '@type': 'way',
            '@ref': '-4',
            '@role': '',
            'nd': [
                {'@ref': '-3'},
                {'@ref': '-5'}
            ]
        }
    ],
}

relation_info_roundabout_only_one_forward_roled = {
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-1',
            '@role': '',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ],
        },
        {
            '@type': 'way',
            '@ref': '-2',
            '@role': 'forward',
            'nd': [
                {'@ref': '-2'},
                {'@ref': '-3'}
            ],
        },
        {
            '@type': 'way',
            '@ref': '-3',
            '@role': '',
            'nd': [
                {'@ref': '-3'},
                {'@ref': '-4'},
                {'@ref': '-5'}
            ],
            'tag': [
                {
                    '@k': 'junction',
                    '@v': 'roundabout'
                }
            ]
        },
    ],
}

relation_info_roundabout_previous_last_is_current_last = {
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-1',
            '@role': 'forward',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ],
        },
        {
            '@type': 'way',
            '@ref': '-2',
            '@role': 'forward',
            'nd': [
                {'@ref': '-2'},
                {'@ref': '-3'}
            ],
        },
        {
            '@type': 'way',
            '@ref': '-3',
            '@role': '',
            'nd': [
                {'@ref': '-3'},
                {'@ref': '-4'},
                {'@ref': '-3'}
            ],
            'tag': [
                {
                    '@k': 'junction',
                    '@v': 'roundabout'
                }
            ]
        },
    ],
}

relation_info_roundabout_two_roundabout_pieces = {
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-4',
            '@role': 'forward',
            'nd': [
                {'@ref': '-5'},
                {'@ref': '-6'},
                {'@ref': '-7'}
            ],
            'tag': [
                {
                    '@k': 'junction',
                    '@v': 'roundabout'
                }
            ]
        },
        {
            '@type': 'way',
            '@ref': '-5',
            '@role': 'forward',
            'nd': [
                {'@ref': '-7'},
                {'@ref': '-8'},
                {'@ref': '-9'}
            ],
            'tag': [
                {
                    '@k': 'junction',
                    '@v': 'roundabout'
                }
            ],
        },
        {
            '@type': 'way',
            '@ref': '-6',
            '@role': '',
            'nd': [
                {'@ref': '-8'},
                {'@ref': '-9'},
                {'@ref': '-10'}
            ],
        },
    ],
}

relation_info_continuous_series = {
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-4',
            '@role': '',
            'nd': [
                {'@ref': '-5'},
                {'@ref': '-6'},
                {'@ref': '-7'}
            ],
        },
        {
            '@type': 'way',
            '@ref': '-5',
            '@role': '',
            'nd': [
                {'@ref': '-7'},
                {'@ref': '-8'},
                {'@ref': '-9'}
            ],
        },
        {
            '@type': 'way',
            '@ref': '-6',
            '@role': '',
            'nd': [
                {'@ref': '-9'},
                {'@ref': '-10'},
            ],
        },
    ],
    "network": "HU:National",
    "ref": "9999"
}

relation_info_NNFN_pattern = {
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-4',
            '@role': '',
            'nd': [
                {'@ref': '-5'},
                {'@ref': '-6'},
                {'@ref': '-7'}
            ],
        },
        {
            '@type': 'way',
            '@ref': '-5',
            '@role': '',
            'nd': [
                {'@ref': '-7'},
                {'@ref': '-8'},
                {'@ref': '-9'}
            ],
        },
        {
            '@type': 'way',
            '@ref': '-6',
            '@role': 'forward',
            'nd': [
                {'@ref': '-9'},
                {'@ref': '-10'},
            ],
        },
        {
            '@type': 'way',
            '@ref': '-7',
            '@role': '',
            'nd': [
                {'@ref': '-10'},
                {'@ref': '-11'},
            ],
        },
    ],
    "network": "HU:National",
    "ref": "9999"
}

relation_info_no_gap_in_first_forward_series_no_oneway = {
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-1',
            '@role': 'forward',
            'nd': [
                {'@ref': '-1'},
                {'@ref': '-2'}
            ],
        },
        {
            '@type': 'way',
            '@ref': '-2',
            '@role': 'forward',
            'nd': [
                {'@ref': '-2'},
                {'@ref': '-3'}
            ],
        },
        {
            '@type': 'way',
            '@ref': '-3',
            '@role': 'forward',
            'nd': [
                {'@ref': '-4'},
                {'@ref': '-3'}
            ],
        },
        {
            '@type': 'way',
            '@ref': '-4',
            '@role': '',
            'nd': [
                {'@ref': '-3'},
                {'@ref': '-5'}
            ],
            'tag': [
                {
                    "@k": "oneway",
                    "@v": "yes"
                }
            ]
        }
    ],
}