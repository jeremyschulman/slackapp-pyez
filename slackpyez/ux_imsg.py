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

# -------------------------------------------------------------------------
# The following are the main action items
# -------------------------------------------------------------------------


def field(title, value, short=True):
    """
    Creates an Interactive message attachment field item.  The caller
    can create a list of these in the attachment.

    Notes
    -----
    API: https://api.slack.com/docs/message-buttons

    Parameters
    ----------
    title : str - The field title, User sees
    value : str - The field value, User sees
    short : bool - format in UX short mode, optional

    Returns
    -------
    dict
    """
    return dict(title=title, value=value, short=short)


# -------------------------------------------------------------------------
# The following are the main action items
# -------------------------------------------------------------------------


def select(text, action_id, options=None, option_groups=None):
    """
    Create a static selection menu item.

    Notes
    -----
    API: https://api.slack.com/docs/message-menus

    Parameters
    ----------
    text : str - what the User sees
    action_id : str - the value to identify this item in the attachment
    options : list[i_option] - list of option values
    option_groups : list[i_option_group] - list of option group values

    Returns
    -------
    dict
    """

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


def button(text, name=None, value=None, style='default'):
    """
    Create an Interactive attachment button.

    Notes
    -----
    API: https://api.slack.com/docs/message-buttons

    Parameters
    ----------
    text : str - the button text the User will see
    name : str - the button name/ID value, optional, defaults to text
    value : str - the value assigned to button, optional.  defaults to name | text
    style : str
        The button style, optional default to 'default'.  Other values are:
        * 'primary' - will show green
        * 'danger' - will show red.

    Returns
    -------
    dict
    """
    return dict(type='button', text=text,
                name=name or text,value=value or name or text,
                style=style)


def i_option(text, value):
    return dict(text=text, value=value)


def i_option_group(group, options):
    return dict(text=group, options=[
        i_option(o_t, o_v)
        for o_t, o_v in options
    ])


# -------------------------------------------------------------------------
# Value helpers
# -------------------------------------------------------------------------

def v_action(action_data):
    """
    Returns a tuple (item_id, item_value) based on the type of action
    that the User interacted with.

    Parameters
    ----------
    action_data : dict
        The action data element

    Returns
    -------
    tuple
    """
    return {
        'button':
            lambda: (action_data['name'], action_data['value']),
        'select':
            lambda: (action_data['name'], action_data['selected_options'][0]['value'])
    }.get(
        action_data['type'])()
