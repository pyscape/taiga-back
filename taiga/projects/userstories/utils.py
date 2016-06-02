# -*- coding: utf-8 -*-
# Copyright (C) 2014-2016 Andrey Antukh <niwi@niwi.nz>
# Copyright (C) 2014-2016 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2016 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014-2016 Alejandro Alonso <alejandro.alonso@kaleidos.net>
# Copyright (C) 2014-2016 Anler Hernández <hello@anler.me>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


def attach_total_points(queryset, as_field="total_points_attr"):
    """Attach total of point values to each object of the queryset.

    :param queryset: A Django user stories queryset object.
    :param as_field: Attach the points as an attribute with this name.

    :return: Queryset object with the additional `as_field` field.
    """
    model = queryset.model
    sql = """SELECT SUM(projects_points.value)
            	    FROM userstories_rolepoints
                    INNER JOIN projects_points ON userstories_rolepoints.points_id = projects_points.id
                    WHERE userstories_rolepoints.user_story_id = {tbl}.id"""

    sql = sql.format(tbl=model._meta.db_table)
    queryset = queryset.extra(select={as_field: sql})
    return queryset


def attach_role_points(queryset, as_field="role_points_attr"):
    """Attach role point as json column to each object of the queryset.

    :param queryset: A Django user stories queryset object.
    :param as_field: Attach the role points as an attribute with this name.

    :return: Queryset object with the additional `as_field` field.
    """
    model = queryset.model
    sql = """SELECT format('[%%s]', string_agg(format('{{"%%s":%%s}}', to_json(userstories_rolepoints.role_id), to_json(userstories_rolepoints.points_id)), ','))::text
            	    FROM userstories_rolepoints
                    WHERE userstories_rolepoints.user_story_id = {tbl}.id"""

    sql = sql.format(tbl=model._meta.db_table)
    queryset = queryset.extra(select={as_field: sql})
    return queryset


def attach_tasks(queryset, as_field="tasks_attr"):
    """Attach tasks as json column to each object of the queryset.

    :param queryset: A Django user stories queryset object.
    :param as_field: Attach the role points as an attribute with this name.

    :return: Queryset object with the additional `as_field` field.
    """

    model = queryset.model
    sql = """SELECT format('[%%s]', string_agg(format('{{
                        "id":%%s,
                        "ref": %%s,
                        "subject": %%s,
                        "status": %%s,
                        "is_blocked": %%s,
                        "is_iocaine": %%s,
                        "is_closed": %%s
                    }}',
                    to_json(tasks_task.id),
                    to_json(tasks_task.ref),
                    to_json(tasks_task.subject),
                    to_json(tasks_task.status_id),
                    to_json(tasks_task.is_blocked),
                    to_json(tasks_task.is_iocaine),
                    to_json(projects_taskstatus.is_closed)), ','))::text
                FROM tasks_task
                INNER JOIN projects_taskstatus on projects_taskstatus.id = tasks_task.status_id
                WHERE user_story_id = {tbl}.id"""

    sql = sql.format(tbl=model._meta.db_table)
    queryset = queryset.extra(select={as_field: sql})
    return queryset
