relation = {
    "ways": [
        {
            "@ref": "1",
            "@role": "forward",
            "@type": "way",
            "attributes": {
                "@id": "1"
            },
            "nd": [
                {
                    "@ref": 1
                },
                {
                    "@ref": 2
                },
                {
                    "@ref": 3
                }
            ],
            "tag": [
                {
                    "@k": "highway",
                    "@v": "primary"
                },
                {
                    "@k": "railway",
                    "@v": "rail"
                },
                {
                    "@k": "oneway",
                    "@v": "yes"
                },
                {
                    "@k": "junction",
                    "@v": "roundabout"
                },
            ]
        },
        {
            "@ref": "2",
            "@role": "",
            "@type": "way",
            "attributes": {
                "@id": "1"
            },
            "nd": [
                {
                    "@ref": 3
                },
                {
                    "@ref": 4
                },
                {
                    "@ref": 5
                },
                {
                    "@ref": 6
                },
                {
                    "@ref": 3
                }
            ],
            "tag": [
                {
                    "@k": "highway",
                    "@v": "primary"
                },
                {
                    "@k": "railway",
                    "@v": "rail"
                },
                {
                    "@k": "oneway",
                    "@v": "yes"
                },
                {
                    "@k": "junction",
                    "@v": "roundabout"
                },
                {
                    "@k": "ref",
                    "@v": "3"
                }
            ]
        },
        {
            "@ref": "3",
            "@role": "",
            "@type": "node",
            "attributes": {
                "@id": "3"
            },
        },
        {
            "@ref": "4",
            "@role": "",
            "@type": "way",
            "tag": [
                {
                    "@k": "ref",
                    "@v": "3"
                }
            ]
        },
    ],

    "network": "HU:national",
    "ref": 710,
    "type": "route",
    "route": "road"
}

relation2 = {
    "network": "US:WV:County"
}