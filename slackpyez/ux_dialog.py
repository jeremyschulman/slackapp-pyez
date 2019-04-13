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



"""
This file contains the Slack components for using Dialogs

Notes
-----
API: https://api.slack.com/dialogs

For reference, the dialog fields are copy/paste from the API here:

    title : str
        User-facing title of this entire dialog. 24 characters to work with and
        it's required.

    callback_id	: str
        An identifier strictly for you to recognize submissions of this
        particular instance of a dialog. Use something meaningful to your app.
        255 characters maximum. Don't use this ID to reference sensitive data;
        use the more expansive state parameter below for that. Absolutely
        required.

    elements : dict
        Up to 10 form elements are allowed per dialog. See elements below.
        Required.

    state : str
        An optional string that will be echoed back to your app when a user
        interacts with your dialog. Use it as a pointer to reference sensitive
        data stored elsewhere.

    submit_label : str
        User-facing string for whichever button-like thing submits the form,
        depending on form factor. Defaults to Submit, localized in whichever
        language the end user prefers. 48 characters maximum, and may contain
        only a single word.

    notify_on_cancel : bool
        Default is false. When set to true, we'll notify your request URL
        whenever there's a user-induced dialog cancellation.
"""


def text(label, name, **kwargs):
    """
    Creates a Dialog "text element".

    Other Parameters
    ----------------
    placeholder : str
        A string displayed as needed to help guide users in completing the
        element. 150 character maximum.

    subtype : str
        ['email', 'url', 'tel', 'number']

    max_length : int
        Maximum input length allowed for element. Up to 150 characters. Defaults
        to 150.

    min_length : int
        Integer	Minimum input length allowed for element. Up to 150
        characters. Defaults to 0.

    optional : bool
        Provide true when the form element is not required. By default, form
        elements are required.

    hint : str
        Helpful text provided to assist users in answering a question. Up to 150
        characters.

    value : str
        A default value for this field. Up to 150 characters.

    Returns
    -------
    dict
    """
    return {'type': 'text', 'label': label, 'name': name,
            **kwargs}


def textarea(label, name, **kwargs):
    """
    Creates a Dialog "textarea" element.  For Parameters / Other Parameters,
    see the `func:text` above.  The only difference is the maximum length
    of the `value` field is much larger - 3000 characters.

    Returns
    -------
    dict
    """
    return {'type': 'textarea', 'label': label, 'name': name,
            **kwargs}


def select(label, name, options=None, option_groups=None, **kwargs):
    """
    Create a Dialog "select" element composed of *static* values defined
    in either the `options` or the `option_groups` lists.

    To create an item in the `options` list, use `func:i_option`.

    To create a group in the `options_groups` list, use
    `func:i_option_group`

    Parameters
    ----------
    label : str
        The select label text the User sees

    name : str
        The ID for this menu select provided in dialog submission

    options : list[dict]
        The list of i_option dicts

    option_groups : list[dict]
        the list of i_option_group dicts

    Notes
    -----
    You can only provide a MAXIMUM OF 100 items in a select element.

    Other Parameters
    ----------------
    value : str
        The select "default value".  It must be one of the `options`
        provided

    min_query_length : int
        Specify the number of characters that must be typed by a user into a
        dynamic select menu before dispatching to the app.

    placeholder	: str
        A string displayed as needed to help guide users in completing the
        element. 150 character maximum.

    optional : bool
        Provide true when the form element is not required. By default, form
        elements are required.

    Returns
    -------
    dict
    """
    if options:
        kwargs['options'] = options

    elif option_groups:
        kwargs['option_groups'] = option_groups

    else:
        raise RuntimeError("Missing param 'options' or 'option_groups'.")

    return {'type': 'select',
            'label': label,
            'name': name,
            **kwargs}


def i_option(label, value):
    """
    Create an "option item" used by the select `options` field.

    Parameters
    ----------
    label : str
        Item label the User sees

    value : str
        Item value provided in the dialog submission

    Returns
    -------
    dict
    """
    return dict(label=label, value=value)


def i_option_group(label, options):
    """
    Create an "option group" item used by select elements.

    Parameters
    ----------
    label : str
        The group label the User sess

    options : list[(label, value)]
        The list of tuple|set|list whose first item is the label and the second
        item is the value.

    Returns
    -------
    dict
    """
    return dict(
        label=label,
        options=[i_option(o_t, o_v) for o_t, o_v in options])