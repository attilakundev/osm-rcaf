from error_hwy import ErrorHighway, ErrorMultipolygon
import sys
from pathlib import Path
import gettext

project_path = Path(__file__).resolve().parent.absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib/model")


class OSMErrorMessages:
    def remote_relation(self, relation_id, source):
        remote_relation = ("https://osm.org/relation/{}").format(relation_id) if not source else relation_id
        return remote_relation

    def remote_way(self, way_id, source):
        remote_relation = ("https://osm.org/way/{}").format(way_id) if not source else way_id
        return remote_relation

    def remote_node(self, way_id, source):
        remote_relation = ("https://osm.org/node/{}").format(way_id) if not source else way_id
        return remote_relation

    def return_messages(self, error_information, correct_ways_count, relation_id, source, language, verbose):
        translation = gettext.translation(domain="base", localedir="locale", languages=[language], fallback=True)
        translation.install()
        _ = translation.gettext
        messages = []
        errors = len(error_information)
        total = errors + correct_ways_count
        correctness = round((correct_ways_count / total) * 100, 2)

        print(_("=================[Relation #{relation_id}]=================").format(relation_id=relation_id))
        if errors > 0:
            if not verbose:
                messages.append(_("This relation has {errors} errors and {correct_ways_count} correct ways. "
                                  "That's {correctness}% correct.").format(errors=errors,
                                                                           correct_ways_count=correct_ways_count,
                                                                           correctness=correctness))
            else:
                for error in error_information:
                    if type(error_information[0]) == ErrorHighway:
                        relation = self.remote_relation(relation_id, source)
                        previous_ref = self.remote_way(error.previous_ref, source)
                        current_way = self.remote_way(error.current_ref, source)
                        last_forward_way_before_backward_direction = self.remote_way(
                            error.last_forward_way_before_backward_direction[0], source)
                        currently_checked_ref = self.remote_way(error.currently_checked_ref, source)
                        current_ref = self.remote_way(error.current_ref, source)
                        match error_information[0].error_type:
                            case "Gap at the beginning":
                                messages.append(_("ERROR: Relation ref={relation} has gap at way: {current_way}"
                                                  "This case occured because there is a gap, this happened at the beginning of the "
                                                  "relation, since it started with a 2x2 seperated highway. "
                                                  "The ID of last way before going to backward direction: "
                                                  "{last_forward_way_before_backward_direction}"
                                                  .format(relation=relation,
                                                          current_way=current_way,
                                                          last_forward_way_before_backward_direction=last_forward_way_before_backward_direction)))

                            case "Split roundabout":
                                messages.append(
                                    _("INFO: There is a roundabout split up to multiple ways, "
                                      "last known way is {current_way}").format(
                                        current_way=current_way))
                            case "Forward but not oneway":
                                messages.append(
                                    _("ERROR: Relation ref={currently_checked_ref} has a road segment which"
                                      "has forward role, but not oneway and the following road segment"
                                      " is a normal road segment, way number where this was found: {current_ref}\n "
                                      "Previous way:{previous_ref}".format(currently_checked_ref=currently_checked_ref,
                                                                           current_ref=current_ref,
                                                                           previous_ref=previous_ref)

                                      ))
                    else:
                        # type is ErrorMultipolygon
                        pass
            return messages
