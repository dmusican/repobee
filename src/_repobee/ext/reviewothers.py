"""A peer review plugin which assigns one set of students to review all
other students.
Intended for student graders who are in the class for which they are grading.
Once those student graders have submitted their own work to the instructor, the
instructor can use this plugin to make the other repos in the class
available to the student graders.

.. module:: reviewothers
    :synopsis: Plugin that allows a student grader to review others.

.. moduleauthor:: Dave Musicant, Simon Larsén
"""
import random
from typing import List


import repobee_plug as plug

PLUGIN_DESCRIPTION = (
    "Allows a student grader team to be able to review another set of "
    "students; typically the rest of the class."
)


class ReviewOthers(plug.Plugin, plug.cli.CommandExtension):
    __settings__ = plug.cli.command_extension_settings(
        actions=[plug.cli.CoreCommand.reviews.assign]
    )

    grader = plug.cli.option(
        help="username of student grader",
        required=True,
    )


    def generate_review_allocations(
        self, teams: List[plug.StudentTeam], num_reviews: int = 1
    ) -> List[plug.ReviewAllocation]:
        """Generate peer review allocations so that the student grader team
        reviews all other teams.

        The ``num_reviews`` argument is ignored by this plugin.

        Args:
            teams: Student teams to be reviewed
            num_reviews: Ignored by this plugin.
        Returns:
            A list of allocations that
        """

        grader_team = plug.StudentTeam(members=[self.grader])
        teams = list(teams)
        if num_reviews != 1:
            plug.log.warning(
                "num_reviews specified to {}, but in review others "
                "num_reviews is ignored".format(num_reviews)
            )


        allocations = []
        for reviewed_team in teams:
            allocations.append(
                plug.ReviewAllocation(
                    review_team=grader_team, reviewed_team=reviewed_team
                )
            )
        return allocations
