Unit tests:

- ☑ Continuous road, no roles, order is wrong
- ☑ Continuous road, good order, it has a oneway road, the rest is normal: the oneway should be two-way.
- ☑ Continuous road, wrong order, it has a oneway road, the rest is normal: the oneway should be two-way.
- ☑ Continuous road, good/wrong order(doesn't matter though now, since now we know it puts the roads together correctly), it has a forward road, the rest is normal: the forward role should be removed - works both with motorway and only one piece forward series.
---
- ☑ Split one way road, order is swapped
- ☑ Split one way road, order is swapped, has some backward roled road pieces
  (handling of these: if it's not a biking path, then make the backward member forward, and reverse its nodes. According to OSM wiki, reverse role is used at bike paths if they're going the opposite direction than what the road originally heads to, especially if it's one-way)
- ☑ Split one way road, order and the starting way is swapped
- [?] Split road but it doesn't have the forward roles given and not one-way. It's a good question if this can be fixed, depending the order of the relation. if the continuation and not the other side comes, that side will be literally neglected.
---
- ☑ Closed roundabout correct roles wrong order
- ☑ Closed roundabout correct roles correct order
- ☑ Closed roundabout wrong roles wrong order
- ☑ Closed roundabout wrong roles correct order
- ☑ Closed roundabout: ways that go in it but not merging back, going split and merging back at another roundabout. FYI: Road nr. 67 north of Kaposvár but closed (so it's like double roundaboutish thing)
---
- ☑ Open roundabout correct roles wrong order
- ☑ Open roundabout correct roles correct order
- ☑ Open roundabout wrong roles correct order 
- ☑ Open roundabout correct roles wrong order, extra members in roundabout
- ☑ Open roundabout wrong roles wrong order

- ☐ Open roundabout: ways that go in it but not merging back, going split and merging back at another roundabout. FYI: Road nr. 67 north of Kaposvár
---
- ☑ It's an expressway but has no roles, which is wrong

- ☐ Get the missing route piece from the map itself. For local files though the <way> </way> list should contain it , but from Overpass the list can be queried too

 
18/21 (20) is done.