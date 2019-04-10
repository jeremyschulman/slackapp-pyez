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
# c_<item> - message composition object
# -------------------------------------------------------------------------


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


def c_confirm(title, text, confirm, deny='Cancel'):
    return {
        'title': c_ptext(title),
        'text': c_text(text),
        'confirm': c_ptext(confirm),
        'deny': c_ptext(deny)
    }


def section(text, **kwargs):
    return {'type': 'section',
            'text': c_text(text),
            **kwargs}


def context(elements):
    return {
        'type': 'context',
        'elements': elements
    }


def divider():
    return {'type': 'divider'}


def actions(elements, **kwargs):
    return {'type': 'actions',
            'elements': elements,
            **kwargs}


def b_image(image_url, alt_text, **kwargs):
    """

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
# e_<item> - block element definitions
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
