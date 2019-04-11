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

DEFAULT_SELECT_PLACEHOLDER = 'select'

# -------------------------------------------------------------------------
# primary Block object definitions
# -------------------------------------------------------------------------


def section(text, **kwargs):
    """
    Creates a "Section" block.

    Notes
    -----
    API: https://api.slack.com/reference/messaging/blocks#section

    Parameters
    ----------
    text : str
        The primary text of the section block.

    Other Parameters
    ----------------
    fields : list[<text compositions>]
    block_id : str
    accessory : dict
        One of the block element objects defined:
        https://api.slack.com/reference/messaging/block-elements

    Returns
    -------
    dict
    """
    return {'type': 'section',
            'text': c_text(text),
            **kwargs}


def context(elements):
    """
    Create a "Context" block that allows you to define text and image
    composition items in the `elements`.

    Notes
    -----
    API: https://api.slack.com/reference/messaging/blocks#context

    Parameters
    ----------
    elements

    Other Parameters
    ----------------
    block_id : str

    Returns
    -------
    dict
    """
    return {
        'type': 'context',
        'elements': elements
    }


def divider():
    """
    Creates a "Divider" block.  Nothing magical about this one.

    Notes
    -----
    API: https://api.slack.com/reference/messaging/blocks#divider

    Returns
    -------
    dict
    """
    return {'type': 'divider'}


def actions(elements, **kwargs):
    """
    Define a block "action".
    API: https://api.slack.com/reference/messaging/blocks#actions

    Other Parameters
    ----------------
    block_id : str

    Returns
    -------
    dict
    """
    return {'type': 'actions',
            'elements': elements,
            **kwargs}


def image(image_url, alt_text, **kwargs):
    """
    Create an "Image" block.

    Parameters
    ----------
    image_url : str
    alt_text : str

    Notes
    -----
    API: https://api.slack.com/reference/messaging/blocks#image

    Other Parameters
    ----------------
    title : text object
    block_id : str
    """
    return {
        'type': 'image',
        'image_url': image_url,
        'alt_text': alt_text,
        **kwargs
    }


# -------------------------------------------------------------------------
# Block message composition items begin with "c_"
# -------------------------------------------------------------------------

def c_confirm(title, text, confirm, deny='Cancel'):
    return {
        'title': c_ptext(title),
        'text': c_text(text),
        'confirm': c_ptext(confirm),
        'deny': c_ptext(deny)
    }


def c_text(text):
    return {'type': 'mrkdwn', 'text': text}


def c_ptext(text):
    return {'type': 'plain_text', 'text': text}


def c_option(text, value):
    return {'text': c_ptext(text),
            'value': value}


def c_option_group(label, options):
    return {
        'label': c_ptext(label),
        'options': [
            c_option(label, value)
            for label, value in options
        ]
    }


# -------------------------------------------------------------------------
# Block element items begin with "e_"
# -------------------------------------------------------------------------

def e_button(text, action_id=None, value=None, **kwargs):
    return {
        'type': 'button',
        'text': c_ptext(text),
        'action_id': action_id or text,
        'value': value or text,
        **kwargs}


def e_image(image_url, alt_text):
    return {
        'type': 'image',
        'image_url': image_url,
        'alt_text': alt_text
    }


def e_static_select(action_id, placeholder=None,
                    options=None, option_groups=None,
                    **kwargs):
    """
    This helper creates the "menu option select" message element dictionary.

    Parameters
    ----------
    action_id
    placeholder
    options
    option_groups
    kwargs

    Other Parameters
    ----------------

    Returns
    -------
    dict
    """
    ele = {
        'type': 'static_select',
        'action_id': action_id,
        'placeholder': c_ptext(placeholder or DEFAULT_SELECT_PLACEHOLDER)
    }

    if options:
        ele['options'] = options
    elif option_groups:
        ele['option_groups'] = option_groups

    else:
        raise RuntimeError("Required `options` | `option_groups`")

    ele.update(kwargs)
    return ele


# -------------------------------------------------------------------------
# v_<item> are used as "value" helpers to get data from the item.
# -------------------------------------------------------------------------

def v_action_selected(action):
    """
    Return the value from the selected "menu option select" element.

    Parameters
    ----------
    action : dict

    Returns
    -------
    str
        The value that was selected by the User
    """
    return action['selected_option']['value']


def v_action(action):
    return {
        'button':
            lambda a: a.get('value') or a.get('action_id'),
        'static_select':
            lambda a: v_action_selected(a),
    }[action['type']](action)


def v_first_option(options):
    """
    Return the first value in a menu-select options structure.  This is useful when
    you create an options structure and you want the first item as the placeholder or
    the default selected value.

    Parameters
    ----------
    options : list
        The menu select option list

    Returns
    -------
    str
        The text of the first option
    """
    return options[0]['text']['text']


def v_first_group_option(group_options):
    """
    Returns the first value in a menu-select that uses option_groups. This is
    useful when you create an options structure and you want the first item as
    the placeholder or the default selected value.

    Parameters
    ----------
    group_options : list
        The this of group options

    Returns
    -------
    str
        The text of the first option
    """
    return group_options[0]['options'][0]['text']['text']