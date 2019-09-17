from lxml import html

def get_value_by_attr(attr, tree):
    base = "//b[contains(text(), '%s')]/../following-sibling::td" % attr
    if attr in ["Indirizzo web", "Posta elettronica", "Commercio elettronico"]:
        base += "/a"

    value = ''

    try:
        value = tree.xpath("%s/text()" % base)[0].strip()
    except IndexError as e:
        print("[ERROR] %s" % str(e))

    return value


def create_json(attrs, tree):
    my_contact = {}
    for attr in attrs:
        my_contact[attr] = get_value_by_attr(attr, tree)
    return my_contact


def get_contact_by_crawled_page(pageText, fields):
    tree = html.fromstring(pageText)

    contact = create_json(fields, tree)

    return contact
