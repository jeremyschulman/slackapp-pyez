#  Copyright 2019 Jeremy Schulman, nwkautomaniac@gmail.com
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


def select(text, action_id, options=None, option_groups=None):
    select_data = dict(
        type='select',
        name=action_id,
        text=text
    )

    if options:
        select_data['options'] = options
    elif option_groups:
        select_data['option_groups'] = option_groups
    else:
        raise RuntimeError("Missing `options` or `option_groups`")

    return select_data


def field(title, value, short=True):
    return dict(title=title, value=value, short=short)


def i_option(text, value):
    return dict(text=text, value=value)


def i_option_group(group, options):
    return dict(text=group, options=[
        i_option(o_t, o_v)
        for o_t, o_v in options
    ])


def v_action(action_data):
    return {
        'button':
            lambda: (action_data['name'], action_data['value']),
        'select':
            lambda: (action_data['name'], action_data['selected_options'][0]['value'])
    }.get(
        action_data['type'])()
