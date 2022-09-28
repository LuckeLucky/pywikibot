import re
from mwparserfromhell.nodes import Text, Template
from scripts.match2conversion.match2exceptions import VodX, WikiStyle

def get_parent_wikicode(wikicode, node):
    """
    Returns the parent of `node` as a `wikicode` object.
    Raises :exc:`ValueError` if `node` is not a descendant of `wikicode`.
    """
    context, index = wikicode._do_strong_search(node, True)
    return context

def remove_and_squash(wikicode, obj):
    """
	merit to https://github.com/lahwaacz/wiki-scripts :)
    Remove `obj` from `wikicode` and fix whitespace in the place it was removed from.
    """
    parent = get_parent_wikicode(wikicode, obj)
    index = parent.index(obj)
    parent.remove(obj)

    def _get_text(index):
        # the first node has no previous node, especially not the last node
        if index < 0:
            return None, None
        try:
            node = parent.get(index)
            # don't EVER remove whitespace from non-Text nodes (it would
            # modify the objects by converting to str, making the operation
            # and replacing the object with str, but we keep references to
            # the old nodes)
            if not isinstance(node, Text):
                return None, Text
            return node, Text
        except IndexError:
            return None, None

    prev, prev_cls = _get_text(index - 1)
    next_, next_cls = _get_text(index)

    if prev is None and next_ is not None:
        # strip only at the beginning of the document, not after non-text elements,
        # see https://github.com/lahwaacz/wiki-scripts/issues/44
        if prev_cls is None:
            next_.value = next_.lstrip()
    elif prev is not None and next_ is None:
        # strip only at the end of the document, not before non-text elements,
        # see https://github.com/lahwaacz/wiki-scripts/issues/44
        if next_cls is None:
            prev.value = prev.value.rstrip()
    elif prev is not None and next_ is not None:
        if prev.endswith(" ") and next_.startswith(" "):
            prev.value = prev.rstrip(" ")
            next_.value = " " + next_.lstrip(" ")
        elif prev.endswith("\n") and next_.startswith("\n"):
            if prev[:-1].endswith("\n") or next_[1:].startswith("\n"):
                # preserve preceding blank line
                prev.value = prev.rstrip("\n") + "\n\n"
                next_.value = next_.lstrip("\n")
            else:
                # leave one linebreak
                prev.value = prev.rstrip("\n") + "\n"
                next_.value = next_.lstrip("\n")
        elif prev.endswith("\n"):
            next_.value = next_.lstrip()
        elif next_.startswith("\n"):    # pragma: no branch
            prev.value = prev.rstrip()
        # merge successive Text nodes
        prev.value += next_.value
        parent.remove(next_)

def sanitize_template(template: Template, removeComments: bool = False):
	for parameter in template.params:
		name = str(parameter.name)
		value = str(parameter.value).strip()
		isValueSet = True if len(value) > 0 else False
		if isValueSet and (('vod2' in name) or ('vod3' in name) or ('vod4' in name) or ('vod5' in name) or ('vod1' in name)):
			raise VodX
		if isValueSet and ('2vod' in name):
			raise VodX
		if isValueSet and ('[' in value or "''" in value or ']' in value):
			raise WikiStyle
		if '<!--' in value and removeComments:
			value = re.sub(r'(<!--.*?-->)', '', value, 0, re.MULTILINE)
		template.add(str(parameter.name), value.strip(), preserve_spacing=False)
	return template

def get_value(template: Template, key: str = None, index: int = -1) -> str:
	'''Check if template has a key, if true return str(value) or empty string'''
	if template is None:
		return None
	if key:
		if template.has(key):
			return str(template.get(key).value)
	if index >= 0:
		if len(template.params) > index:
			return str(template.params[index].value)
	return None

def dict_has_value_set(dictionary: dict) -> bool:
	for _, v in dictionary.items():
		if v != '':
			return True
	return False